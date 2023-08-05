# LIBTBX_SET_DISPATCHER_NAME dev.dials.make_polar_background_image

from __future__ import absolute_import, division, print_function

import logging

logger = logging.getLogger("dials.command_line.make_polar_background_image")

help_message = """

This program makes a polar background image

Examples::

dev.dials.make_polar_background_image experiments.json model=background.pickle

"""

import matplotlib

matplotlib.use("Agg")

# Create the phil scope
from libtbx.phil import parse

phil_scope = parse(
    """

  model = None
    .type = str
    .help = "The background model filename"

  output {
    data = 'polar.pickle'
      .type = str
      .help = "The filename for the output image"
    image = 'polar.png'
      .type = str
      .help = "The filename for the output image"
  }

"""
)


class Script(object):
    """ The integration program. """

    def __init__(self):
        """Initialise the script."""
        from dials.util.options import OptionParser
        import libtbx.load_env

        # The script usage
        usage = "usage: %s [options] experiment.json" % libtbx.env.dispatcher_name

        # Create the parser
        self.parser = OptionParser(
            usage=usage, phil=phil_scope, epilog=help_message, read_experiments=True
        )

    def run(self):
        """ Perform the integration. """
        from dials.util.options import flatten_experiments
        from dials.util import log
        from dials.array_family import flex

        # Parse the command line
        params, options = self.parser.parse_args(show_diff_phil=False)
        experiments = flatten_experiments(params.input.experiments)
        if len(experiments) == 0:
            self.parser.print_help()
            return

        assert len(experiments) == 1
        imageset = experiments[0].imageset
        beam = experiments[0].beam
        detector = experiments[0].detector
        goniometer = experiments[0].goniometer
        assert len(detector) == 1

        # Configure logging
        log.config()

        from dials.algorithms.background.gmodel import PolarTransform
        import six.moves.cPickle as pickle

        with open(params.model, "rb") as fh:
            model = pickle.load(fh)
        image = model.data(0)
        mask = flex.bool(image.accessor(), True)

        # Do the transformation
        transform = PolarTransform(beam, detector[0], goniometer)
        result = transform.to_polar(image, mask)
        data = result.data()
        mask = result.mask()

        with open(params.output.data, "wb") as fh:
            pickle.dump((data, mask), fh, pickle.HIGHEST_PROTOCOL)

        from matplotlib import pylab

        vmax = sorted(list(data))[int(0.99 * len(data))]
        figure = pylab.figure(figsize=(6, 4))
        pylab.imshow(data.as_numpy_array(), interpolation="none", vmin=0, vmax=vmax)
        ax1 = pylab.gca()
        ax1.get_xaxis().set_visible(False)
        ax1.get_yaxis().set_visible(False)
        cb = pylab.colorbar()
        cb.ax.tick_params(labelsize=8)
        logger.info("Saving polar model %s" % (params.output.image))
        pylab.savefig("%s" % (params.output.image), dpi=600, bbox_inches="tight")


if __name__ == "__main__":
    from dials.util import halraiser

    try:
        script = Script()
        script.run()
    except Exception as e:
        halraiser(e)
