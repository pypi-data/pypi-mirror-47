from __future__ import absolute_import, division, print_function

import logging
import os

logger = logging.getLogger("dials.command_line.refine_bravais_settings")
from six.moves import cStringIO as StringIO
from dials.util import Sorry
import iotbx.phil

# from dials.util.command_line import Importer
from dials.util.options import OptionParser
from dials.util.options import flatten_reflections
from dials.util.options import flatten_experiments
from dials.array_family import flex

help_message = """

This program takes as input the output of dials.index, i.e. experiments.json
and indexed.pickle files. Full refinement of the crystal and experimental
geometry parameters will be performed (by default) in all Bravais settings
that are consistent with the input primitive unit cell. A table is printed
containing various information for each potential Bravais setting, including
the metric fit (a measure of the deviation from the triclinic cell),
the root-mean-square-deviations (rmsd), in mm, between the observed and
predicted spot centroids, the refined unit cell parameters in each Bravais
setting, and the change of basis operator to transform from the triclinic cell
to each Bravais setting.

The program also generates a .json file for each Bravais setting, e.g.
bravais_setting_1.json, which is equivalent to the input experiments.json, but
with the crystal model refined in the chosen Bravais setting. These
bravais_setting_*.json files are suitable as input to dials.refine or
dials.integrate, although the indexed.pickle file will need to be re-indexed
using dials.reindex if the change of basis operator (cb_op) for the chosen
Bravais setting is not the identity operator (a,b,c).

Examples::

  dials.refine_bravais_settings experiments.json indexed.pickle

  dials.refine_bravais_settings experiments.json indexed.pickle nproc=4

"""

phil_scope = iotbx.phil.parse(
    """
lepage_max_delta = 5
  .type = float
verbosity = 0
  .type = int(value_min=0)
nproc = Auto
  .type = int(value_min=1)
crystal_id = None
  .type = int(value_min=0)
normalise = False
  .type = bool
  .help = "Normalise intensities before calculating correlation coefficients."
normalise_bins = 0
  .type = int
  .help = "Number of resolution bins for normalisation"
cc_n_bins = None
  .type = int(value_min=1)
  .help = "Number of resolution bins to use for calculation of correlation coefficients"
output {
  directory = "."
    .type = path
  log = dials.refine_bravais_settings.log
    .type = path
  debug_log = dials.refine_bravais_settings.debug.log
    .type = path
  prefix = None
    .type = str
}

include scope dials.algorithms.refinement.refiner.phil_scope
""",
    process_includes=True,
)

# override default refinement parameters
phil_scope = phil_scope.fetch(
    source=iotbx.phil.parse(
        """\
refinement {
  reflections {
    reflections_per_degree=100
  }
}
"""
    )
)


def bravais_lattice_to_space_groups(chiral_only=True):
    from cctbx import sgtbx
    from cctbx.sgtbx import bravais_types
    import collections

    bravais_lattice_to_sg = collections.OrderedDict()
    for sgn in range(230):
        sg = sgtbx.space_group_info(number=sgn + 1).group()
        if (not chiral_only) or (sg.is_chiral()):
            bravais_lattice = bravais_types.bravais_lattice(group=sg)
            bravais_lattice_to_sg.setdefault(str(bravais_lattice), [])
            bravais_lattice_to_sg[str(bravais_lattice)].append(sg)
    return bravais_lattice_to_sg


def bravais_lattice_to_space_group_table(bravais_settings=None, chiral_only=True):
    bravais_lattice_to_sg = bravais_lattice_to_space_groups(chiral_only=chiral_only)
    logger.info("Chiral space groups corresponding to each Bravais lattice:")
    for bravais_lattice, space_groups in bravais_lattice_to_sg.iteritems():
        if bravais_settings is not None and bravais_lattice not in bravais_settings:
            continue
        logger.info(
            ": ".join(
                [
                    bravais_lattice,
                    " ".join([short_space_group_name(sg) for sg in space_groups]),
                ]
            )
        )


def short_space_group_name(space_group):
    sgt = space_group.type()
    symbol = sgt.lookup_symbol()
    if sgt.number() > 1:
        symbol = symbol.replace(" 1", "")
    return symbol.replace(" ", "")


