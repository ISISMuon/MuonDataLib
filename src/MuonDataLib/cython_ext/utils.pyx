import cython
import numpy as np


def warning(msg):
    """
    A simple wrapper for a warning message
    that is printed to screen
    :msg: the message to print
    """
    print("WARNING:", msg)


@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cpdef binary_search(
                    double[:] values,
                    int start,
                    int stop,
                    double target):

    """
    A simple recursive binary search. The expectation is that
    values are sorted into ascending order. It returns the
    index of the left bounding bin for the target value.

    This method adds a simple check before the main calculation.
    :param values: The list of ordered time values to search against
    :param start: The lowest index to include in the search
    :param stop: The largest index to include in the search
    :param target: The value we want to search for
    :returns: The index of the left bounding bin of the target
    """
    if values[0] > target:
        warning(f'The target {target} is before the first frame {values[0]}. Difference is {values[0]-target}')


    elif values[len(values)-1] < target:
        i = len(values) - 1
        warning(f'The target {target} is after the last frame start time {values[i]}. Difference is {target-values[i]}')


    return _binary_search(values, start, stop, target)

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cpdef _binary_search(
                    double[:] values,
                    int start,
                    int stop,
                    double target):

    """
    A simple recursive binary search. The expectation is that
    values are sorted into ascending order. It returns the
    index of the left bounding bin for the target value.

    :param values: The list of ordered time values to search against
    :param start: The lowest index to include in the search
    :param stop: The largest index to include in the search
    :param target: The value we want to search for
    :returns: The index of the left bounding bin of the target
    """


    cdef int mid_point

    if stop - start == 1:
        return start

    elif stop > start:
        mid_point = start + (stop - start) //2

        if values[mid_point] == target:
            return mid_point

        elif values[mid_point] > target:
            return _binary_search(values, start, mid_point, target)

        else:
            return _binary_search(values, mid_point, stop, target)
    elif values[start] < target or values[stop] > target:
        return -1
    else:
        return stop
