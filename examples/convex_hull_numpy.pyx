# cython: language_level=3str

import numpy as np
cimport numpy as np


cpdef bint turn_right_np(p1, p2, p3):
    cdef double vec_p1_p2_1 = p2[0] - p1[0]
    cdef double vec_p1_p2_2 = p2[1] - p1[1]

    cdef double vec_p1_p3_1 = p3[0] - p1[0]
    cdef double vec_p1_p3_2 = p3[1] - p1[1]

    cdef double cross = vec_p1_p3_1 * vec_p1_p2_2 - vec_p1_p3_2 * vec_p1_p2_1

    return cross > 0


cpdef list convex_hull_np_array(np.ndarray p):
    points = p[p[:,0].argsort()]
    cdef int number_of_points = points.shape[0]
    cdef list top_hull = [(points[0][0], points[0][1]), (points[1][0], points[1][1])]
    cdef unsigned int i
    for i in range(2, number_of_points):
        top_hull.append((points[i][0], points[i][1]))
        while len(top_hull) > 2 and not turn_right_np(*top_hull[-3:]):
            del top_hull[-2]
    cdef list bottom_hull = [(points.item(number_of_points-1, 0), points.item(number_of_points-1, 1)),
                             (points.item(number_of_points-2, 0), points.item(number_of_points-2, 1))]
    for i in range(number_of_points-3, -1, -1):
        bottom_hull.append((points.item(i, 0), points.item(i, 1)))
        while len(bottom_hull) > 2 and not turn_right_np(*bottom_hull[-3:]):
            del bottom_hull[-2]
    del bottom_hull[0]
    del bottom_hull[-1]
    cdef list full_convex_hull = top_hull + bottom_hull

    return full_convex_hull


cpdef void test(int number_of_points):
    cdef np.ndarray points = np.zeros((number_of_points, 2), dtype=np.float64)
    cdef int i
    for i in range(number_of_points):
        points[i] = np.random.uniform(-10, 10), np.random.uniform(-10, 10)

    cdef list hull_points = convex_hull_np_array(points)