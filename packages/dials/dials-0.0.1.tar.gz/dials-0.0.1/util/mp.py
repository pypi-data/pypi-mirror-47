from __future__ import absolute_import, division, print_function


def parallel_map(
    func,
    iterable,
    processes=1,
    nslots=1,
    method=None,
    asynchronous=True,
    callback=None,
    preserve_order=True,
    preserve_exception_message=True,
    job_category="low",
):
    """
    A wrapper function to call either drmaa or easy_mp to do a parallel map
    calculation. This function is setup so that in each case we can select
    the number of cores on a machine

    """
    from dials.util.cluster_map import cluster_map as drmaa_parallel_map
    from libtbx.easy_mp import parallel_map as easy_mp_parallel_map

    if method == "drmaa":
        return drmaa_parallel_map(
            func=func,
            iterable=iterable,
            callback=callback,
            nslots=nslots,
            njobs=processes,
            job_category=job_category,
        )
    else:
        qsub_command = "qsub -pe smp %d" % nslots
        return easy_mp_parallel_map(
            func=func,
            iterable=iterable,
            callback=callback,
            method=method,
            processes=processes,
            qsub_command=qsub_command,
            asynchronous=asynchronous,
            preserve_order=preserve_order,
            preserve_exception_message=preserve_exception_message,
        )


class MultiNodeClusterFunction(object):
    """
    A function called by the multi node parallel map. On each cluster node, a
    nested parallel map using the multi processing method will be used.

    """

    def __init__(
        self,
        func,
        nproc=1,
        asynchronous=True,
        preserve_order=True,
        preserve_exception_message=True,
    ):
        """
        Init the function

        """
        self.func = func
        self.nproc = nproc
        self.asynchronous = asynchronous
        self.preserve_order = (preserve_order,)
        self.preserve_exception_message = preserve_exception_message

    def __call__(self, iterable):
        """
        Call the function

        """
        from libtbx.easy_mp import parallel_map as easy_mp_parallel_map

        return easy_mp_parallel_map(
            func=self.func,
            iterable=iterable,
            processes=self.nproc,
            method="multiprocessing",
            asynchronous=self.asynchronous,
            preserve_order=self.preserve_order,
            preserve_exception_message=self.preserve_exception_message,
        )


def iterable_grouper(iterable, n):
    """
    Group the iterables

    """
    from itertools import izip_longest

    args = [iter(iterable)] * n
    for group in izip_longest(*args):
        group = tuple(item for item in group if item is not None)
        yield group


class MultiNodeClusterCallback(object):
    """
    A callback function used with the multi node parallel map

    """

    def __init__(self, callback):
        """
        Init the callback

        """
        self.callback = callback

    def __call__(self, x):
        """
        Call the callback

        """
        for item in x:
            self.callback(item)


def multi_node_parallel_map(
    func,
    iterable,
    njobs=1,
    nproc=1,
    cluster_method=None,
    asynchronous=True,
    callback=None,
    preserve_order=True,
    preserve_exception_message=True,
):
    """
    A wrapper function to call a function using multiple cluster nodes and with
    multiple processors on each node

    """

    # The function to all on the cluster
    cluster_func = MultiNodeClusterFunction(
        func=func,
        nproc=nproc,
        asynchronous=asynchronous,
        preserve_order=preserve_order,
        preserve_exception_message=preserve_exception_message,
    )

    # Create the cluster iterable
    cluster_iterable = iterable_grouper(iterable, nproc)

    # Create the cluster callback
    if callback is not None:
        cluster_callback = MultiNodeClusterCallback(callback)
    else:
        cluster_callback = None

    # Do the parallel map on the cluster
    result = parallel_map(
        func=cluster_func,
        iterable=cluster_iterable,
        callback=cluster_callback,
        method=cluster_method,
        nslots=nproc,
        processes=njobs,
        asynchronous=asynchronous,
        preserve_order=preserve_order,
        preserve_exception_message=preserve_exception_message,
    )

    # return result
    return [item for rlist in result for item in rlist]


class BatchFunc(object):
    """
    Process the batch iterables

    """

    def __init__(self, func):
        self.func = func

    def __call__(self, index):
        result = []
        for i in index:
            result.append(self.func(i))
        return result


class BatchIterable(object):
    """
    Split the iterables into batches

    """

    def __init__(self, iterable, chunksize):
        self.iterable = iterable
        self.chunksize = chunksize

    def __iter__(self):
        i = 0
        while i < len(self.iterable):
            j = i + self.chunksize
            yield self.iterable[i:j]
            i = j


class BatchCallback(object):
    """
    Process the batch callback

    """

    def __init__(self, callback):
        self.callback = callback

    def __call__(self, result):
        for r in result:
            self.callback(r)


def batch_parallel_map(
    func=None, iterable=None, processes=None, callback=None, method=None, chunksize=1
):
    """
    A function to run jobs in batches in each process

    """
    from libtbx import easy_mp

    # Call the batches in parallel
    return easy_mp.parallel_map(
        func=BatchFunc(func),
        iterable=BatchIterable(iterable, chunksize),
        processes=processes,
        callback=BatchCallback(callback),
        method=method,
        preserve_order=True,
        preserve_exception_message=True,
    )


def batch_multi_node_parallel_map(
    func=None,
    iterable=None,
    nproc=1,
    njobs=1,
    callback=None,
    cluster_method=None,
    chunksize=1,
):
    """
    A function to run jobs in batches in each process

    """
    from libtbx import easy_mp

    # Call the batches in parallel
    return multi_node_parallel_map(
        func=BatchFunc(func),
        iterable=BatchIterable(iterable, chunksize),
        nproc=nproc,
        njobs=njobs,
        cluster_method=cluster_method,
        callback=BatchCallback(callback),
        preserve_order=True,
        preserve_exception_message=True,
    )


if __name__ == "__main__":

    def func(x):
        return x

    iterable = range(100)

    multi_node_parallel_map(
        func,
        iterable,
        nproc=4,
        njobs=10,
        cluster_method="multiprocessing",
        callback=print,
    )
