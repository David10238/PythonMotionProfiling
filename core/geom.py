
import math

class Angle:
    def __init__(self, radians) -> None:
        self.radians = radians
        self.degrees = math.degrees(radians)

def Radians(theta)->Angle:
    return Angle(theta)

def Degrees(theta)->Angle:
    return Angle(math.radians(theta))

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.magnitude = math.hypot(x, y)
        self.theta = math.atan2(__y = y, __x = x)