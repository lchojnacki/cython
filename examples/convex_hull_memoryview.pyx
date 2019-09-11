# cython: language_level=3str
# cython: profile=True
# cython: linetrace=True
# cython: binding=True

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
cimport numpy as np
import time
from timeit import default_timer as timer
from datetime import datetime
import line_profiler
from cython cimport boundscheck, wraparound


cpdef bint turn_right(p1, p2, p3):
    cdef:
        int zero = 0
        int one = 1
        int two = 2
    cdef double cross = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
    return cross > 0


cpdef list convex_hull_mv_old(double[:, :] points):
    cdef int number_of_points = points.shape[0]
    cdef list top_hull = [points[0], points[1]]
    cdef unsigned int i
    for i in range(2, number_of_points):
        top_hull.append(points[i])
        while len(top_hull) > 2 and \
        not turn_right(top_hull[-3], top_hull[-2], top_hull[-1]):
            del top_hull[-2]
    cdef list bottom_hull = [points[-1], points[-2]]
    for i in range(number_of_points-3, -1, -1):
        bottom_hull.append(points[i])
        while len(bottom_hull) > 2 and \
        not turn_right(bottom_hull[-3], bottom_hull[-2], bottom_hull[-1]):
            del bottom_hull[-2]
    del bottom_hull[0]
    del bottom_hull[-1]
    cdef list full_convex_hull = top_hull + bottom_hull

    return full_convex_hull


cpdef list convex_hull(double[:, :] points):
    cdef int number_of_points = points.shape[0]
    cdef list top_hull = [0, 1]
    cdef unsigned int i
    for i in range(2, number_of_points):
        top_hull.append(i)
        while len(top_hull) > 2 and \
        not (points[top_hull[-2]][0] - points[top_hull[-3]][0]) * (points[top_hull[-1]][1] - points[top_hull[-3]][1]) - (points[top_hull[-2]][1] - points[top_hull[-3]][1]) * (points[top_hull[-1]][0] - points[top_hull[-3]][0]) > 0:
            del top_hull[-2]
    cdef list bottom_hull = [number_of_points-1, number_of_points-2]
    for i in range(number_of_points-3, -1, -1):
        bottom_hull.append(i)
        while len(bottom_hull) > 2 and \
        not (points[bottom_hull[-2]][0] - points[bottom_hull[-3]][0]) * (points[bottom_hull[-1]][1] - points[bottom_hull[-3]][1]) - (points[bottom_hull[-2]][1] - points[bottom_hull[-3]][1]) * (points[bottom_hull[-1]][0] - points[bottom_hull[-3]][0]) > 0:
            del bottom_hull[-2]
    del bottom_hull[0]
    del bottom_hull[-1]
    cdef list full_convex_hull = top_hull + bottom_hull
    cdef list return_value = []
    for i in full_convex_hull:
        return_value.append(points[i])

    return return_value


cpdef void draw_convex_hull(np.ndarray points, list hull_points):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)

    cdef np.ndarray p = points.transpose()

    ax.plot(p[0], p[1], '.')

    lines = []
    for i in range(len(hull_points)):
        lines.append((hull_points[i - 1], hull_points[i]))

    if lines is not None:
        for line in lines:
            new_line = Line2D([line[0][0], line[1][0]], [line[0][1], line[1][1]], color='red')
            ax.add_line(new_line)
    plt.show()


cpdef void test(int number_of_points):
    cdef np.ndarray points = np.zeros((number_of_points, 2))
    cdef int i
    for i in range(number_of_points):
        points[i] = np.random.uniform(-10, 10), np.random.uniform(-10, 10)

    cdef np.ndarray p = points[points[:, 0].argsort()]
    cdef list hull_points = convex_hull(p)


cpdef void test_old(list p_list, bint draw = False):
    cdef int number_of_points = len(p_list)
    cdef np.ndarray points = np.zeros((number_of_points, 2))
    cdef int i
    for i in range(number_of_points):
        points[i][0] = p_list[i][0]
        points[i][1] = p_list[i][1]

    cdef float start = timer()
    cdef np.ndarray p = points[points[:, 0].argsort()]
    cdef list hull_points = convex_hull_mv_old(p)
    cdef float end = timer()

    print("Time of convex_hull function execution (MV OLD), " + str(number_of_points) + " points: " +
          str(end - start))

    file = open("../cython.log", 'a+')
    now = datetime.now()
    file.write(now.strftime("%Y-%m-%d %H:%M:%S") + "\tconvex_hull_mv\t" +
               str(number_of_points) + " points\t" +
               str(end - start) + "s\n")
    file.close()

    if draw != 0:
        draw_convex_hull(points, hull_points)


def profile_function(list p_list):
    cdef int number_of_points = len(p_list)
    cdef np.ndarray points = np.zeros((number_of_points, 2))
    cdef int i
    for i in range(number_of_points):
        points[i][0] = p_list[i][0]
        points[i][1] = p_list[i][1]
    
    cdef np.ndarray p = points[points[:, 0].argsort()]
    profile = line_profiler.LineProfiler(convex_hull)
    profile.runcall(convex_hull, p)
    now = datetime.now()
    file = open("../cython_profiler_mv_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt", 'w+')
    profile.print_stats(file)
    file.close()