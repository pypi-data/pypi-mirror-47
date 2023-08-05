from __future__ import absolute_import, division, print_function

import collections
import logging

logger = logging.getLogger(__name__)


def generate_phil_scope():
    from iotbx.phil import parse
    import dials.extensions

    phil_scope = parse(
        """

  spotfinder
    .help = "Parameters used in the spot finding algorithm."
  {
    include scope dials.data.lookup.phil_scope

    write_hot_mask = False
      .type = bool
      .help = "Write the hot mask"

    hot_mask_prefix = 'hot_mask'
      .type = str
      .help = "Prefix for the hot mask pickle file"

    force_2d = False
      .type = bool
      .help = "Do spot finding in 2D"

    scan_range = None
      .help = "The range of images to use in finding spots. The ranges are"
              "inclusive (e.g. j0 <= j < j1)."
              "For sweeps the scan range is interpreted as the literal scan"
              "range. Whereas for imagesets the scan range is interpreted as"
              "the image number in the imageset. Multiple ranges can be"
              "specified by repeating the scan_range= parameter."
      .type = ints(size=2)
      .multiple = True

    region_of_interest = None
      .type = ints(size=4)
      .help = "A region of interest to look for spots."
              "Specified as: x0,x1,y0,y1"
              "The pixels x0 and y0 are included in the range but the pixels x1 and y1"
              "are not. To specify an ROI covering the whole image set"
              "region_of_interest=0,width,0,height."

    compute_mean_background = False
      .type = bool
      .help = "Compute the mean background for each image"

    filter
      .help = "Parameters used in the spot finding filter strategy."

    {
      min_spot_size = Auto
        .help = "The minimum number of contiguous pixels for a spot"
                "to be accepted by the filtering algorithm."
        .type = int(value_min=1)

      max_spot_size = 100
        .help = "The maximum number of contiguous pixels for a spot"
                "to be accepted by the filtering algorithm."
        .type = int(value_min=1, allow_none=False)

      max_separation = 2
        .help = "The maximum peak-to-centroid separation (in pixels)"
                "for a spot to be accepted by the filtering algorithm."
        .type = float(value_min=0)
        .expert_level = 1

      max_strong_pixel_fraction = 0.25
        .help = "If the fraction of pixels in an image marked as strong is"
                "greater than this value, throw an exception"
        .type = float(value_min=0, value_max=1)

      background_gradient
        .expert_level=2
      {
        filter = False
          .type = bool
        background_size = 2
          .type = int(value_min=1)
        gradient_cutoff = 4
          .type = float(value_min=0)
      }

      spot_density
        .expert_level=2
      {
        filter = False
          .type = bool
      }

      include scope dials.util.masking.phil_scope
    }

    mp {
      method = *none drmaa sge lsf pbs
        .type = choice
        .help = "The cluster method to use"

      njobs = 1
        .type = int(value_min=1)
        .help = "The number of cluster jobs to use"

      nproc = 1
        .type = int(value_min=1)
        .help = "The number of processes to use per cluster job"

      chunksize = auto
        .type = int(value_min=1)
        .help = "The number of jobs to process per process"

      min_chunksize = 20
        .type = int(value_min=1)
        .help = "When chunksize is auto, this is the minimum chunksize"
    }
  }

  """,
        process_includes=True,
    )

    main_scope = phil_scope.get_without_substitution("spotfinder")
    assert len(main_scope) == 1
    main_scope = main_scope[0]
    main_scope.adopt_scope(dials.extensions.SpotFinderThreshold.phil_scope())
    return phil_scope


phil_scope = generate_phil_scope()


class FilterRunner(object):
    """
    A class to run multiple filters in succession.

    """

    def __init__(self, filters=None):
        """
        Initialise with a list of filters.

        :param filters: The list of filters

        """
        if filters is None:
            self.filters = []
        else:
            self.filters = filters

    def __call__(self, flags, **kwargs):
        """
        Call the filters one by one.

        :param flags: The input flags
        :returns: The filtered flags

        """
        flags = self.check_flags(flags, **kwargs)
        for f in self.filters:
            flags = f(flags, **kwargs)
        return flags

    def check_flags(
        self, flags, predictions=None, observations=None, shoeboxes=None, **kwargs
    ):
        """
        Check the flags are set, if they're not then create a list
        of Trues equal to the number of items given.

        :param flags: The input flags
        :param predictions: The predictions
        :param observations: The observations
        :param shoeboxes: The shoeboxes
        :return: The filtered flags

        """
        from scitbx.array_family import flex

        # If flags are not set then create a list of Trues
        if flags is None:
            length = 0
            if predictions:
                length = len(predictions)
            if observations:
                if length > 0:
                    assert length == len(observations)
                else:
                    length = len(observations)
            if shoeboxes:
                if length > 0:
                    assert length == len(observations)
                else:
                    length = len(shoeboxes)

            # Create an array of flags
            flags = flex.bool(length, True)

        # Return the flags
        return flags


