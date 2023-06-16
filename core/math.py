from typing import Callable
import numpy as np
from geom import Point
from math import sqrt, exp

EPS = 2.2e-15

# todo make list of results, to make parametization easier

class IntegrationResult:
    def __init__(self) -> None:
        self.vals = [0.0]
        self.sums = [0.0]
        self.total_sum = 0.0
    
    def interpolate(self, t:float)->float:
        return np.interp(x=t, xp=self.vals, fp=self.sums, left=self.sums[0], right=self.total_sum)
    
    def inverse_interpolate(self, t:float)->float:
        return np.interp(x=t, xp=self.sums, fp=self.vals, left=self.vals[0], right=self.vals[-1])

def integrate(a:float, b:float, f:Callable[[float], float], eps=EPS, maxJump = 100000.0)->IntegrationResult:
    result = IntegrationResult()
    f = np.vectorize(f)

    def five_point(a:float, b:float)->float:
        points = np.array([0, (-1/3) * sqrt(5 - 2*sqrt(10/7)), (1/3) * sqrt(5 - 2*sqrt(10/7)), (-1/3) * sqrt(5 + 2*sqrt(10/7)), (1/3) * sqrt(5 + 2*sqrt(10/7))])
        weights = np.array([128 / 225, (322 + 13*sqrt(70))/900, (322 + 13*sqrt(70))/900, (322 - 13*sqrt(70))/900, (322 - 13*sqrt(70))/900])
        x = ((b-a)*points/2) + (a+b)/2
        return ((b-a)/2) * sum(f(x) * weights)
    
    def helper(a:float, b:float, i:float, result:IntegrationResult)->float:
        m = (a+b) / 2
        i1 = five_point(a, m)
        i2 = five_point(m, b)
        if(abs(i - (i1 + i2)) <= eps and abs(i1) <= maxJump and abs(i2) <= maxJump):
            result.vals.append(m)
            result.sums.append(result.sums[-1] + i1)
            result.vals.append(b)
            result.sums.append(result.sums[-1] + i2)
        else:
            helper(a, m, i1, result)
            helper(m, b, i2, result)
    
    helper(a, b, five_point(a, b), result)
    result.total_sum = result.sums[-1]
    return result

def arc_length(a:float, b:float, df:Callable[[float], Point]):
    f = lambda t : sqrt(1 + df(t)**2)
    return integrate(a, b, f, maxJump=0.01)