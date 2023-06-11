from typing import Callable
import numpy as np
from math import sqrt, exp

EPS = 2.2e-10

# todo make list of results, to make parametization easier
def integrate(a:float, b:float, f:Callable[[float], float], eps=EPS)->float:
    f = np.vectorize(f)
    def five_point(a:float, b:float)->float:
        points = np.array([0, (-1/3) * sqrt(5 - 2*sqrt(10/7)), (1/3) * sqrt(5 - 2*sqrt(10/7)), (-1/3) * sqrt(5 + 2*sqrt(10/7)), (1/3) * sqrt(5 + 2*sqrt(10/7))])
        weights = np.array([128 / 225, (322 + 13*sqrt(70))/900, (322 + 13*sqrt(70))/900, (322 - 13*sqrt(70))/900, (322 - 13*sqrt(70))/900])
        x = ((b-a)*points/2) + (a+b)/2
        return ((b-a)/2) * sum(f(x) * weights)
    
    def helper(a:float, b:float, i:float)->float:
        m = (a+b) / 2
        i1 = five_point(a, m)
        i2 = five_point(m, b)

        if(abs(i - (i1 + i2)) <= eps):
            return i1 + i2
        return helper(a, m, i1) + helper(m, b, i2)
    
    return helper(a, b, five_point(a, b))