class PeakCentroidDistanceFilter(object):
    def __init__(self, maxd):
        """
        Initialise

        :param maxd: The maximum distance allowed

        """
        self.maxd = maxd

    def run(self, flags, observations=None, shoeboxes=None, **kwargs):
        """
        Run the filtering.

        """

        # Get the peak locations and the centroids and return the flags of
        # those closer than the min distance
        peak = shoeboxes.peak_coordinates()
        cent = observations.centroids().px_position()
        return flags.__and__((peak - cent).norms() <= self.maxd)

    def __call__(self, flags, **kwargs):
        """ Call the filter and print information. """
        num_before = flags.count(True)
        flags = self.run(flags, **kwargs)
        num_after = flags.count(True)
        logger.info(
            "Filtered {0} of {1} spots by peak-centroid distance".format(
                num_after, num_before
            )
        )
        return flags


class BackgroundGradientFilter(object):
    def __init__(self, background_size=2, gradient_cutoff=4):
        self.background_size = background_size
        self.gradient_cutoff = gradient_cutoff

    def run(self, flags, sweep=None, shoeboxes=None, **kwargs):
        from dials.array_family import flex
        from dials.algorithms.background.simple import Linear2dModeller

        modeller = Linear2dModeller()
        detector = sweep.get_detector()

        class image_data_cache(object):
            def __init__(self, imageset, size=10):
                self.imageset = imageset
                self.size = size
                self._image_data = collections.OrderedDict()

            def __getitem__(self, i):
                image_data = self._image_data.get(i)
                if image_data is None:
                    image_data = self.imageset.get_raw_data(i)
                    if len(self._image_data) >= self.size:
                        # remove the oldest entry in the cache
                        del self._image_data[self._image_data.keys()[0]]
                    self._image_data[i] = image_data
                return image_data

        # sort shoeboxes by centroid z
        frame = shoeboxes.centroid_all().position_frame()
        perm = flex.sort_permutation(frame)
        shoeboxes = shoeboxes.select(perm)
        buffer_size = 1
        bg_plus_buffer = self.background_size + buffer_size

        import time

        t0 = time.time()
        for i, shoebox in enumerate(shoeboxes):
            if not flags[perm[i]]:
                continue
            panel = detector[shoebox.panel]
            max_x, max_y = panel.get_image_size()
            bbox = shoebox.bbox
            x1, x2, y1, y2, z1, z2 = bbox
            # expand the bbox with a background region around the spotfinder shoebox
            # perhaps also should use a buffer zone between the shoebox and the
            # background region
            expanded_bbox = (
                max(0, x1 - bg_plus_buffer),
                min(max_x, x2 + bg_plus_buffer),
                max(0, y1 - bg_plus_buffer),
                min(max_y, y2 + bg_plus_buffer),
                z1,
                z2,
            )
            shoebox.bbox = expanded_bbox
        t1 = time.time()
        logger.info("Time expand_shoebox: %s" % (t1 - t0))

        rlist = flex.reflection_table()
        rlist["shoebox"] = shoeboxes
        rlist["shoebox"].allocate()
        rlist["panel"] = shoeboxes.panels()
        rlist["bbox"] = shoeboxes.bounding_boxes()

        rlist.extract_shoeboxes(sweep)

        shoeboxes = rlist["shoebox"]
        shoeboxes.flatten()

        for i, shoebox in enumerate(shoeboxes):
            if not flags[perm[i]]:
                continue
            panel = detector[shoebox.panel]
            trusted_range = panel.get_trusted_range()
            ex1, ex2, ey1, ey2, ez1, ez2 = shoebox.bbox
            data = shoebox.data
            mask = flex.bool(data.accessor(), False)
            for i_y, y in enumerate(range(ey1, ey2)):
                for i_x, x in enumerate(range(ex1, ex2)):
                    value = data[0, i_y, i_x]
                    if (
                        y >= (ey1 + buffer_size)
                        and y < (ey2 - buffer_size)
                        and x >= (ex1 + buffer_size)
                        and x < (ex2 - buffer_size)
                    ):
                        mask[0, i_y, i_x] = False  # foreground
                    elif value > trusted_range[0] and value < trusted_range[1]:
                        mask[0, i_y, i_x] = True  # background

            model = modeller.create(data.as_double(), mask)
            d, a, b = model.params()[:3]

            if abs(a) > self.gradient_cutoff or abs(b) > self.gradient_cutoff:
                flags[perm[i]] = False

        return flags

    def __call__(self, flags, **kwargs):
        """ Call the filter and print information. """
        num_before = flags.count(True)
        flags = self.run(flags, **kwargs)
        num_after = flags.count(True)
        logger.info(
            "Filtered {0} or {1} spots by background gradient".format(
                num_after, num_before
            )
        )
        return flags


