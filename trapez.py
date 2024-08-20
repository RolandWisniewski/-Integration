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

def sum_area_trapez(cords, step=1):
    """This function sums the areas of all trapezes"""
    sum_area = 0
    for i in range(len(cords)-1):
        area = ((abs(cords[i][2])+abs(cords[i+1][2])) * 
                (abs(cords[i][1]) - abs(cords[i][0]))) / 2
        sum_area += area
    return sum_area

def time_measure(get_coo_fun, sum_area_fun, step=1):
    start = time.process_time()

    x_list, y_list = get_points_list(func=integrand, step=step, **params)
    cords = get_coo_fun(x_list, y_list, step=step)
    result = sum_area_fun(cords, step=step)

    end = time.process_time()
    total = end - start
    return result, total


STEP = 1
results_trapez = []
result_time_trapez = []
step_list_trapez = []

""" Loop that will run functions 13 times 
    (reduces the step by half each time) """
for i in range(1, 14):
    step_list_trapez.append(STEP)
    res, tim = time_measure(get_trapez, sum_area_trapez, step=STEP)
    results_trapez.append(res)
    result_time_trapez.append(tim)
    STEP *= 0.5

fig, ax = plt.subplots()

fig = plt.plot(result_time_trapez)

labels = [item.get_text() for item in ax.get_xticklabels()]

labels[::] = [round(step_list_trapez[i], 4) for i,
              v in enumerate(step_list_trapez)]

ax.set_xticklabels(labels)

plt.xlabel("Step")
plt.ylabel("Time [s]")
plt.grid(True)
plt.show()

comparison_t = {
    "time": [tim for tim in result_time_trapez],
    "result": [res for res in results_trapez],
    "step": [step for step in step_list_trapez]
}

print(tabulate(comparison_t, headers='keys',
               disable_numparse=True, showindex=True))
