from commands2 import Command, SequentialCommandGroup
from commands2.cmd import runOnce, deadline, run
from wpilib import RobotController

from commands.climber.moveclimber import ReadyClimber, Climb
from commands.climber.resetclimber import ResetClimber
from subsystems.climber import Climber
from ultime.autoproperty import autoproperty
from ultime.command import ignore_requirements, WaitCommand
from ultime.proxy import proxy


@ignore_requirements(["climber"])
class DiagnoseSwitchAndMotor(SequentialCommandGroup):
    voltage_change_threshold = autoproperty(0.5)

    def __init__(self, climber: Climber):
        super().__init__(
            runOnce(proxy(self.before_climb)),
            ReadyClimber(climber),
            deadline(
                Climb(climber),
                run(proxy(self.during_climb))
            ),
            WaitCommand(0.1),
            runOnce(proxy(self.after_climb)),
            ResetClimber(climber)
        )
        self.climber = climber
        self.voltage_before = None
        self.voltage_during = None
        self.voltage_after = None

    def before_climb(self):
        self.voltage_before = RobotController.getBatteryVoltage()
        if self.climber.isClimbed():
            self.climber.alert_lswitch.set(True)

    def during_climb(self):
        self.voltage_during = RobotController.getBatteryVoltage()

    def after_climb(self):
        self.voltage_after = RobotController.getBatteryVoltage()
        voltage_delta_before = self.voltage_before - self.voltage_during
        voltage_delta_after = self.voltage_after - self.voltage_during
        if voltage_delta_before < self.voltage_change_threshold or voltage_delta_after < self.voltage_change_threshold:
            self.climber.alert_motor.set(True)
        if not self.climber.isClimbed():
            self.climber.alert_lswitch.set(True)
