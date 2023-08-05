# Plotter
A sane plotting API. Currently it only supports matplotlib as the backend, but other backends can be plugged.

# Source
https://bitbucket.org/avilay/plotter/src/master/

# Installation
```bash
pip install avilabs-plotter
```

# Quick Start
```python
import plotter as pltr
pltr.set_backend(pltr.MatplotlibBackend)

nodes = ['master', 'worker1', 'worker2']
cpus = [0.1, 0.6, 0.4]
cpusbar = pltr.VerticalBar(categories=nodes, values=cpus)
pltr.show_plot('CPU Performance', cpusbar)
```

### Output:
![Figure_1.png](images/quick_start.png)

# Plot Styles
Plotter can plot a number of different plot styles.

### Samples

![bars](images/bars.png)

![graphs](images/graphs.png)

![imgs](images/imgs.png)

![lines](images/lines.png)

![quick_start](images/quick_start.png)

![scatter](images/scatter.png)

### Categorical Plots
When the x-axis is composed of labels and the y-axis are numbers.

  * Horizontal Bar
  * Line
  * Vertical Bar
  
### Numeric Plots
When both the x-axis and y-axis are numbers.

  * Graph
  * Scatter
  
### Images

  * Grayscale Image
  * RGB Image
  
# Concepts

Frame --> * Chart --> * Plot --> * Axis

A `Plot` is composed of `Axis` objects. A `Chart` can have multiple `Plot`s in it, provided all their `Axis` are compatible. A `Frame` can have multiple `Chart`s. 

# Detailed Usage
```python
import numpy as np

from plotter import Axis, Frame, Graph, MatplotlibBackend, set_backend, Font, Color

set_backend(MatplotlibBackend)

frame = Frame(height_px=600, width_px=10000)
frame.layout(nrows=1, ncols=2)

# Trig chart
chart = frame.create_chart()
chart.title = 'Trig Chart'
chart.x_axis = Axis(label='Radians', font=Font(size=14, color=Color(red=255, blue=126, green=0)))

cosx = Graph((-np.pi, np.pi), np.cos, legend='cos(x)')
chart.add(cosx)

sinx = Graph((-np.pi, np.pi), np.sin, legend='sin(x)')
chart.add(sinx)

# Geometry chart
chart = frame.create_chart()
chart.grid = True
chart.origin = (0, 0)

line = Graph((-10, 10), lambda x: 2*x)
chart.add(line)
chart.x_axis = Axis(label='x')
chart.y_axis = Axis(label='y', limits=(-25, 25))

frame.show()
```

### Output:
![Figure_2.png](images/graphs.png)


See the [examples directory](https://gitlab.com/avilay/plotter/tree/master/examples) for more usage.
