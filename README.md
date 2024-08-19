# Integration

Comparison of different integration methods in Python

# Getting Started

Libraries used:
* [numpy](https://numpy.org/)
* [time](https://docs.python.org/3/library/time.html)
* [pyplot](https://matplotlib.org/stable/tutorials/pyplot.html) from [matplotlib](https://matplotlib.org/)
* [tabulate](https://pypi.org/project/tabulate/)
* `quad` form [scipy.integrate](https://docs.scipy.org/doc/scipy/tutorial/integrate.html)

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
