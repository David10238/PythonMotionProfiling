
import matplotlib.pyplot as plt
import numpy as np

from core.profile import generateTrapezoidProfile, MotionProfile

v = 70
a = 50


def plot_profile(title:str, prof: MotionProfile)-> None:
    t = np.linspace(0.0, prof.duration, 10000)
    plt.plot(t, np.vectorize(lambda t : prof.interp(t).x)(t), label = "x")
    plt.plot(t, np.vectorize(lambda t : prof.interp(t).vel)(t), label = "vel")
    plt.plot(t, np.vectorize(lambda t : prof.interp(t).acc)(t), label = "acc")
    plt.legend()
    plt.title(title)
    plt.show()

plot_profile("forward", generateTrapezoidProfile(0, 200, v, a))
plot_profile("backward", generateTrapezoidProfile(200, 0, v, a))
plot_profile("short", generateTrapezoidProfile(50, 0, v, a))

plot_profile("short offset", generateTrapezoidProfile(50, 20, v, a))
plot_profile("long offset", generateTrapezoidProfile(50, 250, v, a))