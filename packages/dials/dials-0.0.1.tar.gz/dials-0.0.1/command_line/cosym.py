from __future__ import absolute_import, division, print_function

# LIBTBX_PRE_DISPATCHER_INCLUDE_SH export BOOST_ADAPTBX_FPE_DEFAULT=1

import logging

logger = logging.getLogger("dials.command_line.cosym")

import iotbx.phil
from cctbx import crystal, miller
from cctbx import sgtbx
from dxtbx.serialize import dump
from dials.array_family import flex
from dials.util.options import flatten_experiments, flatten_reflections
from dials.util.multi_dataset_handling import (
    assign_unique_identifiers,
    parse_multiple_datasets,
    select_datasets_on_ids,
)
from dials.util.observer import Subject
from dials.algorithms.symmetry.cosym.observers import register_default_cosym_observers
from dials.algorithms.symmetry.cosym import CosymAnalysis


phil_scope = iotbx.phil.parse(
    """\
partiality_threshold = 0.99
  .type = float
  .help = "Use reflections with a partiality above the threshold."

unit_cell_clustering {
  threshold = 5000
    .type = float(value_min=0)
    .help = 'Threshold value for the clustering'
  log = False
    .type = bool
    .help = 'Display the dendrogram with a log scale'
}

include scope dials.algorithms.symmetry.cosym.phil_scope

seed = 230
  .type = int(value_min=0)

output {
  suffix = "_reindexed"
    .type = str
  log = dials.cosym.log
    .type = str
  debug_log = dials.cosym.debug.log
    .type = str
  experiments = "reindexed_experiments.json"
    .type = path
  reflections = "reindexed_reflections.pickle"
    .type = path
  json = dials.cosym.json
    .type = path
  html = dials.cosym.html
    .type = path
}

verbosity = 1
  .type = int(value_min=0)
  .help = "The verbosity level"
""",
    process_includes=True,
)