class SpotDensityFilter(object):
    def __init__(self, nbins=50, gradient_cutoff=0.002):
        self.nbins = nbins
        self.gradient_cutoff = gradient_cutoff

    def run(self, flags, sweep=None, observations=None, **kwargs):
        obs_x, obs_y = observations.centroids().px_position_xy().parts()

        import numpy as np

        H, xedges, yedges = np.histogram2d(
            obs_x.as_numpy_array(), obs_y.as_numpy_array(), bins=self.nbins
        )

        from scitbx.array_family import flex

        H_flex = flex.double(H.flatten().astype(np.float64))
        n_slots = min(int(flex.max(H_flex)), 30)
        hist = flex.histogram(H_flex, n_slots=n_slots)

        slots = hist.slots()
        cumulative_hist = flex.long(len(slots))
        for i in range(len(slots)):
            cumulative_hist[i] = slots[i]
            if i > 0:
                cumulative_hist[i] += cumulative_hist[i - 1]

        cumulative_hist = cumulative_hist.as_double() / flex.max(
            cumulative_hist.as_double()
        )

        cutoff = None
        gradients = flex.double()
        for i in range(len(slots) - 1):
            x1 = cumulative_hist[i]
            x2 = cumulative_hist[i + 1]
            g = (x2 - x1) / hist.slot_width()
            gradients.append(g)
            if (
                cutoff is None
                and i > 0
                and g < self.gradient_cutoff
                and gradients[i - 1] < self.gradient_cutoff
            ):
                cutoff = hist.slot_centers()[i - 1] - 0.5 * hist.slot_width()

        H_flex = flex.double(np.ascontiguousarray(H))
        sel = np.column_stack(np.where(H > cutoff))
        for (ix, iy) in sel:
            flags.set_selected(
                (
                    (obs_x > xedges[ix])
                    & (obs_x < xedges[ix + 1])
                    & (obs_y > yedges[iy])
                    & (obs_y < yedges[iy + 1])
                ),
                False,
            )

        if 0:
            from matplotlib import pyplot

            fig, ax1 = pyplot.subplots()
            extent = [yedges[0], yedges[-1], xedges[0], xedges[-1]]
            plot1 = ax1.imshow(H, extent=extent, interpolation="nearest")
            pyplot.xlim((0, pyplot.xlim()[1]))
            pyplot.ylim((0, pyplot.ylim()[1]))
            pyplot.gca().invert_yaxis()
            cbar1 = pyplot.colorbar(plot1)
            pyplot.axes().set_aspect("equal")
            pyplot.show()

            fig, ax1 = pyplot.subplots()
            ax2 = ax1.twinx()
            ax1.scatter(hist.slot_centers() - 0.5 * hist.slot_width(), cumulative_hist)
            ax1.set_ylim(0, 1)
            ax2.plot(hist.slot_centers()[:-1] - 0.5 * hist.slot_width(), gradients)
            ymin, ymax = pyplot.ylim()
            pyplot.vlines(cutoff, ymin, ymax, color="r")
            pyplot.show()

            H2 = H.copy()
            if cutoff is not None:
                H2[np.where(H2 >= cutoff)] = 0
            fig, ax1 = pyplot.subplots()
            plot1 = ax1.pcolormesh(xedges, yedges, H2)
            pyplot.xlim((0, pyplot.xlim()[1]))
            pyplot.ylim((0, pyplot.ylim()[1]))
            pyplot.gca().invert_yaxis()
            cbar1 = pyplot.colorbar(plot1)
            pyplot.axes().set_aspect("equal")
            pyplot.show()

        return flags

    def __call__(self, flags, **kwargs):
        """ Call the filter and print information. """
        num_before = flags.count(True)
        flags = self.run(flags, **kwargs)
        num_after = flags.count(True)
        logger.info(
            "Filtered {0} of {1} spots by spot density".format(num_after, num_before)
        )
        return flags


