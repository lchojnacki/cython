from convex_hull import Point
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from timeit import default_timer as timer
from datetime import datetime
import line_profiler


def turn_right(p1, p2, p3):
    vec_p1_p2_1 = p2[0] - p1[0]
    vec_p1_p2_2 = p2[1] - p1[1]

    vec_p1_p3_1 = p3[0] - p1[0]
    vec_p1_p3_2 = p3[1] - p1[1]

    cross = vec_p1_p3_1 * vec_p1_p2_2 - vec_p1_p3_2 * vec_p1_p2_1

    return cross > 0


def turn_right_np(p1, p2, p3):

    cross = np.cross((p2[0] - p1[0], p2[1] - p1[1], 0), (p3[0] - p1[0], p3[1] - p1[1], 0))

    return cross[2] < 0


def convex_hull_np_array(p):
    points = p[p[:,0].argsort()]
    number_of_points = points.shape[0]
    top_hull = [(points[0][0], points[0][1]), (points[1][0], points[1][1])]
    for i in range(2, number_of_points):
        top_hull.append((points[i][0], points[i][1]))
        # while len(top_hull) > 2 and not turn_right_np(top_hull[-3:]):
        while len(top_hull) > 2 and not turn_right(top_hull[-3], top_hull[-2], top_hull[-1]):
            del top_hull[-2]
    bottom_hull = [(points.item(number_of_points-1, 0), points.item(number_of_points-1, 1)),
                             (points.item(number_of_points-2, 0), points.item(number_of_points-2, 1))]
    for i in range(number_of_points-3, -1, -1):
        bottom_hull.append((points.item(i, 0), points.item(i, 1)))
        while len(bottom_hull) > 2 and not turn_right(bottom_hull[-3], bottom_hull[-2], bottom_hull[-1]):
            del bottom_hull[-2]
    del bottom_hull[0]
    del bottom_hull[-1]
    full_convex_hull = top_hull + bottom_hull

    return full_convex_hull


def draw_np(points, lines):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)

    p = points.transpose()

    ax.plot(p[0], p[1], '.')

    if lines is not None:
        for line in lines:
            new_line = Line2D([line.p1.x, line.p2.x], [line.p1.y, line.p2.y], color='red')
            ax.add_line(new_line)
    plt.show()


def test(number_of_points):
    points = np.zeros((number_of_points, 2), dtype=np.float64)
    for i in range(number_of_points):
        points[i] = np.random.uniform(-10, 10), np.random.uniform(-10, 10)

    hull_points = convex_hull_np_array(points)


def profile_function_np(number_of_points):
    points = np.zeros((number_of_points, 2), dtype=np.float64)
    for i in range(number_of_points):
        points[i] = np.random.uniform(-10, 10), np.random.uniform(-10, 10)

    profile = line_profiler.LineProfiler(convex_hull_np_array)
    profile.runcall(convex_hull_np_array, points)
    now = datetime.now()
    file = open("../cython_profiler_np_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt", 'w+')
    profile.print_stats(file)
    file.close()