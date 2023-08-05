from __future__ import absolute_import, division, print_function


def get_entry(filename, mode="a"):
    import h5py

    handle = h5py.File(filename, mode)
    if "entry" in handle:
        entry = handle["entry"]
        assert entry.attrs["NX_class"] == "NXentry"
    else:
        entry = handle.create_group("entry")
        entry.attrs["NX_class"] = "NXentry"
    return entry


def load(filename):
    from dials.util.nexus import nx_reflections, nx_mx

    entry = get_entry(filename, "r")
    ref, exp_index = nx_reflections.load(entry)
    exp = nx_mx.load(entry, exp_index)
    return exp, ref


def dump(experiments, reflections, filename):
    from dials.util.nexus import nx_reflections, nx_mx

    entry = get_entry(filename, "w")
    experiments = nx_mx.dump(entry, experiments)
    nx_reflections.dump(entry, reflections, experiments)
