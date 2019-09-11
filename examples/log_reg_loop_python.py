import numpy as np
from timeit import default_timer as timer
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1/(1 + np.exp(-x))

def h(X, theta):
    z = 0
    for j in range(len(theta)):
        z += X[j] * theta[j]
    return sigmoid(z)

def cost_function(X, y, theta):
    m = len(y)
    hx = np.zeros(m)
    for i in range(len(hx)):
        hx[i] = h(X[i], theta)
    J = 0
    for j in range(m):
        J += -y[j] * np.log(hx[j]) - (1-y[j]) * np.log(1-hx[j])
    J = J/m
    return J

def gradient(X, y, theta):
    m, n = X.shape
    derivatives = np.zeros(n)
    for j in range(n):
        for i in range(m):
            derivatives[j] += (h(theta, X[i,:]) - y[i]) * X[i][j]
    return derivatives/m

def gradient_descent(X, y, theta, alpha, iterations):
    J_history = np.zeros(iterations)
    for k in range(iterations):
        for i in range(len(theta)):
            theta[i] = theta[i] - alpha * gradient(X, y, theta)[i]
        J_history[k] = cost_function(X, y, theta)
    return theta, J_history

def func(init_theta, X, Y, alpha, iters, verify=False, draw=False):
    #print("Starting loop version [Python]")

    t, _ = gradient_descent(X, Y, init_theta, alpha, iters)

    #print(f"Evaluated theta: {t}")
    if verify:
        new_m = 10**6
        new_X = np.random.random((new_m, 2))
        new_X = np.hstack((np.ones((new_m, 1)), new_X))
        new_Y = np.array([1 if a[2]>a[1] else 0 for a in new_X])
        print(f"Correct predictions: {check_predictions(new_X, new_Y, t) * 100}%")
    if draw:
        plot(X, Y, t)

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

def check_predictions(X, Y, theta):
    results = np.around(h(X, theta))
    m = Y.shape[0]
    correct = np.sum(results == Y)
    return correct / m

def test(number_of_points):
    X = np.random.random((number_of_points, 2))
    X = np.hstack((np.ones((number_of_points, 1)), X))
    Y = np.array([1 if a[2]>a[1] else 0 for a in X])
    _ ,n = X.shape
    alpha = 0.01
    iterations = 40000
    init_theta = np.ones(n)
    func(init_theta, X, Y, alpha, iterations, verify=False, draw=False)

"""if __name__ == '__main__':
    #print("This module has to be imported")
    X = np.array([[2,2], [2,3], [3,2], [2,4], [3,3], [4,1], [4,4]])
    Y = np.array([0,0,0,1,1,1,1])
    init_theta = np.ones(X.shape[-1])

    cost_function(X, Y, init_theta)"""
