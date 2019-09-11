# cython: cdivision=True

cimport numpy as cnp
import numpy as np

cpdef long double nilakantha_infinite_series(long long loops):
    cdef long double value = 3.0
    cdef cnp.ndarray i = np.arange(0, loops)
    value += np.sum((-1)**i * 1.0/((i+1)*(i+2)*(2*i+3)))
    return value

def test(loops):
    pi = nilakantha_infinite_series(loops)