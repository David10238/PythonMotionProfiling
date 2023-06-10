import matplotlib.pyplot as plt
import numpy as np

from core.splines import CubicSpline1d

spline = CubicSpline1d.fit_spline(x0=1, x1=4, y0=3, y1=5, k0=0.5, k1=0.0)
x = np.linspace(1, 4, 1000)
y = np.vectorize(spline.interp)(x)
plt.plot(x, y)
plt.show()
