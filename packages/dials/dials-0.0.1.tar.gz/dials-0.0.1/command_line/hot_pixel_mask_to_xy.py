from __future__ import absolute_import, division, print_function

# LIBTBX_SET_DISPATCHER_NAME dev.dials.hot_pixel_mask_to_xy


def hot_pixel_mask_to_xy(hot_pixel_mask):
    from six.moves import cPickle as pickle

    with open(hot_pixel_mask, "rb") as fh:
        mask = pickle.load(fh)
    for j, module in enumerate(mask):
        if module.count(False) == 0:
            continue
        print("Module %d: %d bad pixels" % (j, module.count(False)))
        print("Fast Slow Slow (within module)")
        shape = module.focus()
        sel = (~module).iselection()
        for pixel in sel:
            x = pixel % shape[1]
            y = pixel // shape[1]
            print("%4d %4d %4d" % (x, y + j * shape[0], y))


if __name__ == "__main__":
    import sys

    hot_pixel_mask_to_xy(sys.argv[1])
