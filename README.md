# Integration

Comparison of different integration methods in Python

## 📖 Description

In mathematics, a [Riemann sum](https://en.wikipedia.org/wiki/Riemann_sum) approximates the integral of a function by partitioning the region into finite shapes (e.g., rectangles, trapezoids). This approach is widely used in numerical integration when exact solutions to definite integrals are challenging to compute analytically.

This project compares different methods of numerical integration:

* **Square Method:** Approximating areas using rectangles.
* **Trapezoidal Method:** Approximating areas using trapezoids.
* **Built-in Method:** Using Python's `quad` function from [scipy.integrate](https://docs.scipy.org/doc/scipy/tutorial/integrate.html).

The comparison focuses on:
1. Accuracy of the results.
2. Execution time.

## 🚀 Getting Started

Libraries used:
- [numpy](https://numpy.org/)
- [time](https://docs.python.org/3/library/time.html)
- [pyplot](https://matplotlib.org/stable/tutorials/pyplot.html) from [matplotlib](https://matplotlib.org/)
- [tabulate](https://pypi.org/project/tabulate/)
- `quad` form [scipy.integrate](https://docs.scipy.org/doc/scipy/tutorial/integrate.html)

Install required libraries via `pip`:

```bash
pip install numpy matplotlib tabulate scipy
```

## 🔧 Executing program

### 1. Import Required Libraries
Start by importing the necessary libraries:

```python
import numpy as np
import time
from matplotlib import pyplot as plt
from scipy.integrate import quad
```

### 2. Define Input Parameters
Set up the parameters for the mathematical function to be integrated:

```python
params = {
    "c": 1,
    "a": 2,
    "b": 5,
    "c": 7,
    "z": 4,
}
```

### 3. Define the Integrand Function
This function constructs the mathematical operation based on the parameters:

```python
def integrand(x, **kwargs):
    y = 0
    for i, (k, v) in enumerate(sorted(params.items())[::-1]):
        y = y + (v * x**i) + np.sin(x)
    return y
```

### 4. Generate Points for Approximation
Use the following function to create points for `x` and corresponding values for `y`:

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

## 🧮 Integration Methods

### 1. Built-in Method (`quad`)

Using the `quad` function from [scipy.integrate](https://docs.scipy.org/doc/scipy/tutorial/integrate.html) for numerical integration:

```python
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

### 2. Square Method

The Square Method works by approximating the area under the graph of the function as rectangles and calculating their area.

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

Calculate Area:

```python
def sum_area(cords, step=1):
    """This function sums the areas of all rectangles"""
    sum_area = 0
    for coo in cords:
        area = (abs(coo[1]) - abs(coo[0])) * abs(coo[2])
        sum_area += area
    return sum_area
```

### 3. Trapezoidal Method

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

Calculate Area:

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

## ⏳ Time comparison

### Measuring Execution Time:

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

### Results:

```python
STEP = 1
results = []
result_time = []
step_list = []

""" Loop that will run functions 13 times 
    (reduces the step by half each time) """
for i in range(1, 14):
    step_list.append(STEP)
    res, tim = time_measure(get, sum_area, step=STEP)
    results.append(res)
    result_time.append(tim)
    STEP *= 0.5
```

Results are tabulated using `tabulate` for better readability.

```python
comparison = {
    "time": [tim for tim in result_time_square],
    "result": [res for res in results_square],
    "step": [step for step in step_list_square]
}

print(tabulate(comparison, headers='keys', 
               disable_numparse=True, showindex=True))
```

Results are visualized using `matplotlib`.

```python
fig, ax = plt.subplots()
fig = plt.plot(proc_list)

labels = [item.get_text() for item in ax.get_xticklabels()]
labels[::] = [round(step_list[i], 4) for i,
              v in enumerate(step_list)]

ax.set_xticklabels(labels)

plt.xlabel("Step")
plt.ylabel("Procent")
plt.grid(True)
plt.show()
```

## Results for the Square Method

![image](https://github.com/user-attachments/assets/c0b8b4da-ef14-4f7e-8c52-13161de571e9)

Results entering in the table:

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
proc_list = []
for i, n in enumerate(comparison["result"]):
    if i == 0:
        continue
    else:
        proc = (abs((100 * n) / I[0]) - 100) * 1000
        """ I increased the result 1000 times 
            because the differences were very small """
        proc_list.append(proc)
```

Plot showing our results:

![image](https://github.com/user-attachments/assets/f3964915-ca8f-429a-a189-31e77dd631d5)

## Results for the Trapezoidal Method

We proceed in the same way as in the case of the Square Method:

![image](https://github.com/user-attachments/assets/415e265f-01ee-42f7-aa36-e5458cd23496)

Results entering in the table:

```
    time                  result              step
--  --------------------  ------------------  --------------
0   0.017274687999986327  501670671495.2609   1
1   0.016082500999999638  501670295874.8491   0.5
2   0.03345482000000288   501670201969.7989   0.25
3   0.06489974600000892   501670178493.6401   0.125
4   0.12876187199998412   501670172624.6601   0.0625
5   0.25719226100000014   501670171157.44666  0.03125
6   0.5484355190000088    501670170790.65656  0.015625
7   1.041992456999992     501670170698.97266  0.0078125
8   2.100061573000005     501670170676.0516   0.00390625
9   6.040882949999997     501670170670.32336  0.001953125
10  10.377945259          501670170668.8924   0.0009765625
11  20.778565375          501670170668.51306  0.00048828125
12  41.888402670999994    501670170668.45123  0.000244140625
```

Plot showing percentage differences between our function and the built-in function:

![image](https://github.com/user-attachments/assets/f6910356-0615-4329-bde2-d5e88e265e7a)

## 📊 Comparisons

Comparison of results between the Square Method and the Trapezoidal Method:

![image](https://github.com/user-attachments/assets/23a70324-a9ee-4d41-ab39-bac5baf69232)

Comparison of times between the Square Method and the Trapezoidal Method:

![image](https://github.com/user-attachments/assets/c4d621ea-3c01-47bd-8bd9-e73d58f879bc)


## 🧪 Conclusions

1. The Square Method is simpler but less accurate for smaller step sizes compared to the Trapezoidal Method.
2. The Trapezoidal Method achieves better accuracy with a comparable execution time.
3. For high precision, using built-in methods like `quad` is recommended due to their optimized algorithms.

## 📜 License
This project is licensed under the MIT License. See the `LICENSE` file for details.
