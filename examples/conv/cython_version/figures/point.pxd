#cython: language_level=3str


cdef class Point:
    cdef public double x
    cdef public double y
    cdef public int n
    cpdef double distance(self, Point point=*)