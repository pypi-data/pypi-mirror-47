#!/usr/bin/env python
#
# algorithm.py
#
#  Copyright (C) 2013 Diamond Light Source
#
#  Author: James Parkhurst
#
#  This code is distributed under the BSD license, a copy of which is
#  included in the root directory of this package.

from __future__ import absolute_import, division, print_function


class BackgroundAlgorithm(object):
    """ Class to do background subtraction. """

    def __init__(self, experiments):
        """
        Initialise the algorithm.

        :param experiments: The list of experiments

        """
        pass

    def compute_background(self, reflections, image_volume=None):
        """
        Compute the backgrond.

        :param reflections: The list of reflections

        """
        from dials.algorithms.background.median import create
        from dials.array_family import flex

        # Do the background subtraction
        if image_volume is None:
            success = create(reflections["shoebox"])
            reflections["background.mean"] = flex.double(
                [sbox.background[0] for sbox in reflections["shoebox"]]
            )
        else:
            success = create(reflections, image_volume)
        reflections.set_flags(success != True, reflections.flags.dont_integrate)
        return success
