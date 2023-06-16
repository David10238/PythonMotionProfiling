
from __future__ import annotations

import numpy as np
from numpy.linalg import inv
from core.geom import Point
from core.math import arc_length

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
        
    def interpolate(self, x:float):
        return (self._a*x**3) + (self._b*x**2) + (self._c*x + self._d)
    
    def interpolate_first_derivative(self, x:float):
        return (3*self.a*x**2) + (2*self.b*x) + self.c
    
    def interpolate_second_derivative(self, x:float):
        return (6*self.a*x) + (2*self.b)
    
    def interpolate_third_derivative(self, x:float):
        return 6*self.a

class CubicSpline2d:
    def __init__(self, start:Point, startDeriv:Point, end:Point, endDeriv:Point) -> None:
        self._xSpline = CubicSpline1d.fit_spline(y0 = start.x, y1 = end.x, v0 = startDeriv.x, v1 = endDeriv.x)
        self._ySpline = CubicSpline1d.fit_spline(y0 = start.y, y1 = end.y, v0 = startDeriv.y, v1 = endDeriv.y)
        self._linIntegral = arc_length(0, 1, self.interpolate_first_derivative_percantage)

    def interpolate(self, t:float)->Point:
        return self.interpolate_percantage(self._linIntegral.inverse_interpolate(t))
    
    def interpolate_first_derivative(self, t:float)->Point:
        return self.interpolate_first_derivative_percantage(self._linIntegral.inverse_interpolate(t))
    
    def interpolate_second_derivative(self, t:float)->Point:
        return self.interpolate_second_derivative_percantage(self._linIntegral.inverse_interpolate(t))
    
    def interpolate_third_derivative(self, t:float)->Point:
        return self.interpolate_third_derivative_percantage(self._linIntegral.inverse_interpolate(t))

    def interpolate_percantage(self, t:float)->Point:
        return Point(self._xSpline.interpolate(t), self._ySpline.interpolate(t))
    
    def interpolate_first_derivative_percantage(self, t)->Point:
        return Point(self._xSpline.interpolate_first_derivative(t), self._ySpline.interpolate_first_derivative(t))

    def interpolate_second_derivative_percantage(self, t)->Point:
        return Point(self._xSpline.interpolate_second_derivative(t), self._ySpline.interpolate_second_derivative(t))
    
    def interpolate_third_derivative_percantage(self, t)->Point:
        return Point(self._xSpline.interpolate_third_derivative(t), self._ySpline.interpolate_third_derivative(t))