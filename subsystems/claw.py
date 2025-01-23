from wpilib import VictorSP

import ports
from ultime.subsystem import Subsystem


class Claw(Subsystem):

    def __init__(self):
        super().__init__()
        self._motor_right = VictorSP(ports.PWM.claw_motor_right)
        self._motor_left = VictorSP(ports.PWM.claw_motor_left)

    def stop(self):
        self._motor_right.stopMotor()
        self._motor_left.stopMotor()
