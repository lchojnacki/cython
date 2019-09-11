# cython: cdivision=True
# cython: wraparound=False
# cython: boundscheck=False
# cython: language_level=3str

import numpy as np
cimport numpy as np
import matplotlib.pyplot as plt
from libc.math cimport exp as c_exp
from libc.math cimport log as c_log

cdef double sigmoid(double x):
    return 1/(1 + c_exp(-x))

cdef double h(double[:] X, double[:] theta):
    cdef double z = 0.
    cdef unsigned int j
    cdef unsigned int m = theta.shape[0]
    for j in range(m):
        z += X[j] * theta[j]
    return sigmoid(z)

cdef double cost_function(double[:,:] X, int[:] y, double[:] theta):
    cdef unsigned int m = y.shape[0]
    cdef np.ndarray[double, ndim=1] hx = np.zeros(m)
    cdef unsigned int i, j
    for i in range(m):
        hx[i] = h(X[i], theta)
    cdef double J = 0
    for j in range(m):
        J += -y[j] * c_log(hx[j]) - (1-y[j]) * c_log(1-hx[j])
    J = J/m
    return J

cdef np.ndarray gradient(double[:,:] X, int[:] y, double[:] theta):
    cdef unsigned int m = X.shape[0]
    cdef unsigned int n = X.shape[1]
    cdef np.ndarray[double, ndim=1] derivatives = np.zeros(n)
    cdef unsigned int i, j
    for j in range(n):
        for i in range(m):
            derivatives[j] += (h(X[i], theta) - y[i]) * X[i,j]
    return derivatives/m

cdef tuple gradient_descent(double[:,:] X, int[:] y, double[:] theta, double alpha, int iterations):
    cdef unsigned int n = X.shape[1]
    cdef np.ndarray[dtype=double, ndim=1] J_history = np.zeros(iterations)
    cdef unsigned int k, i
    cdef np.ndarray[double, ndim=1] grad
    for k in range(iterations):
        grad = gradient(X, y, theta)
        for i in range(n):
            theta[i] = theta[i] - alpha * grad[i]
        J_history[k] = cost_function(X, y, theta)
    return theta, J_history

cpdef void func(double[:] init_theta, double[:,:] X, int[:] Y, double alpha, int iters):
    print("Starting loop version [Cython]")
    #cdef np.ndarray t
    t, _ = gradient_descent(X, Y, init_theta, alpha, iters)

    print("Evaluated theta: [", end="")
    print(*t, sep=', ', end="")
    print("]")
    #plot(X, Y, t)

def plot(X, Y, theta):
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