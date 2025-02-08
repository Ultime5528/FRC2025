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
        Invalid = auto()
        Moving = auto()
        Reset = auto()
        Extended = auto()
        Retracted = auto()

    pivot_speed = autoproperty(0.5)
    grab_speed = autoproperty(0.3)
    pivot_encoder_threshold = autoproperty(50)
    pivot_height_max = autoproperty(0)
    position_conversion_factor = autoproperty(0.002)

    retracted = autoproperty(-0.01)

    def __init__(self):
        super().__init__()

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
        self._prev_is_in = False
        self._offset = 0.0

        if RobotBase.isSimulation():
            self._sim_grab_motor = PWMSim(self._grab_motor)
            self._sim_pivot_motor = PWMSim(self._pivot_motor)
            self._sim_encoder = EncoderSim(self._pivot_encoder)
            self._sim_pos = 0.3

    def periodic(self) -> None:
        if self._prev_is_in and not self._pivot_switch.isPressed():
            self._offset = self.pivot_height_max - self._pivot_encoder.getPosition()
            self._has_reset = True
        self._prev_is_in = self._pivot_switch.isPressed()

    def simulationPeriodic(self) -> None:
        distance = self._pivot_motor.get() * 0.02

        self._sim_pos += distance
        self._sim_encoder.setDistance(self._sim_encoder.getDistance() + distance)

        if self._sim_pos <= self.retracted:
            self._pivot_switch.setSimPressed()
        else:
            self._pivot_switch.setSimUnpressed()

    def retractPivot(self):
        if not self._pivot_switch.isPressed():
            self._pivot_motor.set(self.pivot_speed)

    def extendPivot(self):
        self._pivot_motor.set(-1 * self.pivot_speed)

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

    def getPos(self):
        """gets Position"""
        return self._pivot_encoder.get()

    def hasReset(self):
        return self._has_reset

    def isRetracted(self):
        return self._pivot_switch.isPressed()

    def hasAlgae(self):
        return self._grab_switch.isPressed()

    def getMotorInput(self, motor: str):
        """motor should be "pivot" or "grab" """
        if motor == "pivot":
            return self._pivot_motor.get()
        elif motor == "grab":
            return self._grab_motor.get()
        else:
            print("what? this isn't even a motor")

    def getCurrentDrawAmps(self) -> float:
        pass
