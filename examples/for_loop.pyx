# cython: language_level=3str
# cython: boundscheck=False

import numpy as np
cimport numpy as np

cpdef void test(int n):
    cdef list my_list = []
    cdef unsigned int i
    for i in range(n):
        my_list.append(i**2)
        my_list.append(i**4)
        my_list.append(i**8)
