from wpilib import VictorSP
from wpiutil import SendableBuilder

import ports
from ultime.alert import AlertType
from ultime.subsystem import Subsystem
from ultime.switch import Switch
from ultime.timethis import timethis as tt


class Claw(Subsystem):
    def __init__(self):
        super().__init__()
        from commands.claw.loadcoral import LoadCoral

        self._motor_right = VictorSP(ports.PWM.claw_motor_right)
        self._motor_left = VictorSP(ports.PWM.claw_motor_left)
        self._sensor = Switch(Switch.Type.NormallyOpen, ports.DIO.claw_photocell)
        self._load_command = LoadCoral(self)
        self.has_coral = False
        self.is_at_loading = False
        self.is_coral_retracted = False

        self.alert_is_at_loading = self.createAlert(
            "Claw is not at loading. Make sure to also move elevator to loading",
            AlertType.Error,
        )
        self.alert_has_coral = self.createAlert(
            "Claw didn't return the correct value after loading. Is there a coral in the loader? Execution will halt until a coral is placed",
            AlertType.Warning,
        )
        self.alert_load_failed = self.createAlert(
            "Claw didn't succeed loading. Check sensor", AlertType.Error
        )
        self.alert_drop_failed = self.createAlert(
            "Claw did not drop coral. Check motors", AlertType.Error
        )

    def stop(self):
        self._motor_right.stopMotor()
        self._motor_left.stopMotor()

    def setRight(self, speed: float):
        self._motor_right.set(speed)

    def setLeft(self, speed: float):
        self._motor_left.set(speed)

    def getLeftInput(self):
        return self._motor_left.get()

    def getRightInput(self):
        return self._motor_right.get()

    def seesObject(self):
        return self._sensor.isPressed()

    def periodic(self) -> None:
        pass

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def noop(_):
            pass

        builder.addFloatProperty("motor_left", tt(self.getLeftInput), noop)
        builder.addFloatProperty("motor_right", tt(self.getRightInput), noop)
        builder.addBooleanProperty("sees_object", tt(self.seesObject), noop)
        builder.addBooleanProperty("has_coral", tt(lambda: self.has_coral), noop)
        builder.addBooleanProperty("is_at_loading", tt(lambda: self.has_coral), noop)
        builder.addBooleanProperty(
            "is_coral_retracted", tt(lambda: self.is_coral_retracted), noop
        )
