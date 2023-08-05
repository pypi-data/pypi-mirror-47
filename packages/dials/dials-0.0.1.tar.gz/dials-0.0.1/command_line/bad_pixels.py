# LIBTBX_SET_DISPATCHER_NAME dev.dials.bad_pixels

from __future__ import absolute_import, division, print_function

import iotbx.phil
import libtbx.load_env
from scitbx.array_family import flex
from dials.util import Sorry
from dials.algorithms.spot_finding.factory import SpotFinderFactory
from dials.algorithms.spot_finding.factory import phil_scope as spot_phil
from dxtbx.model.experiment_list import ExperimentList, Experiment
from libtbx import easy_pickle

help_message = (
    """

Examples::

  %s data_master.h5

"""
    % libtbx.env.dispatcher_name
)

phil_scope = iotbx.phil.parse(
    """
images = None
  .type = ints
  .help = "Images on which to perform the analysis (otherwise use all images)"
output {
    mask = mask.pickle
        .type = path
        .help = "Output mask file name"
}
"""
)


def run(args):

    from dials.util.options import OptionParser
    from dials.util.options import flatten_experiments

    usage = "%s [options] data_master.h5" % (libtbx.env.dispatcher_name)

    parser = OptionParser(
        usage=usage,
        phil=phil_scope,
        read_experiments=True,
        read_experiments_from_images=True,
        epilog=help_message,
    )

    params, options = parser.parse_args(show_diff_phil=True)

    experiments = flatten_experiments(params.input.experiments)
    if len(experiments) != 1:
        parser.print_help()
        print("Please pass an experiment list\n")
        return

    imagesets = experiments.imagesets()

    if len(imagesets) != 1:
        raise Sorry("Please pass an experiment list that contains one imageset")

    imageset = imagesets[0]

    first, last = imageset.get_scan().get_image_range()
    images = range(first, last + 1)

    if params.images:
        if min(params.images) < first or max(params.images) > last:
            raise Sorry("image outside of scan range")
        images = params.images

    detectors = imageset.get_detector()
    assert len(detectors) == 1
    detector = detectors[0]
    trusted = detector.get_trusted_range()

    # construct an integer array same shape as image; accumulate number of
    # "signal" pixels in each pixel across data

    total = None

    from dials.util.command_line import ProgressBar

    p = ProgressBar(title="Finding hot pixels")

    for idx in images:

        p.update(idx * 100.0 / len(images))

        pixels = imageset.get_raw_data(idx - 1)
        assert len(pixels) == 1
        data = pixels[0]

        negative = data < int(round(trusted[0]))
        hot = data > int(round(trusted[1]))
        bad = negative | hot

        data = data.as_double()

        spot_params = spot_phil.fetch(
            source=iotbx.phil.parse("min_spot_size=1")
        ).extract()
        threshold_function = SpotFinderFactory.configure_threshold(
            spot_params,
            ExperimentList(
                [
                    Experiment(
                        beam=imageset.get_beam(),
                        detector=imageset.get_detector(),
                        goniometer=imageset.get_goniometer(),
                        scan=imageset.get_scan(),
                        imageset=imageset,
                    )
                ]
            ),
        )
        peak_pixels = threshold_function.compute_threshold(data, ~bad)

        if total is None:
            total = peak_pixels.as_1d().as_int()
        else:
            total += peak_pixels.as_1d().as_int()

    p.finished(
        "Found %d hot pixels on %d images" % (total.count(len(images)), len(images))
    )

    hot_mask = total == len(images)
    hot_mask.reshape(flex.grid(data.focus()))

    easy_pickle.dump(params.output.mask, (~hot_mask,))


if __name__ == "__main__":
    import sys

    run(sys.argv[1:])
