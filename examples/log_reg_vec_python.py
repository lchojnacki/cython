import numpy as np
from timeit import default_timer as timer
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1/(1 + np.exp(-x))

def h(X, theta):
    z = X @ theta
    return sigmoid(z)

def cost_function(X, y, theta):
    m = len(y)
    hx = h(X, theta)
    J = 1/(m) * np.sum(-y*np.log(hx) - (1-y)*np.log(1-hx), axis=0)
    return J

def gradient(X, y, theta):
    m, _ = X.shape
    return 1/m * ((h(X, theta)-y) @ X)

def gradient_descent(X, y, theta, alpha, iterations):
    J_history = np.zeros(iterations)
    for k in range(iterations):
        theta = theta - alpha * gradient(X, y, theta)
        J_history[k] = cost_function(X, y, theta)
    return theta, J_history

def func(init_theta, X, Y, alpha, iters, verify=False, draw=False):
    #print("Starting vectorized version [Python]")
    t, _ = gradient_descent(X, Y, init_theta, alpha, iters)
    #print(f"Evaluated theta: {t}")
    if verify:
        print(f"Correct predictions: {check_predictions(X, Y, t) * 100}%")
        new_m = 10**6
        new_X = np.random.random((new_m, 2))
        new_X = np.hstack((np.ones((new_m, 1)), new_X))
        new_Y = np.array([1 if a[2]>a[1] else 0 for a in new_X])
        print(f"Correct predictions: {check_predictions(new_X, new_Y, t) * 100}%")
    if draw:
        plot(X, Y, t)

def plot(X, Y, theta):
    print(theta)
    x1 = np.linspace(np.min(X[:,1]) - 0.2, np.max(X[:,1]) + 0.2, 100)
    x2 = -theta[0]/theta[2] -theta[1]/theta[2]*x1

    mask = Y == 1
    _, ax = plt.subplots()
    ax.plot(X[mask][:,1], X[mask][:,2], 'o')
    ax.plot(X[~mask][:,1], X[~mask][:,2], 'o')
    ax.plot(x1, x2)
    ax.set_xlim(np.min(X[:,1]) - 0.2, np.max(X[:,1]) + 0.2)
    ax.set_ylim(np.min(X[:,2]) - 0.2, np.max(X[:,2]) + 0.2)
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
    m = 10
    X = np.random.random((m, 2))
    X = np.hstack((np.ones((m, 1)), X))
    Y = np.array([1 if a[2]>a[1] else 0 for a in X])
    _ ,n = X.shape
    alpha = 0.01
    iterations = 400000
    init_theta = np.ones(n)
    func(init_theta, X, Y, alpha, iterations, verify=True, draw=True)
"""