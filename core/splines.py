
from __future__ import annotations

import numpy as np
from numpy.linalg import inv
from core.geom import Point

class CubicSpline1d:
    def __init__(self, a:float, b:float, c:float, d:float) -> None:
        self._a = a
        self._b = b
        self._c = c
        self._d = d
        pass
    def fit_spline(y0, y1, v0, v1)-> CubicSpline1d:
        return CubicSpline1d(
            a = 2*y0 - 2*y1 + v0 + v1,
            b = -3*y0 + 3*y1 - 2*v0 - v1,
            c = v0,
            d = y0)
        
    def interp(self, x:float):
        return self._a*x**3 + self._b*x**2 + self._c*x + self._d
    
class CubicSpline2d:
    def __init__(self, start:Point, startDeriv:Point, end:Point, endDeriv:Point) -> None:
        self._xSpline = CubicSpline1d.fit_spline(y0 = start.x, y1 = end.x, v0 = startDeriv.x, v1 = endDeriv.x)
        self._ySpline = CubicSpline1d.fit_spline(y0 = start.y, y1 = end.y, v0 = startDeriv.y, v1 = endDeriv.y)

    def interp(self, t:float)->Point:
        return Point(self._xSpline.interp(t), self._ySpline.interp(t))
