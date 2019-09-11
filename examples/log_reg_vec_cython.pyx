# cython: wraparound=False
# cython: boundscheck=False
# cython: nonecheck=False
# cython: language_level=3str

import numpy as np
cimport numpy as np
import matplotlib.pyplot as plt

cdef np.ndarray[np.double_t, ndim=1] sigmoid(np.ndarray[np.double_t, ndim=1] x):
    return 1/(1 + np.exp(-x))

cdef np.ndarray[np.double_t, ndim=1] h(np.ndarray[np.double_t, ndim=2] X, np.ndarray[np.double_t, ndim=1] theta):
    cdef np.ndarray[np.double_t, ndim=1] z = np.dot(X, theta)
    return sigmoid(z)

cdef double cost_function(np.ndarray[np.double_t, ndim=2] X, np.ndarray[int, ndim=1] y, np.ndarray[np.double_t, ndim=1] theta):
    cdef int m = len(y)
    cdef np.ndarray[np.double_t, ndim=1] hx = h(X, theta)
    cdef double J = 1/(m) * np.sum(-y*np.log(hx) - (1-y)*np.log(1-hx), axis=0)
    return J

cdef np.ndarray[np.double_t, ndim=1] gradient(np.ndarray[np.double_t, ndim=2] X, np.ndarray[int, ndim=1] y, np.ndarray[np.double_t, ndim=1] theta):
    cdef int m = X.shape[0]
    return 1/m * (np.dot((h(X, theta)-y), X))

cdef tuple gradient_descent(np.ndarray[np.double_t, ndim=2] X, np.ndarray[int, ndim=1] y, np.ndarray[np.double_t, ndim=1] theta, double alpha, int iterations):
    cdef np.ndarray[long double, ndim=1] J_history = np.zeros(iterations)
    cdef int k
    for k in range(iterations):
        theta = theta - alpha * gradient(X, y, theta)
        J_history[k] = cost_function(X, y, theta)
    return theta, J_history

cpdef void func(np.ndarray[np.double_t, ndim=1] init_theta, np.ndarray[np.double_t, ndim=2] X, np.ndarray[int, ndim=1] Y, double alpha, int iters):
    print("Starting vectorized version [Cython]")
    t, _ = gradient_descent(X, Y, init_theta, alpha, iters)
    print(f"Evaluated theta: {t}")
    #print(f"Cost history: {cost_history}")
    #plot(X, Y, t)

def plot(X, Y, theta):
    print(theta)
    x1 = np.linspace(0, 6, 100)
    x2 = -theta[0]/theta[2] -theta[1]/theta[2]*x1

    mask = Y == 1
    _, ax = plt.subplots()
    ax.plot(X[mask][:,1], X[mask][:,2], 'o')
    ax.plot(X[~mask][:,1], X[~mask][:,2], 'o')
    ax.plot(x1, x2)
    ax.set_xlim(-0.1,6.1)
    ax.set_ylim(-0.1,6.1)
    plt.show()

cpdef void test(int number_of_points):
    X = np.random.random((number_of_points, 2))
    X = np.hstack((np.ones((number_of_points, 1)), X))
    Y = np.array([1 if a[2]>a[1] else 0 for a in X])
    _ ,n = X.shape
    alpha = 0.01
    iterations = 40000
    init_theta = np.ones(n)
    t, _ = gradient_descent(X, Y, init_theta, alpha, iterations)