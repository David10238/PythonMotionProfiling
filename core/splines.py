
from __future__ import annotations

import numpy as np
from numpy.linalg import inv

class CubicSpline1d:
    def __init__(self, a:float, b:float, c:float, d:float) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        pass
    def fit_spline(x0, x1, y0, y1, k0, k1)-> CubicSpline1d:
        A = np.matrix([
            [x0**3, x0**2, x0, 1],
            [x1**3, x1**2, x1, 1],
            [3*x0**2, 2*x0, 1, 0],
            [3*x1**2, 2*x1, 1, 0]
        ])
        y = np.matrix([[y0, y1, k0, k1]]).transpose()
        fit = np.matmul(inv(A), y)
        [a, b, c, d] = fit
        return CubicSpline1d(a, b, c, d)
        
    def interp(self, x:float):
        return self.a*x**3 + self.b*x**2 + self.c*x + self.d