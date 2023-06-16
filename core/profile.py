from __future__ import annotations

from math import sqrt

class MotionState():
    def __init__(self, x:float = 0.0, vel:float = 0.0, acc:float = 0.0) -> None:
        self.x = x
        self.vel = vel
        self.acc = acc

    def interpolate(self, t:float)->MotionState:
        return MotionState(
            x = (self.x) + (t*self.vel) + (t**2*self.acc/2.0),
            vel = (self.vel) + (self.acc*t),
            acc = self.acc
        )


class MotionStage():
    def __init__(self, start:MotionState, duration:float) -> None:
        self.start = start
        self.end = start.interpolate(t = duration)
        self.duration = duration

    def interpolate(self, t:float)->MotionState:
        if t > self.duration:
            return self.head
        return self.start.interpolate(t)

    def flipped(self)-> MotionState:
        return MotionStage(MotionState(self.end.x, -self.end.vel, self.end.acc), self.duration)

class MotionProfile:
    def __init__(self, stages:list[MotionStage]) -> None:
        self._stages = stages
        self.start = stages[0].start
        self.end = stages[-1].end
        self.duration = 0.0
        for stage in stages:
            self.duration += stage.duration

    def interpolate(self, t:float)->MotionState:
        for stage in self._stages:
            if(t < stage.duration):
                return stage.interpolate(t)
            t -= stage.duration
        return self.end

    def flipped(self)->MotionProfile:
        return MotionProfile(list(map(lambda stage : stage.flipped(), self._stages[::-1])))

def generateTrapezoidProfile(start:float, end:float, maxVel:float, maxAcc:float)->MotionProfile:
    if(end < start):
        return generateTrapezoidProfile(end, start, maxVel, maxAcc).flipped()

    distance = end - start
    rampTime = maxVel / maxAcc
    rampDistance = rampTime**2 * maxAcc / 2

    # distance is too short for max velocity
    if rampDistance * 2 > distance:
        rampTime = sqrt(2 * (distance/2) / maxAcc)
        rampDistance = rampTime**2 * maxAcc / 2
        return MotionProfile([
            MotionStage(MotionState(start), 0.0),
            MotionStage(MotionState(start, 0.0, maxAcc), rampTime), # ramp up
            MotionStage(MotionState(start + rampDistance, maxAcc * rampTime, -maxAcc), rampTime), # ramp doown
            MotionStage(MotionState(end), 0.0)
        ])
    
    # we can reach maximum velocity
    cruiseDistance = distance - (2 * rampDistance)
    return MotionProfile([
        MotionStage(MotionState(start), 0.0),
        MotionStage(MotionState(start, 0.0, maxAcc), rampTime), # ramp up
        MotionStage(MotionState(start + rampDistance, maxVel), cruiseDistance / maxVel), # cruise
        MotionStage(MotionState(start + rampDistance + cruiseDistance, maxVel, -maxAcc), rampTime), # ramp down
        MotionStage(MotionState(end), 0.0) # stop
    ])
