import wpilib
from commands2 import Command
from wpilib import PowerDistribution, DataLogManager

import ports
from subsystems.intake import Intake


class DiagnoseGrabMotor(Command):
    def __init__(self, intake: Intake, pdp: PowerDistribution):
        super().__init__()
        self.addRequirements(intake, pdp)
        self.intake = intake
        self.pdp = pdp
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.restart()
        self.max_value = 0.0
        if self.pdp.getCurrent(ports.PDP.intake_grab_motor) > 0.1:
            DataLogManager.log(
                f"Intake diagnostics: Grab motor current measured too high. {self.pdp.getCurrent(ports.PDP.intake_grab_motor)}"
            )
            self.intake.alert_grab_motor_hi.set(True)

    def execute(self):
        self.intake.grab()
        self.max_value = max(self.max_value, self.pdp.getCurrent(ports.PDP.intake_grab_motor))

    def end(self, interrupted: bool):
        self.intake.stopGrab()
        if self.pdp.getCurrent(ports.PDP.intake_grab_motor) > 0.1:
            DataLogManager.log(
                f"Intake diagnostics: Grab motor current measured too high. {self.pdp.getCurrent(ports.PDP.intake_grab_motor)}"
            )
            self.intake.alert_grab_motor_hi.set(True)

        if self.max_value < 0.1:
            DataLogManager.log(
                f"Intake diagnostics: Grab motor current measured too low. {self.max_value}"
            )
            self.intake.alert_grab_motor_lo.set(True)

    def isFinished(self) -> bool:
        return self.timer.get() > 1
