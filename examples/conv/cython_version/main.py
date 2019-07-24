from algorithms.convex_hull_objects import test as test_obj, profile_function as prof_obj
from algorithms.convex_hull_structs import test as test_st, profile_function as prof_st, timeit_turn_right
from algorithms.convex_hull_numpy import test as test_np, profile_function as prof_np
from algorithms.convex_hull_memoryview import test as test_mv, test_old as test_mv_old, profile_function as prof_mv
import numpy as np
import timeit

def timeit_tests():
    n_loops = 10**8

    setup_et = """from algorithms.convex_hull_structs import turn_right
from algorithms.convex_hull_structs cimport Point
p1 = Point(3.4, 6.7)
p2 = Point(0.0, 0.0)
p3 = Point(-2.0, 3.0)
"""
    py = timeit.timeit('turn_right(p1, p2, p3)', setup=setup_et, number=n_loops)
    print(f"Extension Types: {py}, per loop: {py / n_loops}")

    setup_np = """from algorithms.convex_hull_numpy import turn_right
import numpy as np
p1 = np.array([3.4, 6.7])
p2 = np.array([0.0, 0.0])
p3 = np.array([-2.0, 3.0])
"""
    cy = timeit.timeit('turn_right(p1, p2, p3)', setup=setup_np, number=n_loops)
    print(f"NumPy: {cy}, per loop: {cy / n_loops}")


if __name__ == '__main__':
    """for number_of_points in range(100, 1000, 50):
        for i in range(10):
            p_list = []
            for i in range(number_of_points):
                p_list.append([np.random.uniform(-10, 10), np.random.uniform(-10, 10)])
            test_obj(p_list, False)
            test_st(p_list, False)"""

    
    """factor = 10**5
    for k in range(1, 11):
        number_of_points = factor * k
        print(number_of_points)
        for _ in range(5):
            p_list = []
            for i in range(number_of_points):
                p_list.append([np.random.uniform(-10, 10), np.random.uniform(-10, 10)])
            test_mv_old(p_list, False)
            test_mv(p_list, False)"""
    number_of_points = 10**6
    p_list = []
    for i in range(number_of_points):
        p_list.append([np.random.uniform(-10, 10), np.random.uniform(-10, 10)])
    """
    test_obj(p_list, False)
    test_st(p_list, False)
    test_np(p_list, False)
    test_mv(p_list, False)

    number_of_points = 10**7
    p_list = []
    for i in range(number_of_points):
        p_list.append([np.random.uniform(-10, 10), np.random.uniform(-10, 10)])
    """
    # test_obj(p_list, False)
    # test_st(p_list, False)
    # test_np(p_list, False)
    # test_mv_old(p_list, False)
    # test_mv(p_list, False)
    # prof_obj(p_list)
    # prof_st(p_list)
    # prof_np(p_list)
    prof_mv(p_list)
    # timeit_tests()
    # timeit_turn_right()
