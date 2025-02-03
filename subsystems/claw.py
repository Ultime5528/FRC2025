from wpilib import VictorSP, RobotBase
from wpilib.simulation import PWMSim

import ports
from ultime.subsystem import Subsystem


class Claw(Subsystem):

    def __init__(self):
        super().__init__()
        self._motor_right = VictorSP(ports.PWM.claw_motor_right)
        self._motor_left = VictorSP(ports.PWM.claw_motor_left)

        if RobotBase.isSimulation():
            self._sim_motor = PWMSim(self._motor_right)
            self._sim_motor = PWMSim(self._motor_left)

    def stop(self):
        self._motor_right.stopMotor()
        self._motor_left.stopMotor()

    def setRight(self, speed: float):
        self._motor_right.set(speed)

    def setLeft(self, speed: float):
        self._motor_left.set(speed)
