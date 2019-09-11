# cython: language_level=3str
# cython: profile=True
# cython: linetrace=True
# cython: binding=True
# cython: boundscheck=False

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import line_profiler
from datetime import datetime
from timeit import default_timer as timer
from libc.stdlib cimport malloc, free, qsort


ctypedef struct Point:
    double x, y


cpdef bint turn_right(Point p1, Point p2, Point p3):
    cdef double cross = (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
    return cross < 0


cdef int int_compare(const void *a, const void *b) nogil:
    cdef double x1, x2
    x1 = (<Point*>a).x
    x2 = (<Point*>b).x
    if x1 < x2:
        return -1
    elif x1 > x2:
        return 1
    else:
        return 0
        

cdef list convex_hull(Point *points, int number_of_points):
    qsort(<void*>points, <size_t>number_of_points, sizeof(Point), int_compare)
    cdef list top_hull = [points[0], points[1]]
    cdef int i
    for i in range(2, number_of_points):
        top_hull.append(points[i])
        while len(top_hull) > 2 and not turn_right(*top_hull[-3:]):
                del top_hull[-2]
    cdef list bottom_hull = [points[number_of_points-1], points[number_of_points-2]]
    for i in range(number_of_points-3, -1, -1):
        bottom_hull.append(points[i])
        while len(bottom_hull) > 2 and not turn_right(*bottom_hull[-3:]):
                del bottom_hull[-2]
    del bottom_hull[0]
    del bottom_hull[-1]
    cdef list full_convex_hull = top_hull + bottom_hull
    return full_convex_hull


cdef void draw_convex_hull(Point *points, list hull_points, int number_of_points):
    _, ax = plt.subplots()
    ax.grid(True)
    cdef list X = [points[i].x for i in range(number_of_points)]
    cdef list Y = [points[i].y for i in range(number_of_points)]
    ax.plot(X, Y, '.')
    """for i in range(len(hull_points)):
        new_line = Line2D([hull_points[i-1]['x'], hull_points[i]['x']], [hull_points[i-1]['y'], hull_points[i]['y']], color='red')
        ax.add_line(new_line)"""
    lines = []
    for i in range(len(hull_points)):
        lines.append((hull_points[i - 1], hull_points[i]))
    if lines is not None:
        for line in lines:
            new_line = Line2D([line[0]['x'], line[1]['x']], [line[0]['y'], line[1]['y']], color='red')
            ax.add_line(new_line)
    plt.show()


cpdef void test(int number_of_points):
    cdef Point *points = <Point*>malloc(number_of_points * sizeof(Point))
    cdef int i
    for i in range(number_of_points):
        points[i] = Point(np.random.uniform(-10, 10), np.random.uniform(-10, 10))

    cdef list hull_points = convex_hull(points, number_of_points)
    
    free(points)


def profile_function(number_of_points):
    """cdef int number_of_points = len(p_list)
    cdef Point *points = <Point*>malloc(number_of_points * sizeof(Point))
    cdef int i
    for i in range(number_of_points):
        points[i] = Point(p_list[i][0], p_list[i][1])

    profile = line_profiler.LineProfiler(convex_hull)
    profile.runcall(convex_hull, points, number_of_points)
    now = datetime.now()
    file = open("../cython_profiler_structs_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt", 'w+')
    profile.print_stats(file)
    file.close()"""


def timeit_turn_right():
    p1 = Point(3.4, 6.7)
    p2 = Point(0.0, 0.0)
    p3 = Point(-2.0, 3.0)
    start = timer()
    for _ in range(10**8):
        turn_right(p1, p2, p3)
    t = timer() - start
    print(f"{t}, per loop: {t/10**8}")