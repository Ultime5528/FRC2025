from wpilib import VictorSP
from wpiutil import SendableBuilder
from commands.printer.moveprinter import MovePrinter
from commands2.cmd import sequence
import ports
from ultime.subsystem import Subsystem
from ultime.switch import Switch


class Claw(Subsystem):
    def __init__(self):
        super().__init__()
        from commands.claw.loadcoral import LoadCoral

        self._motor_right = VictorSP(ports.PWM.claw_motor_right)
        self._motor_left = VictorSP(ports.PWM.claw_motor_left)
        self._sensor = Switch(Switch.Type.NormallyOpen, ports.DIO.claw_photocell)
        self._load = LoadCoral(self.claw)
        self._move = MovePrinter.toMiddleRight(self.printer)
        self._load_command = sequence(self._load, self._move)
        self.has_coral = False
        self.is_at_loading = False
        self.is_coral_retracted = False

    def stop(self):
        self._motor_right.stopMotor()
        self._motor_left.stopMotor()

    def setRight(self, speed: float):
        self._motor_right.set(speed)

    def setLeft(self, speed: float):
        self._motor_left.set(speed)

    def seesObject(self):
        return self._sensor.isPressed()

    def periodic(self) -> None:
        if self.seesObject() and not self.has_coral and self.is_at_loading:
            self._load_command.schedule()

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def noop(_):
            pass

        builder.addFloatProperty("motor_left", self._motor_left.get, noop)
        builder.addFloatProperty("motor_right", self._motor_right.get, noop)
        builder.addBooleanProperty("sees_object", self.seesObject, noop)
        builder.addBooleanProperty("has_coral", lambda: self.has_coral, noop)
        builder.addBooleanProperty("is_at_loading", lambda: self.has_coral, noop)
        builder.addBooleanProperty(
            "is_coral_retracted", lambda: self.is_coral_retracted, noop
        )
