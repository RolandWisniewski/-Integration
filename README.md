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

In calculus, the square method is a technique for numerical integration, i.e., approximating the definite integral.
The square method works by approximating the region under the graph of the function as a square and calculating its area.

You need to divide math functions into rectangles.

The following function creates the coordinates of these rectangles:

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

In calculus, the trapezoidal rule is a technique for numerical integration, i.e., approximating the definite integral.
The trapezoidal rule works by approximating the region under the graph of the function as a trapezoid and calculating its area.

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
