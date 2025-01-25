import wpilib

from ports import PWM
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem


class Arm(Subsystem):
    speed = autoproperty(0.3)

    def __init__(self):
        super().__init__()
        self.arm_motor = wpilib.VictorSP(PWM.arm_motor)

    def moveUp(self):
        self.arm_motor.set(self.speed)

    def moveDown(self):
        self.arm_motor.set(self.speed * -1)

    def stop(self):
        self.arm_motor.stopMotor()

    def getCurrentDrawAmps(self) -> float:
        pass
