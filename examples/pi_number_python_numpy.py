from timeit import default_timer as timer
import line_profiler
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

def nilakantha_infinite_series(loops):
    value = 3.0
    i = np.arange(0, loops)
    value += np.sum((-1)**i * 1.0/((i+1)*(i+2)*(2*i+3)))
    return value

def profile(loops):
    profile = line_profiler.LineProfiler(nilakantha_infinite_series)
    profile.runcall(nilakantha_infinite_series, loops)
    now = datetime.now()
    file = open("./profile/pi_python_profile_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt", 'w+')
    profile.print_stats(file)
    file.close()

def test(loops):
    nilakantha_infinite_series(loops)

def plot_old():
    _, ax = plt.subplots(figsize=(9, 5))
    N = 300
    X = np.linspace(1, N, N, dtype=int)
    Y = np.array([nilakantha_infinite_series(x) for x in X])
    Y_pi = np.empty(N)
    Y_pi.fill(np.pi)
    ax.plot(X, Y, label="Szereg nieskończony Nilakanthy")
    ax.plot(X, Y_pi, label=f"pi = {np.pi}")
    ax.set_ylim(3.1415875, 3.141598)
    ax.set_xlim(0, N)
    ax.legend()
    ax.set_xlabel("Ilość zsumowanych wyrazów szeregu")
    ax.set_ylabel("Wartość liczbowa")
    ax.grid(True)
    plt.show()

def plot_new():
    _, ax = plt.subplots(figsize=(7, 4))
    N = 50
    X = np.linspace(1, N, N, dtype=int)
    Y = np.array([abs((np.pi - nilakantha_infinite_series(x))/np.pi) for x in X])
    ax.plot(X, Y, label=r"$\left|\dfrac{\pi - p}{\pi}\right|$")
    ax.legend(prop={'size': 10})
    ax.set_xlabel("Liczba zsumowanych wyrazów szeregu")
    ax.set_ylabel("Błąd względny przybliżenia liczby π")
    ax.grid(True)
    plt.show()

if __name__ == "__main__":
    """t = timer()
    approximate_pi(10000000)
    print(timer() - t)
    t = timer()
    approximate_pi(100000000)
    print(timer() - t)
    t = timer()
    approximate_pi(300000000)
    print(timer() - t)"""
    
    plot_new()
