import numpy as np
import time
from matplotlib import pyplot as plt
from tabulate import tabulate


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

def get_squares(xs, ys, step=1):
    coo = []
    for x, y in zip(xs, ys):
        x1 = x - step / 2
        x2 = x + step / 2
        y1 = y
        # y2 will be always 0, witch is why I didn't include it
        coo.append([x1, x2, y1])
    coo[0][0] += step / 2 # substracting half of step from the first 
    coo[-1][1] -= step / 2 # and last x because those are out of range
    return coo

def sum_area(cords, step=1):
    """This function sums the areas of all rectangles"""
    sum_area = 0
    for coo in cords:
        area = (abs(coo[1]) - abs(coo[0])) * abs(coo[2])
        sum_area += area
    return sum_area

def get_trapez(xs, ys, step=1):
    coo = []
    for x, y in zip(xs, ys):
        x1 = x - step / 2
        x2 = x + step / 2
        y1 = y
        coo.append([x1, x2, y1])
    coo[0][0] += step / 2
    coo[-1][1] -= step / 2
    return coo

def time_measure(get_coo_fun, sum_area_fun, step=1):
    start = time.process_time()

    x_list, y_list = get_points_list(func=integrand, step=step, **params)
    cords = get_coo_fun(x_list, y_list, step=step)
    result = sum_area_fun(cords, step=step)

    end = time.process_time()
    total = end - start
    return result, total


STEP = 1
results_square = []
result_time_square = []
step_list_square = []

""" Loop that will run functions 13 times 
    (reduces the step by half each time) """
for i in range(1, 14):
    step_list_square.append(STEP)
    res, tim = time_measure(get_squares, sum_area, step=STEP)
    results_square.append(res)
    result_time_square.append(tim)
    STEP *= 0.5

fig, ax = plt.subplots()

fig = plt.plot(result_time_square)

labels = [item.get_text() for item in ax.get_xticklabels()]

labels[::] = [round(step_list_square[i], 4) for i,
              v in enumerate(step_list_square)]

ax.set_xticklabels(labels)

plt.xlabel("Step")
plt.ylabel("Time [s]")
plt.grid(True)
plt.show()

comparison_sq = {
    "time": [tim for tim in result_time_square],
    "result": [res for res in results_square],
    "step": [step for step in step_list_square]
}

print(tabulate(comparison_sq, headers='keys', 
               disable_numparse=True, showindex=True))