def run(args=None):
    from dials.util import log
    import libtbx.load_env

    usage = "%s experiments.json indexed.pickle [options]" % libtbx.env.dispatcher_name

    parser = OptionParser(
        usage=usage,
        phil=phil_scope,
        read_experiments=True,
        read_reflections=True,
        check_format=False,
        epilog=help_message,
    )

    params, options = parser.parse_args(args=args, show_diff_phil=False)

    # Configure the logging
    log.config(info=params.output.log, debug=params.output.debug_log)

    from dials.util.version import dials_version

    logger.info(dials_version())

    # Log the diff phil
    diff_phil = parser.diff_phil.as_str()
    if diff_phil is not "":
        logger.info("The following parameters have been modified:\n")
        logger.info(diff_phil)

    experiments = flatten_experiments(params.input.experiments)
    reflections = flatten_reflections(params.input.reflections)
    if len(reflections) == 0 or len(experiments) == 0:
        parser.print_help()
        return

    assert len(reflections) == 1
    reflections = reflections[0]

    if len(experiments) == 0:
        parser.print_help()
        return
    elif len(experiments.crystals()) > 1:
        if params.crystal_id is not None:
            assert params.crystal_id < len(experiments.crystals())
            experiment_ids = experiments.where(
                crystal=experiments.crystals()[params.crystal_id]
            )
            from dxtbx.model.experiment_list import ExperimentList

            experiments = ExperimentList([experiments[i] for i in experiment_ids])
            refl_selections = [reflections["id"] == i for i in experiment_ids]
            reflections["id"] = flex.int(len(reflections), -1)
            for i, sel in enumerate(refl_selections):
                reflections["id"].set_selected(sel, i)
            reflections = reflections.select(reflections["id"] > -1)
        else:
            raise Sorry(
                "Only one crystal can be processed at a time: set crystal_id to choose experiment."
            )

    if params.refinement.reflections.outlier.algorithm in ("auto", libtbx.Auto):
        if experiments[0].goniometer is None:
            params.refinement.reflections.outlier.algorithm = "sauter_poon"
        else:
            # different default to dials.refine
            # tukey is faster and more appropriate at the indexing step
            params.refinement.reflections.outlier.algorithm = "tukey"

    from dials.algorithms.indexing.symmetry import (
        refined_settings_factory_from_refined_triclinic,
    )

    cb_op_to_primitive = (
        experiments[0]
        .crystal.get_space_group()
        .info()
        .change_of_basis_op_to_primitive_setting()
    )
    if experiments[0].crystal.get_space_group().n_ltr() > 1:
        effective_group = (
            experiments[0]
            .crystal.get_space_group()
            .build_derived_reflection_intensity_group(anomalous_flag=True)
        )
        sys_absent_flags = effective_group.is_sys_absent(reflections["miller_index"])
        reflections = reflections.select(~sys_absent_flags)
    experiments[0].crystal.update(
        experiments[0].crystal.change_basis(cb_op_to_primitive)
    )
    miller_indices = reflections["miller_index"]
    miller_indices = cb_op_to_primitive.apply(miller_indices)
    reflections["miller_index"] = miller_indices

    Lfat = refined_settings_factory_from_refined_triclinic(
        params,
        experiments,
        reflections,
        lepage_max_delta=params.lepage_max_delta,
        nproc=params.nproc,
        refiner_verbosity=params.verbosity,
    )
    s = StringIO()
    possible_bravais_settings = set(solution["bravais"] for solution in Lfat)
    bravais_lattice_to_space_group_table(possible_bravais_settings)
    Lfat.labelit_printout(out=s)
    logger.info(s.getvalue())
    import json

    prefix = params.output.prefix
    if prefix is None:
        prefix = ""
    summary_file = "%sbravais_summary.json" % prefix
    logger.info("Saving summary as %s" % summary_file)
    with open(os.path.join(params.output.directory, summary_file), "wb") as fh:
        json.dump(Lfat.as_dict(), fh)
    from dxtbx.serialize import dump

    for subgroup in Lfat:
        expts = subgroup.refined_experiments
        soln = int(subgroup.setting_number)
        bs_json = "%sbravais_setting_%i.json" % (prefix, soln)
        logger.info("Saving solution %i as %s" % (soln, bs_json))
        dump.experiment_list(expts, os.path.join(params.output.directory, bs_json))


if __name__ == "__main__":
    from libtbx.utils import show_times_at_exit

    show_times_at_exit()
    run()
