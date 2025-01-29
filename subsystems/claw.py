from _pytest.python_api import approx
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

            def simulationPeriodic(self) -> None:

                self._sim_encoder.setDistance(
                    self._sim_encoder.getDistance() + self._motor.get()
                )

    def stop(self):
        self._motor_right.stopMotor()
        self._motor_left.stopMotor()

    def setRight(self, speed: float):
        self._motor_right.set(speed)

    def setLeft(self, speed: float):
        self._motor_left.set(speed)

    def isLeftRunning(self) -> bool:
        return not self._motor_left.getVoltage() == approx(0.0)

    def isRightRunning(self) -> bool:
        return not self._motor_right.getVoltage() == approx(0.0)
