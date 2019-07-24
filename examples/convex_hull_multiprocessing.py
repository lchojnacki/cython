from figures.point import Point
from figures.line import Line
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import time
from datetime import datetime
import line_profiler
import multiprocessing


def turn_right(p1, p2, p3):
    line = Line(p1, p2)
    return line.position_of_point(p3) > 0


def hull(points, queue, top=True):
    if top:
        hull_part = points[:2]
        for i in range(2, len(points)):
            hull_part.append(points[i])
            while len(hull_part) > 2 and not turn_right(*hull_part[-3:]):
                del hull_part[-2]
        queue.put(hull_part)
    else:
        hull_part = [points[-1], points[-2]]
        for i in range(len(points)-3, -1, -1):
            hull_part.append(points[i])
            while len(hull_part) > 2 and not turn_right(*hull_part[-3:]):
                del hull_part[-2]
        del hull_part[0]
        del hull_part[-1]
        queue.put(hull_part)


def convex_hull(points):
    queue = multiprocessing.Queue()
    points.sort()

    top_hull = multiprocessing.Process(target=hull, args=(points, queue, True))
    bottom_hull = multiprocessing.Process(target=hull, args=(points, queue, False))
    top_hull.start()
    bottom_hull.start()
    top_hull.join()
    bottom_hull.join()

    full_convex_hull = queue.get()
    full_convex_hull += queue.get()
    return full_convex_hull


def test(number_of_points):
    points = []
    for i in range(number_of_points):
        points.append(Point(np.random.uniform(-10, 10), np.random.uniform(-10, 10)))

    start = time.time()
    convex_hull(points)
    end = time.time()

    print("Convex Hull (multiprocessing); " + str(number_of_points) + " points: " +
          str(end - start) + "s")