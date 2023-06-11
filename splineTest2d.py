
from core.splines import CubicSpline2d
from core.geom import Point

import numpy as np
import tkinter as tk

spline = CubicSpline2d(
    start = Point(0, 0),
    startDeriv = Point(50, 0),
    end = Point(30, 20),
    endDeriv = Point(0, 50))

points = np.vectorize(spline.interp)(np.linspace(0, 1, 1000))


top = tk.Tk()
c = tk.Canvas(top, bg="white", height = 200, width= 300)
lastPoint = None
for point in points:
    if lastPoint != None:
        c.create_line(lastPoint.x*10, lastPoint.y*10, point.x*10, point.y*10)
    lastPoint = point
c.pack()
top.mainloop()