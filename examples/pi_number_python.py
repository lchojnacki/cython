from timeit import default_timer as timer
import line_profiler
from datetime import datetime

def approximate_pi(rank):
    value = 0
    for k in range(1, 2*rank+1, 2):
        sign = -(k % 4 - 2)
        value += float(sign) / k
    return 4 * value

def nilakantha_infinite_series(loops):
    value = 3.0
    for i in range(2, 2*loops+1, 2):
        sign = (i % 4 - 1)
        value += sign * 4.0/(i * (i+1) * (i+2))
    return value

def profile(loops):
    profile = line_profiler.LineProfiler(nilakantha_infinite_series)
    profile.runcall(nilakantha_infinite_series, loops)
    now = datetime.now()
    file = open("./profile/pi_python_profile_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt", 'w+')
    profile.print_stats(file)
    file.close()

def test(loops):
    pi = nilakantha_infinite_series(loops)

if __name__ == "__main__":
    t = timer()
    approximate_pi(10000000)
    print(timer() - t)
    t = timer()
    approximate_pi(100000000)
    print(timer() - t)
    t = timer()
    approximate_pi(300000000)
    print(timer() - t)
