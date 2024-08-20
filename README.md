# Integration

Comparison of different integration methods in Python

# Description

In mathematics, a [Riemann sum](https://en.wikipedia.org/wiki/Riemann_sum) is a certain kind of approximation of an integral by a finite sum. It is named after nineteenth century German mathematician Bernhard Riemann. One very common application is in numerical integration, i.e., approximating the area of functions or lines on a graph, where it is also known as the rectangle rule. It can also be applied for approximating the length of curves and other approximations.

The sum is calculated by partitioning the region into shapes (rectangles, trapezoids, parabolas, or cubics - sometimes infinitesimally small) that together form a region that is similar to the region being measured, then calculating the area for each of these shapes, and finally adding all of these small areas together. This approach can be used to find a numerical approximation for a definite integral even if the fundamental theorem of calculus does not make it easy to find a closed-form solution.

Because the region by the small shapes is usually not exactly the same shape as the region being measured, the Riemann sum will differ from the area being measured. This error can be reduced by dividing up the region more finely, using smaller and smaller shapes. As the shapes get smaller and smaller, the sum approaches the Riemann integral.

# Getting Started

Libraries used:
- [numpy](https://numpy.org/)
- [time](https://docs.python.org/3/library/time.html)
- [pyplot](https://matplotlib.org/stable/tutorials/pyplot.html) from [matplotlib](https://matplotlib.org/)
- [tabulate](https://pypi.org/project/tabulate/)
- `quad` form [scipy.integrate](https://docs.scipy.org/doc/scipy/tutorial/integrate.html)

# Executing program

First you need to import the libraries you need at this point:

```python
import numpy as np
import time
```

Then you need a few variables. You can enter any keys and values:

```python
params = {
    "c": 1,
    "a": 2,
    "b": 5,
    "c": 7,
    "z": 4,
}
```

You also need a function that will create a mathematical operation depending on the previous values ​​​​added to 'params' dict:

```python
def integrand(x, **kwargs):
    y = 0
    for i, (k, v) in enumerate(sorted(params.items())[::-1]):
        y = y + (v * x**i) + np.sin(x)
    return y
```

And a function that will automatically create two lists with points x and y:

```python
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
``` 

To integrate in Python, you could use ready-made functions such as `quad` from the [scipy.integrate](https://docs.scipy.org/doc/scipy/tutorial/integrate.html) sub-package:

```python
from scipy.integrate import quad

start = time.process_time()
I = quad(integrand, 0, 1000)
end = time.process_time()
total = end - start
comp_quad = {
    "time": total,
    "result": I[0],
}

print(comp_quad)
```
Output:

`{'time': 0.005239291999998841, 'result': 501670170391.79364}`

This method is relatively fast and the result is sufficiently accurate.

However, we will create our own functions and calculate integrals using the `square method` and the `trapezoidal method`, and we will also compare the accuracies and times of these methods.


# Square Method

The square method works by approximating the area under the graph of the function as rectangles and calculating their area.

The following functions creates the coordinates of these rectangles:

```python
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
```


```python
def sum_area(cords, step=1):
    """This function sums the areas of all rectangles"""
    sum_area = 0
    for coo in cords:
        area = (abs(coo[1]) - abs(coo[0])) * abs(coo[2])
        sum_area += area
    return sum_area
```

# Trapezoidal Method

Identical to the square method, with the difference that in this case we are dealing with trapezoids:

```python
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
```

```python
def sum_area_trapez(cords, step=1):
    """This function sums the areas of all trapezes"""
    sum_area = 0
    for i in range(len(cords)-1):
        area = ((abs(cords[i][2])+abs(cords[i+1][2])) * 
                (abs(cords[i][1]) - abs(cords[i][0]))) / 2
        sum_area += area
    return sum_area
```

# Time comparison

Now it's time to compare the methods in terms of execution time.

Below is the time measuring function:

```python
def time_measure(get_coo_fun, sum_area_fun, step=1):
    start = time.process_time()

    x_list, y_list = get_points_list(func=integrand, step=step, **params)
    cords = get_coo_fun(x_list, y_list, step=step)
    result = sum_area_fun(cords, step=step)

    end = time.process_time()
    total = end - start
    return result, total
```

# Results for the Square Method

```python
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
```

Create a plot that compares step and time:

```python
from matplotlib import pyplot as plt

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
```
Output:

![image](https://github.com/user-attachments/assets/c0b8b4da-ef14-4f7e-8c52-13161de571e9)


Results entering in the table:

```python
from tabulate import tabulate

comparison_sq = {
    "time": [tim for tim in result_time_square],
    "result": [res for res in results_square],
    "step": [step for step in step_list_square]
}

print(tabulate(comparison_sq, headers='keys', 
               disable_numparse=True, showindex=True))
```
Output:

```
    time                  result              step
--  --------------------  ------------------  --------------
0   0.01847597700000847   501670671501.60205  1
1   0.027218473000004906  501670295876.71387  0.5
2   0.05680925600000819   501670201970.4916   0.25
3   0.10743188299998963   501670178493.9365   0.125
4   0.1759064350000017    501670172624.79663  0.0625
5   0.2323298629999897    501670171157.5102   0.03125
6   0.5132962990000038    501670170790.6903   0.015625
7   0.9817313989999974    501670170698.9831   0.0078125
8   1.9272066569999993    501670170676.0623   0.00390625
9   4.635888637000008     501670170670.32056  0.001953125
10  10.27567470000001     501670170668.8956   0.0009765625
11  20.576515642000004    501670170668.52997  0.00048828125
12  40.267461870000005    501670170668.46185  0.000244140625
```

A function that calculates the percentage differences between our function and the built-in function:

```python
proc_list_sq = []
for i, n in enumerate(comparison_sq["result"]):
    if i == 0:
        continue
    else:
        proc = (abs((100 * n) / I[0]) - 100) * 1000
        """ I increased the result 1000 times 
            because the differences were very small """
        proc_list_sq.append(proc)
```

Creating a plot showing our results:

```python
fig, ax = plt.subplots()

fig = plt.plot(proc_list_sq)

labels = [item.get_text() for item in ax.get_xticklabels()]

labels[::] = [round(step_list_square[i], 4) for i,
              v in enumerate(step_list_square)]

ax.set_xticklabels(labels)

plt.xlabel("Step")
plt.ylabel("Precent")
plt.grid(True)
plt.show()
```

Output:

![image](https://github.com/user-attachments/assets/f3964915-ca8f-429a-a189-31e77dd631d5)


# Results for the Trapezoidal Method

...

