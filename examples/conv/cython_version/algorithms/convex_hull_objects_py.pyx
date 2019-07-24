# cython: language_level=3str
# cython: profile=True
# cython: linetrace=True
# cython: binding=True

cimport figures.point
from figures.point cimport Point
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import line_profiler
from datetime import datetime
from timeit import default_timer as timer


cpdef bint turn_right(Point p1, Point p2, Point p3):
    cdef double cross = (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
    return cross < 0


cdef double sort_key(Point p):
   return p.x


def convex_hull(points):
    points.sort(key=lambda p: p.x)
    number_of_points = len(points)
    top_hull = points[:2]
    for i in range(2, number_of_points):
        top_hull.append(points[i])
        while len(top_hull) > 2 and not turn_right(*top_hull[-3:]):
            del top_hull[-2]
    bottom_hull = [points[-1], points[-2]]
    for i in range(number_of_points-3, -1, -1):
        bottom_hull.append(points[i])
        while len(bottom_hull) > 2 and not turn_right(*bottom_hull[-3:]):
            del bottom_hull[-2]
    del bottom_hull[0]
    del bottom_hull[-1]
    full_convex_hull = top_hull + bottom_hull
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


cpdef void test(list p_list, bint draw=False):
    cdef int number_of_points = len(p_list)
    cdef list points = []
    cdef int i
    for i in range(number_of_points):
        points.append(Point(p_list[i][0], p_list[i][1]))
        #points.append(Point(np.random.uniform(-10, 10), np.random.uniform(-10, 10)))

    cdef float start = timer()
    cdef list hull_points = convex_hull(points)
    cdef float end = timer()

    print("Time of convex_hull function execution (objects), " + str(number_of_points) + " points: " +
        str(end - start) + "s")

    file = open("../cython.log", 'a+')
    now = datetime.now()
    file.write(now.strftime("%Y-%m-%d %H:%M:%S") + "\tconvex_hull_objects\t" +
                str(number_of_points) + " points\t" +
                str(end - start) + "s\n")
    file.close()
    if draw != 0:
        draw_convex_hull(points, hull_points)


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