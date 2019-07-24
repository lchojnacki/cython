#cython: language_level=3str
from libc.math cimport sqrt


cdef class Point:
    def __init__(self, double _x=0, double _y=0):
        self.x = _x
        self.y = _y
        self.n = 0

    def __gt__(self, Point other):
        # No need of __richcmp__: New from Cython 0.27
        return self.x > other.x if self.x != other.x else self.y > other.y

    def __lt__(self, Point other):
        # No need of __richcmp__: New from Cython 0.27
        return self.x < other.x if self.x != other.x else self.y < other.y

    def __eq__(self, Point other):
        # No need of __richcmp__: New from Cython 0.27
        return self.x == other.x and self.y == other.y

    def __iter__(self):
        return self

    def __next__(self):
        if self.n == 0:
            self.n += 1
            return self.x
        elif self.n == 1:
            self.n += 1
            return self.y
        else:
            raise StopIteration

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y

    cpdef double distance(self, Point point=None):
        """Calculates distance between two points.
        If no argument given, calculates distance from the origin of a Euclidean space."""
        if not isinstance(point, Point):
            point = Point()
        cdef double result = sqrt((point.x - self.x)**2 + (point.y - self.y)**2)
        return result
