# cython: language_level=3str
# cython: profile=True
# cython: linetrace=True
# cython: binding=True

#cimport figures.point
#from figures.point cimport Point
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import line_profiler
from datetime import datetime
from timeit import default_timer as timer


from libc.math cimport sqrt


cdef class Point:
    cdef public double x, y
    cdef public int n
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



cpdef bint turn_right(Point p1, Point p2, Point p3):
    cdef double cross = (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
    return cross < 0


cdef double sort_key(Point p):
   return p.x


cpdef list convex_hull(list points):
    points.sort(key=sort_key)
    cdef int number_of_points = len(points)
    cdef list top_hull = points[:2]
    cdef int i
    for i in range(2, number_of_points):
        top_hull.append(points[i])
        while len(top_hull) > 2 and \
        not turn_right(*top_hull[-3:]):
            del top_hull[-2]
    cdef list bottom_hull = [points[-1], points[-2]]
    for i in range(number_of_points-3, -1, -1):
        bottom_hull.append(points[i])
        while len(bottom_hull) > 2 and \
        not turn_right(*bottom_hull[-3:]):
            del bottom_hull[-2]
    del bottom_hull[0]
    del bottom_hull[-1]
    cdef list full_convex_hull = top_hull + bottom_hull
    return full_convex_hull


cpdef void draw_convex_hull(list points, list hull_points):
    _, ax = plt.subplots()
    ax.grid(True)
    cdef list p = list(map(list, zip(*points)))
    ax.plot(p[0], p[1], '.')
    lines = []
    for i in range(len(hull_points)):
        lines.append((hull_points[i - 1], hull_points[i]))
    if lines is not None:
        for line in lines:
            new_line = Line2D([line[0].x, line[1].x], [line[0].y, line[1].y], color='red')
            ax.add_line(new_line)
    plt.show()


cpdef void test(int number_of_points):
    cdef list points = []
    cdef int i
    for i in range(number_of_points):
        points.append(Point(np.random.uniform(-10, 10), np.random.uniform(-10, 10)))

    cdef list hull_points = convex_hull(points)


def profile_function(list p_list):
    cdef int number_of_points = len(p_list)
    cdef list points = []
    cdef int i
    for i in range(number_of_points):
        points.append(Point(p_list[i][0], p_list[i][1]))

    profile = line_profiler.LineProfiler(convex_hull)
    profile.runcall(convex_hull, points)
    now = datetime.now()
    file = open("../cython_profiler_obj_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt", 'w+')
    profile.print_stats(file)
    file.close()