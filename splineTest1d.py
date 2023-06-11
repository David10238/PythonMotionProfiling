import matplotlib.pyplot as plt
import numpy as np

from core.splines import CubicSpline1d

spline = CubicSpline1d.fit_spline(y0=6, y1=4, v0=1.0, v1=-1.0)
x = np.linspace(0, 1, 1000)
y = np.vectorize(spline.interp)(x)
plt.plot(x, y)
plt.show()