class cosym(Subject):
    def __init__(self, experiments, reflections, params=None):
        super(cosym, self).__init__(
            events=["run_cosym", "performed_unit_cell_clustering"]
        )
        if params is None:
            params = phil_scope.extract()
        self.params = params

        # map experiments and reflections to primitive setting
        self._experiments, self._reflections = self._map_to_primitive(
            experiments, reflections
        )

        if len(self._experiments) > 1:
            # perform unit cell clustering
            identifiers = self._unit_cell_clustering(self._experiments)
            if len(identifiers) < len(self._experiments):
                logger.info(
                    "Selecting subset of %i datasets for cosym analysis: %s",
                    len(identifiers),
                    str(identifiers),
                )
                self._experiments, self._reflections = select_datasets_on_ids(
                    self._experiments, self._reflections, use_datasets=identifiers
                )

        self._experiments, self._reflections = self._map_to_minimum_cell(
            self._experiments, self._reflections
        )

        # transform models into miller arrays
        datasets = self._miller_arrays_from_experiments_reflections(
            self._experiments, self._reflections
        )

        self.cosym_analysis = CosymAnalysis(datasets, self.params)

    @property
    def experiments(self):
        """Return the experiment list."""
        return self._experiments

    @property
    def reflections(self):
        """Return the list of reflection tables."""
        return self._reflections

    @Subject.notify_event(event="run_cosym")
    def run(self):
        self.cosym_analysis.run()

        space_groups = {}
        reindexing_ops = {}
        for dataset_id in self.cosym_analysis.reindexing_ops.iterkeys():
            if 0 in self.cosym_analysis.reindexing_ops[dataset_id]:
                cb_op = self.cosym_analysis.reindexing_ops[dataset_id][0]
                reindexing_ops.setdefault(cb_op, [])
                reindexing_ops[cb_op].append(dataset_id)
            if dataset_id in self.cosym_analysis.space_groups:
                space_groups.setdefault(
                    self.cosym_analysis.space_groups[dataset_id], []
                )
                space_groups[self.cosym_analysis.space_groups[dataset_id]].append(
                    dataset_id
                )

        logger.info("Space groups:")
        for sg, datasets in space_groups.iteritems():
            logger.info(str(sg.info().reference_setting()))
            logger.info(datasets)

        logger.info("Reindexing operators:")
        for cb_op, datasets in reindexing_ops.iteritems():
            logger.info(cb_op)
            logger.info(datasets)

        if self.cosym_analysis.best_solution is not None:
            subgroup = self.cosym_analysis.best_solution.subgroup
        else:
            subgroup = None

        self._apply_reindexing_operators(reindexing_ops, subgroup=subgroup)

    def export(self):
        """Output the datafiles for cosym.

        This includes the cosym.json, reflections and experiments files."""

        reindexed_reflections = flex.reflection_table()
        for refl in self._reflections:
            reindexed_reflections.extend(refl)
        reindexed_reflections.reset_ids()

        if self.params.output.json is not None:
            self.cosym_analysis.as_json(filename=self.params.output.json)
        logger.info(
            "Saving reindexed experiments to %s", self.params.output.experiments
        )
        dump.experiment_list(self._experiments, self.params.output.experiments)
        logger.info(
            "Saving reindexed reflections to %s", self.params.output.reflections
        )
        reindexed_reflections.as_pickle(self.params.output.reflections)

    def _apply_reindexing_operators(self, reindexing_ops, subgroup=None):
        """Apply the reindexing operators to the reflections and experiments."""
        for cb_op, dataset_ids in reindexing_ops.iteritems():
            cb_op = sgtbx.change_of_basis_op(cb_op)
            if subgroup is not None:
                cb_op = subgroup["cb_op_inp_best"] * cb_op
            for dataset_id in dataset_ids:
                expt = self._experiments[dataset_id]
                refl = self._reflections[dataset_id]
                expt.crystal = expt.crystal.change_basis(cb_op)
                if subgroup is not None:
                    expt.crystal.set_space_group(
                        subgroup["best_subsym"]
                        .space_group()
                        .build_derived_acentric_group()
                    )
                expt.crystal.set_unit_cell(
                    expt.crystal.get_space_group().average_unit_cell(
                        expt.crystal.get_unit_cell()
                    )
                )
                refl["miller_index"] = cb_op.apply(refl["miller_index"])

    def _miller_arrays_from_experiments_reflections(self, experiments, reflections):
        miller_arrays = []

        for expt, refl in zip(experiments, reflections):
            crystal_symmetry = crystal.symmetry(
                unit_cell=expt.crystal.get_unit_cell(),
                space_group=expt.crystal.get_space_group(),
            )

            from dials.util.filter_reflections import filter_reflection_table

            if "intensity.scale.value" in refl:
                intensity_choice = ["scale"]
                intensity_to_use = "scale"
            else:
                assert "intensity.sum.value" in refl
                intensity_choice = ["sum"]
                if "intensity.prf.value" in refl:
                    intensity_choice.append("profile")
                    intensity_to_use = "prf"
                else:
                    intensity_to_use = "sum"

            refl = filter_reflection_table(
                refl,
                intensity_choice,
                min_isigi=-5,
                filter_ice_rings=False,
                combine_partials=True,
                partiality_threshold=self.params.partiality_threshold,
            )
            assert refl.size() > 0
            try:
                data = refl["intensity." + intensity_to_use + ".value"]
                variances = refl["intensity." + intensity_to_use + ".variance"]
            except RuntimeError:
                data = refl["intensity.sum.value"]
                variances = refl["intensity.sum.variance"]

            miller_indices = refl["miller_index"]
            assert variances.all_gt(0)
            sigmas = flex.sqrt(variances)

            miller_set = miller.set(
                crystal_symmetry, miller_indices, anomalous_flag=False
            )
            intensities = miller.array(miller_set, data=data, sigmas=sigmas)
            intensities.set_observation_type_xray_intensity()
            intensities.set_info(
                miller.array_info(source="DIALS", source_type="pickle")
            )
            miller_arrays.append(intensities)

        return miller_arrays

    def _map_to_primitive(self, experiments, reflections):
        identifiers = []

        for expt, refl in zip(experiments, reflections):
            cb_op_to_primitive = (
                expt.crystal.get_crystal_symmetry().change_of_basis_op_to_primitive_setting()
            )
            sel = expt.crystal.get_space_group().is_sys_absent(refl["miller_index"])
            if sel.count(True):
                logger.info(
                    "Eliminating %i systematic absences for experiment %s",
                    sel.count(True),
                    expt.identifier,
                )
                refl = refl.select(~sel)
            refl["miller_index"] = cb_op_to_primitive.apply(refl["miller_index"])
            expt.crystal = expt.crystal.change_basis(cb_op_to_primitive)

            if self.params.space_group is not None:
                space_group_info = self.params.space_group.primitive_setting()
                if not space_group_info.group().is_compatible_unit_cell(
                    expt.crystal.get_unit_cell()
                ):
                    logger.info(
                        "Skipping data set - incompatible space group and unit cell: %s, %s",
                        space_group_info,
                        expt.crystal.get_unit_cell(),
                    )
                    continue
            else:
                expt.crystal.set_space_group(sgtbx.space_group())
            identifiers.append(expt.identifier)

        return select_datasets_on_ids(
            experiments, reflections, use_datasets=identifiers
        )

    def _map_to_minimum_cell(self, experiments, reflections):
        cb_op_ref_min = (
            experiments[0]
            .crystal.get_crystal_symmetry()
            .change_of_basis_op_to_minimum_cell()
        )
        for expt, refl in zip(experiments, reflections):
            expt.crystal = expt.crystal.change_basis(cb_op_ref_min)
            refl["miller_index"] = cb_op_ref_min.apply(refl["miller_index"])

            if self.params.space_group is not None:
                expt.crystal.set_space_group(
                    self.params.space_group.primitive_setting().group()
                )
                expt.crystal.set_unit_cell(
                    expt.crystal.get_space_group().average_unit_cell(
                        expt.crystal.get_unit_cell()
                    )
                )
            else:
                expt.crystal.set_space_group(sgtbx.space_group())
        return experiments, reflections

    @Subject.notify_event("performed_unit_cell_clustering")
    def _unit_cell_clustering(self, experiments):
        crystal_symmetries = [
            expt.crystal.get_crystal_symmetry() for expt in experiments
        ]
        lattice_ids = experiments.identifiers()
        from dials.algorithms.clustering.unit_cell import UnitCellCluster
        from xfel.clustering.cluster_groups import unit_cell_info

        ucs = UnitCellCluster.from_crystal_symmetries(
            crystal_symmetries, lattice_ids=lattice_ids
        )
        self.unit_cell_clusters, self.unit_cell_dendrogram, _ = ucs.ab_cluster(
            self.params.unit_cell_clustering.threshold,
            log=self.params.unit_cell_clustering.log,
            labels="lattice_id",
            write_file_lists=False,
            schnell=False,
            doplot=False,
        )
        logger.info(unit_cell_info(self.unit_cell_clusters))
        largest_cluster_lattice_ids = None
        for cluster in self.unit_cell_clusters:
            cluster_lattice_ids = [m.lattice_id for m in cluster.members]
            if largest_cluster_lattice_ids is None:
                largest_cluster_lattice_ids = cluster_lattice_ids
            elif len(cluster_lattice_ids) > len(largest_cluster_lattice_ids):
                largest_cluster_lattice_ids = cluster_lattice_ids

        dataset_selection = largest_cluster_lattice_ids
        return dataset_selection