class SpotFinderFactory(object):
    """
    Factory class to create spot finders

    """

    @staticmethod
    def from_parameters(params=None, experiments=None):
        """
        Given a set of parameters, construct the spot finder

        :param params: The input parameters
        :returns: The spot finder instance

        """
        from dials.util.masking import MaskGenerator
        from dials.algorithms.spot_finding.finder import SpotFinder
        from libtbx.phil import parse
        from dxtbx.imageset import ImageSweep

        if params is None:
            params = phil_scope.fetch(source=parse("")).extract()

        if params.spotfinder.force_2d and params.output.shoeboxes is False:
            no_shoeboxes_2d = True
        elif experiments is not None and params.output.shoeboxes is False:
            no_shoeboxes_2d = False
            all_stills = True
            for experiment in experiments:
                if isinstance(experiment.imageset, ImageSweep):
                    all_stills = False
                    break
            if all_stills:
                no_shoeboxes_2d = True
        else:
            no_shoeboxes_2d = False

        # Read in the lookup files
        mask = SpotFinderFactory.load_image(params.spotfinder.lookup.mask)
        params.spotfinder.lookup.mask = mask

        # Configure the filter options
        filter_spots = SpotFinderFactory.configure_filter(params)

        # Create the threshold strategy
        threshold_function = SpotFinderFactory.configure_threshold(params, experiments)

        # Configure the mask generator
        mask_generator = MaskGenerator(params.spotfinder.filter)

        # Make sure 'none' is interpreted as None
        if params.spotfinder.mp.method == "none":
            params.spotfinder.mp.method = None

        # Setup the spot finder
        return SpotFinder(
            threshold_function=threshold_function,
            mask=params.spotfinder.lookup.mask,
            filter_spots=filter_spots,
            scan_range=params.spotfinder.scan_range,
            write_hot_mask=params.spotfinder.write_hot_mask,
            hot_mask_prefix=params.spotfinder.hot_mask_prefix,
            mp_method=params.spotfinder.mp.method,
            mp_nproc=params.spotfinder.mp.nproc,
            mp_njobs=params.spotfinder.mp.njobs,
            mp_chunksize=params.spotfinder.mp.chunksize,
            max_strong_pixel_fraction=params.spotfinder.filter.max_strong_pixel_fraction,
            compute_mean_background=params.spotfinder.compute_mean_background,
            region_of_interest=params.spotfinder.region_of_interest,
            mask_generator=mask_generator,
            min_spot_size=params.spotfinder.filter.min_spot_size,
            max_spot_size=params.spotfinder.filter.max_spot_size,
            no_shoeboxes_2d=no_shoeboxes_2d,
            min_chunksize=params.spotfinder.mp.min_chunksize,
        )

    @staticmethod
    def configure_threshold(params, experiments):
        """
        Get the threshold strategy

        :param params: The input parameters
        :return: The threshold algorithm

        """
        import dials.extensions

        # Configure the algotihm
        Algorithm = dials.extensions.SpotFinderThreshold.load(
            params.spotfinder.threshold.algorithm
        )
        return Algorithm(params)

    @staticmethod
    def configure_filter(params):
        """
        Get the filter strategy.

        :param params: The input parameters
        :return: The filter algorithm

        """
        # Initialise an empty list of filters
        filters = []

        # Add a peak-centroid distance filter
        if params.spotfinder.filter.max_separation is not None:
            filters.append(
                PeakCentroidDistanceFilter(params.spotfinder.filter.max_separation)
            )

        if params.spotfinder.filter.background_gradient.filter:
            bg_filter_params = params.spotfinder.filter.background_gradient
            filters.append(
                BackgroundGradientFilter(
                    background_size=bg_filter_params.background_size,
                    gradient_cutoff=bg_filter_params.gradient_cutoff,
                )
            )

        if params.spotfinder.filter.spot_density.filter:
            filters.append(SpotDensityFilter())

        # Return the filter runner with the list of filters
        return FilterRunner(filters)

    @staticmethod
    def load_image(filename_or_data):
        """
        Given a filename, load an image. If the data is already loaded, return it.

        :param filename_or_data: The input filename (or data)
        :return: The image or None

        """
        import six.moves.cPickle as pickle

        # If no filename is set then return None
        if not filename_or_data:
            return None

        # If it's already loaded, return early
        if isinstance(filename_or_data, tuple):
            return filename_or_data

        # Read the image and return the image data
        with open(filename_or_data, "rb") as fh:
            image = pickle.load(fh)
        if not isinstance(image, tuple):
            image = (image,)
        return image
