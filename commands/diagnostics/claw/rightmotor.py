import wpilib
from commands2 import Command
from wpilib import RobotController, DataLogManager

from commands.claw.drop import drop_properties
from subsystems.claw import Claw
from ultime.autoproperty import autoproperty


class DiagnoseRightMotor(Command):
    voltage_change_threshold = autoproperty(0.5)

    def __init__(self, claw: Claw):
        super().__init__()
        self.addRequirements(claw)
        self.claw = claw
        self.timer = wpilib.Timer()
        self.voltage_before = None
        self.voltage_during = None
        self.voltage_after = None

    def initialize(self):
        self.timer.reset()
        self.timer.start()
        self.voltage_before = RobotController.getBatteryVoltage()
        self.claw.stop()

    def execute(self):
        if self.timer.get() < 0.1:
            self.claw.setRight(0)
            self.voltage_before = RobotController.getBatteryVoltage()
        elif self.timer.get() < 1:
            self.claw.setRight(drop_properties.speed_level_4_right)
            self.voltage_during = RobotController.getBatteryVoltage()
        elif self.timer.get() < 2:
            self.claw.setRight(0)
            self.voltage_after = RobotController.getBatteryVoltage()

    def isFinished(self) -> bool:
        return self.timer.get() > 2

    def end(self, interrupted: bool):
        self.claw.stop()
        voltage_delta_before = self.voltage_before - self.voltage_during
        voltage_delta_after = self.voltage_after - self.voltage_during
        DataLogManager.log(
            "Claw diagnostics: Right motor voltage delta before:"
            + str(voltage_delta_before)
        )
        DataLogManager.log(
            "Claw diagnostics: Right motor voltage delta after:"
            + str(voltage_delta_after)
        )
        if (
            voltage_delta_before < self.voltage_change_threshold
            or voltage_delta_after < self.voltage_change_threshold
        ):
            self.claw.alert_right_motor.set(True)
