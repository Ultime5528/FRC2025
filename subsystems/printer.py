from enum import Enum, auto

import wpilib
from wpilib import RobotBase
from wpilib.simulation import PWMSim, EncoderSim
from wpiutil import SendableBuilder

import ports
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem
from ultime.switch import Switch


class Printer(Subsystem):
    class State(Enum):
        Unknown = auto()
        Moving = auto()
        Left = auto()
        MiddleLeft = auto()
        Middle = auto()
        MiddleRight = auto()
        Right = auto()
        Loading = auto()
        Reset = auto()

    class MovementState(Enum):
        AvoidMiddleZone = auto()
        FreeToMove = auto()
        Unknown = auto()

    speed = autoproperty(0.5)
    left = autoproperty(0.42)
    right = autoproperty(-0.01)
    middle_zone_left = autoproperty(0.3)
    middle_zone_right = autoproperty(0.1)

    position_conversion_factor = autoproperty(0.002)

    def __init__(self):
        super().__init__()
        self._switch_right = Switch(
            Switch.Type.NormallyClosed, ports.DIO.printer_switch_right
        )
        self._switch_left = Switch(
            Switch.Type.NormallyClosed, ports.DIO.printer_switch_left
        )

        self._motor = wpilib.VictorSP(ports.PWM.printer_motor)
        self._motor.setInverted(True)
        self._encoder = wpilib.Encoder(
            ports.DIO.printer_encoder_a,
            ports.DIO.printer_encoder_b,
            reverseDirection=True,
        )
        self.addChild("motor", self._motor)
        self.addChild("encoder", self._encoder)

        self.photocell = Switch(Switch.Type.NormallyOpen, ports.DIO.printer_photocell)

        self._offset = 0.0
        self._has_reset = False
        self._prev_is_right = False
        self._prev_is_left = False
        self.movement_state = Printer.MovementState.Unknown
        self.state = Printer.State.Unknown

        if RobotBase.isSimulation():
            self._sim_motor = PWMSim(self._motor)
            self._sim_encoder = EncoderSim(self._encoder)
            self._sim_initial_position = 0.03
            self._sim_position = self._sim_initial_position

    def periodic(self) -> None:
        if self._prev_is_right and not self._switch_right.isPressed():
            self._offset = self.right - self._encoder.get()
            self._has_reset = True
        self._prev_is_right = self._switch_right.isPressed()

    def simulationPeriodic(self) -> None:
        distance = self._motor.get() * 0.05

        self._sim_position += distance

        self._sim_encoder.setCount(
            int(
                (self._sim_position - self._sim_initial_position)
                / self.position_conversion_factor
            )
        )

        if self._sim_position <= self.right:
            self._switch_right.setSimPressed()
            self._switch_left.setSimUnpressed()
        elif self._sim_position >= self.left:
            self._switch_left.setSimPressed()
            self._switch_right.setSimUnpressed()
        else:
            self._switch_right.setSimUnpressed()
            self._switch_left.setSimUnpressed()

        assert not (
            self.isRight() and self.isLeft()
        ), "Both switches are on at the same time which doesn't make any sense"

    def moveLeft(self):
        self.setSpeed(self.speed)

    def moveRight(self):
        self.setSpeed(-self.speed)

    def setSpeed(self, speed: float):
        if (
            self.movement_state == Printer.MovementState.AvoidMiddleZone
            and self.isInMiddleZone()
        ):
            middle = (self.middle_zone_left + self.middle_zone_right) / 2.0
            position = self.getPosition()

            if (position < middle and speed > 0.0) or position > middle and speed < 0.0:
                speed = 0.0
        elif self.isLeft():
            speed = speed if speed <= 0.0 else 0.0
        elif self.isRight():
            speed = speed if speed >= 0.0 else 0.0

        self._motor.set(speed)

    def isLeft(self) -> bool:
        return self._switch_left.isPressed()

    def isRight(self) -> bool:
        return self._switch_right.isPressed()

    def seesReef(self):
        return self.photocell.isPressed()

    def isInMiddleZone(self) -> bool:
        pose = self.getPosition()
        return pose >= self.middle_zone_right and pose <= self.middle_zone_left

    def stop(self):
        self._motor.stopMotor()

    def setPosition(self, reset_value):
        self._offset = reset_value - self._encoder.get()

    def getPosition(self):
        return (self._encoder.get() + self._offset) * self.position_conversion_factor

    def getMotorInput(self):
        return self._motor.get()

    def hasReset(self):
        return self._has_reset

    def getCurrentDrawAmps(self) -> float:
        return self._motor.getVoltage()

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def setOffset(value: float):
            self._offset = value

        def noop(x):
            pass

        def setHasReset(value: bool):
            self._has_reset = value

        builder.addStringProperty("state", lambda: self.state.name, noop)
        builder.addStringProperty(
            "state_movement", lambda: self.movement_state.name, noop
        )
        builder.addFloatProperty("motor_input", self._motor.get, noop)
        builder.addFloatProperty("encoder", self._encoder.get, noop)
        builder.addFloatProperty("offset", lambda: self._offset, lambda x: setOffset(x))
        builder.addFloatProperty("position", self.getPosition, noop)
        builder.addBooleanProperty("has_reset", lambda: self._has_reset, setHasReset)
        builder.addBooleanProperty("switch_right", self._switch_right.isPressed, noop)
        builder.addBooleanProperty("switch_left", self._switch_left.isPressed, noop)
        builder.addBooleanProperty("isRight", self.isRight, noop)
        builder.addBooleanProperty("isLeft", self.isLeft, noop)
        builder.addBooleanProperty("seesReef", self.seesReef, noop)
        builder.addBooleanProperty("isInMiddleZone", self.isInMiddleZone, noop)
