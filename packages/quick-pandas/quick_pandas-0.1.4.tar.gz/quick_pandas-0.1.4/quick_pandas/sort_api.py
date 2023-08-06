import numpy as np

from quick_pandas import sort, config
# from quick_pandas.wrappers.numpy_wrapper import ndarray_wrapper
ndarray_wrapper = None


def radix_argsort(array, unicode=None):
    if getattr(array, '__actual_class__', None) == ndarray_wrapper:
        array = array.__wrapped_instance__
    if unicode is None:
        unicode = not config.ASCII_SORT
    return sort.radix_argsort(array, unicode=unicode)


def radix_sort(array):
    if getattr(array, '__actual_class__', None) == ndarray_wrapper:
        array = array.__wrapped_instance__
    return sort.radix_sort(array)


def init():
    radix_argsort(np.array([1], dtype=int))
    radix_sort(np.array([1], dtype=int))
