import random
from math import sqrt
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import time
from datetime import datetime
import line_profiler


class Point:
    def __init__(self, _x=0, _y=0):
        self.x = _x
        self.y = _y

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"

    def __repr__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"

    def __gt__(self, other):
        return self.x > other.x if self.x != other.x else self.y > other.y

    def __lt__(self, other):
        return self.x < other.x if self.x != other.x else self.y < other.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def distance(self, point=None):
        """
        Calculates distance between two points.
        If no argument given, calculates distance from the origin of a Euclidean space.
        :param point: point to calculate distance with.
        :return: distance between self and given point OR the origin of Euclidean space.
        """
        if not isinstance(point, Point):
            point = Point()
        result = sqrt((point.x - self.x)**2 + (point.y - self.y)**2)
        return result

    def draw(self):
        plt.plot(self.x, self.y, 'o')
        plt.grid(True)
        plt.show()
		
		
		
class Line:
    def __init__(self, _p1, _p2):
        self.p1 = _p1
        self.p2 = _p2

    def position_of_point(self, point):
        """
        Returns position of point:
        - negative if point is on the left side of the line
        - 0 if point is on the line
        - positive if point is on the right side of the line
        :param point:
        :return: 0 or positive/negative number
        """
        vec_p1_p2_1 = self.p2.x - self.p1.x
        vec_p1_p2_2 = self.p2.y - self.p1.y

        vec_p1_point_1 = point.x - self.p1.x
        vec_p1_point_2 = point.y - self.p1.y

        cross = vec_p1_point_1 * vec_p1_p2_2 - vec_p1_point_2 * vec_p1_p2_1

        return cross

    def draw(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        new_line = Line2D([self.p1.x, self.p2.x], [self.p1.y, self.p2.y])
        ax.add_line(new_line)
        ax.grid(True)
        plt.show()


def turn_left(p1, p2, p3):
    line = Line(p1, p2)
    return line.position_of_point(p3) < 0


def turn_right(p1, p2, p3):
    line = Line(p1, p2)
    return line.position_of_point(p3) > 0


def turn_right_np(p1, p2, p3):
    vec_p1_p2_1 = p2[0] - p1[0]
    vec_p1_p2_2 = p2[1] - p1[1]

    vec_p1_p3_1 = p3[0] - p1[0]
    vec_p1_p3_2 = p3[1] - p1[1]

    cross = vec_p1_p3_1 * vec_p1_p2_2 - vec_p1_p3_2 * vec_p1_p2_1

    return cross > 0


def convex_hull(points):
    points.sort()
    top_hull = points[:2]
    for i in range(2, len(points)):
        top_hull.append(points[i])
        while len(top_hull) > 2 and not turn_right(*top_hull[-3:]):
            del top_hull[-2]
    bottom_hull = [points[-1], points[-2]]
    for i in range(len(points)-3, -1, -1):
        bottom_hull.append(points[i])
        while len(bottom_hull) > 2 and not turn_right(*bottom_hull[-3:]):
            del bottom_hull[-2]
    del bottom_hull[0]
    del bottom_hull[-1]
    full_convex_hull = top_hull + bottom_hull
    return full_convex_hull


def convex_hull_numpy(p):
    points = p[p[:, 0].argsort()]
    number_of_points = points.shape[0]
    top_hull = [(points.item(0, 0), points.item(0, 1)), (points.item(1, 0), points.item(1, 1))]
    for i in range(2, number_of_points):
        top_hull.append((points.item(i, 0), points.item(i, 1)))
        while len(top_hull) > 2 and not turn_right_np(*top_hull[-3:]):
            del top_hull[-2]

    bottom_hull = [(points.item(number_of_points-1, 0), points.item(number_of_points-1, 1)),
                   (points.item(number_of_points-2, 0), points.item(number_of_points-2, 1))]
    for i in range(number_of_points - 3, -1, -1):
        bottom_hull.append((points.item(i, 0), points.item(i, 1)))
        while len(bottom_hull) > 2 and not turn_right_np(*bottom_hull[-3:]):
            del bottom_hull[-2]
    del bottom_hull[0]
    del bottom_hull[-1]
    full_convex_hull = top_hull + bottom_hull
    return full_convex_hull


def draw_convex_hull(points, lines):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    points_xy = np.zeros((2, len(points)))
    for i in range(len(points)):
        points_xy[0][i] = points[i].x
        points_xy[1][i] = points[i].y
    ax.plot(points_xy[0], points_xy[1], '.')
    for line in lines:
        new_line = Line2D([line.p1.x, line.p2.x], [line.p1.y, line.p2.y], color='red')
        ax.add_line(new_line)
    plt.show()


def test(number_of_points):
    points = []
    for i in range(number_of_points):
        points.append(Point(np.random.uniform(-10, 10), np.random.uniform(-10, 10)))

    hull_points = convex_hull(points)


def convex_hull_test_np(number_of_points):
    points = np.random.uniform(-10, 10, (10, 2))

    start = time.time()
    hull_points = convex_hull_numpy(points)
    end = time.time()

    print("Time of convex_hull_numpy function execution, " + str(number_of_points) + " points: " +
          str(end - start) + "s")

    file = open("../python.log", 'a+')
    now = datetime.now()
    file.write(now.strftime("%Y-%m-%d %H:%M:%S") + "\tconvex_hull_numpy\t" +
               str(number_of_points) + " points\t" +
               str(end - start) + "s\n")
    file.close()


def profile_function(number_of_points):
    points = []
    for i in range(number_of_points):
        points.append(Point(np.random.uniform(-10, 10), np.random.uniform(-10, 10)))

    profile = line_profiler.LineProfiler(convex_hull)
    profile.runcall(convex_hull, points)
    now = datetime.now()
    file = open("../python_profiler_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt", 'w+')
    profile.print_stats(file)
    file.close()


def profile_function_np(number_of_points):
    points = np.zeros((number_of_points, 2), dtype=np.float64)
    for i in range(number_of_points):
        points[i] = np.random.uniform(-10, 10), np.random.uniform(-10, 10)

    profile = line_profiler.LineProfiler(convex_hull_numpy)
    profile.runcall(convex_hull_numpy, points)
    now = datetime.now()
    file = open("../python_profiler_np_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt", 'w+')
    profile.print_stats(file)
    file.close()
