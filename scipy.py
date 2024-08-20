import numpy as np
import time
from matplotlib import pyplot as plt
from scipy.integrate import quad

params = {
    "c": 1,
    "a": 2,
    "b": 5,
    "c": 7,
    "z": 4,
}

def integrand(x, **kwargs):
    y = 0
    for i, (k, v) in enumerate(sorted(params.items())[::-1]):
        y = y + (v * x**i) + np.sin(x)
    return y

def get_points_list(func, start=0, stop=1000, step=1, **kwargs):
    """
    func = integrand function
    **kwargs = items in 'params' list
    """
    x2 = []
    y2 = []
    while start <= stop:
        x2.append(start)
        y2.append(integrand(start, **kwargs))
        start += step
    return x2, y2

start = time.process_time()
I = quad(integrand, 0, 1000)
end = time.process_time()
total = end - start
comp_quad = {
    "time": total,
    "result": I[0],
}

print(comp_quad)