help_message = """
This program implements the methods of `Gildea, R. J. & Winter, G. (2018).
Acta Cryst. D74, 405-410 <https://doi.org/10.1107/S2059798318002978>`_ for
determination of Patterson group symmetry from sparse multi-crystal data sets in
the presence of an indexing ambiguity.

The program takes as input a set of integrated experiments and reflections,
either in one file per experiment, or with all experiments combined in a single
experiments.json and reflections.pickle file. It will perform analysis of the
symmetry elements present in the datasets and, if necessary, reindex experiments
and reflections as necessary to ensure that all output experiments and
reflections are indexed consistently.

Examples::

  dials.cosym experiments.json reflections.pickle

  dials.cosym experiments.json reflections.pickle space_group=I23

  dials.cosym experiments.json reflections.pickle space_group=I23 lattice_group=I23

"""


def run(args):
    from dials.util import log
    from dials.util.options import OptionParser

    usage = "dials.cosym [options] experiments.json reflections.pickle"

    parser = OptionParser(
        usage=usage,
        phil=phil_scope,
        read_reflections=True,
        read_experiments=True,
        check_format=False,
        epilog=help_message,
    )

    params, _, args = parser.parse_args(
        args=args, show_diff_phil=False, return_unhandled=True
    )

    # Configure the logging
    log.config(params.verbosity, info=params.output.log, debug=params.output.debug_log)

    from dials.util.version import dials_version

    logger.info(dials_version())

    # Log the diff phil
    diff_phil = parser.diff_phil.as_str()
    if diff_phil is not "":
        logger.info("The following parameters have been modified:\n")
        logger.info(diff_phil)

    if params.seed is not None:
        import random

        flex.set_random_seed(params.seed)
        random.seed(params.seed)

    if not params.input.experiments or not params.input.reflections:
        parser.print_help()
        sys.exit()

    experiments = flatten_experiments(params.input.experiments)
    reflections = flatten_reflections(params.input.reflections)
    reflections = parse_multiple_datasets(reflections)
    experiments, reflections = assign_unique_identifiers(experiments, reflections)

    cosym_instance = cosym(
        experiments=experiments, reflections=reflections, params=params
    )
    if params.output.html:
        register_default_cosym_observers(cosym_instance)
    cosym_instance.run()
    cosym_instance.export()


if __name__ == "__main__":
    import sys

    run(sys.argv[1:])
