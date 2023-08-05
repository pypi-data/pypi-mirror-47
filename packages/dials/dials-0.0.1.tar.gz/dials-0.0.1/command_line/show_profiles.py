# LIBTBX_SET_DISPATCHER_NAME dev.dials.show_profiles
from __future__ import absolute_import, division, print_function


def print_profile(r):
    s = r["shoebox"].data
    _i, _j, _k = s.all()
    for i in range(_i):
        for j in range(_j):
            for k in range(_k):
                print("%5d" % int(s[i, j, k]), end=" ")
            print("")
        print("")
        print("")


def show_profiles(integrated_reflections, isig_limit=None):
    from dials.array_family import flex
    import math

    integrated_data = flex.reflection_table.from_file(integrated_reflections)

    for j, r in enumerate(integrated_data):
        if isig_limit is not None:
            if r["intensity.sum.value"] <= 0:
                continue
            if (
                r["intensity.sum.value"] / math.sqrt(r["intensity.sum.variance"])
                < isig_limit
            ):
                continue

        print_profile(r)


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        show_profiles(sys.argv[1], None)
    else:
        show_profiles(sys.argv[1], isig_limit=float(sys.argv[2]))
