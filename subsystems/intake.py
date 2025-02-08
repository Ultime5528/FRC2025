from enum import Enum, auto

import wpilib
from wpilib import VictorSP, Encoder, RobotBase
from wpilib.simulation import PWMSim, EncoderSim

import ports
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem
from ultime.switch import Switch


class Intake(Subsystem):
    class State(Enum):
        Unknown = auto()
        Moving = auto()
        Extended = auto()
        Retracted = auto()

    pivot_speed = autoproperty(0.5)
    grab_speed = autoproperty(0.3)
    pivot_height_max = autoproperty(0.0)
    position_conversion_factor = autoproperty(0.02)

    def __init__(self):
        super().__init__()
        self.state = Intake.State.Unknown

        self._pivot_motor = VictorSP(ports.PWM.intake_motor_pivot)
        self._pivot_encoder = wpilib.Encoder(
            ports.DIO.intake_encoder_a,
            ports.DIO.intake_encoder_b,
            reverseDirection=False,
        )
        self._pivot_encoder.setDistancePerPulse(self.position_conversion_factor)
        self._pivot_switch = Switch(
            switch_type=Switch.Type.NormallyOpen, port=ports.DIO.intake_switch_pivot
        )

        self._grab_motor = VictorSP(ports.PWM.intake_motor_grab)
        self._grab_switch = Switch(
            Switch.Type.NormallyOpen, ports.DIO.intake_switch_grab
        )

        self._has_reset = False
        self._prev_is_retracted = False
        self._offset = 0.0

        if RobotBase.isSimulation():
            self._sim_grab_motor = PWMSim(self._grab_motor)
            self._sim_pivot_motor = PWMSim(self._pivot_motor)
            self._sim_encoder = EncoderSim(self._pivot_encoder)
            self._sim_pos = 0.3

    def periodic(self) -> None:
        if self._prev_is_retracted and not self.isRetracted():
            self._offset = self.pivot_height_max - self._pivot_encoder.get()
            self._has_reset = True
        self._prev_is_retracted = self.isRetracted()

    def simulationPeriodic(self) -> None:
        distance = self._pivot_motor.get() * 0.02

        self._sim_pos += distance
        self._sim_encoder.setDistance(self._sim_encoder.getDistance() + distance)

        if self._sim_pos <= -0.01:
            self._pivot_switch.setSimPressed()
        else:
            self._pivot_switch.setSimUnpressed()

    def retractPivot(self):
        if not self._pivot_switch.isPressed():
            self._pivot_motor.set(-1 * self.pivot_speed)

    def extendPivot(self):
        self._pivot_motor.set(self.pivot_speed)

    def stopPivot(self):
        self._pivot_motor.stopMotor()

    def setSpeedPivot(self, speed: float):
        self._pivot_motor.set(speed)

    def grab(self):
        self._grab_motor.set(self.grab_speed)

    def drop(self):
        self._grab_motor.set(-1 * self.grab_speed)

    def stopGrab(self):
        self._grab_motor.stopMotor()

    def getPivotPosition(self):
        return self._pivot_encoder.get() + self._offset

    def hasReset(self):
        return self._has_reset

    def isRetracted(self):
        return self._pivot_switch.isPressed()

    def hasAlgae(self):
        return self._grab_switch.isPressed()

    def getPivotMotorInput(self):
        return self._pivot_motor.get()

    def getCurrentDrawAmps(self) -> float:
        return 0.0
