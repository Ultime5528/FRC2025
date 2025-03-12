import wpilib
from commands2 import Command
from wpilib import RobotController, DataLogManager, PowerDistribution

import ports
from commands.claw.drop import drop_properties
from subsystems.claw import Claw
from ultime.autoproperty import autoproperty


class DiagnoseLeftMotor(Command):
    voltage_change_threshold = autoproperty(0.5)

    def __init__(self, claw: Claw, pdp: PowerDistribution):
        super().__init__()
        self.addRequirements(claw)
        self.pdp = pdp
        self.claw = claw
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.restart()
        self.claw.stop()

    def execute(self):
        if self.timer.get() < 0.1:
            self.claw.setLeft(0)
            if self.pdp.getCurrent(ports.PDP.claw_motor_left) > 0.1:
                DataLogManager.log(
                    f"Claw diagnostics: Left motor current measured too high. {self.pdp.getCurrent(ports.PDP.claw_motor_left)}"
                )
                self.claw.alert_left_motor_hi.set(True)
        elif self.timer.get() < 1:
            self.claw.setLeft(drop_properties.speed_level_4_left)
            if self.pdp.getCurrent(ports.PDP.claw_motor_left) < 0.1:
                DataLogManager.log(
                    f"Claw diagnostics: Left motor current measured too low. {self.pdp.getCurrent(ports.PDP.claw_motor_left)}"
                )
                self.claw.alert_left_motor_lo.set(True)
        elif self.timer.get() < 2:
            self.claw.setLeft(0)
            if self.pdp.getCurrent(ports.PDP.claw_motor_left) > 0.1:
                DataLogManager.log(
                    f"Claw diagnostics: Left motor current measured too high. {self.pdp.getCurrent(ports.PDP.claw_motor_left)}"
                )
                self.claw.alert_left_motor_hi.set(True)

    def isFinished(self) -> bool:
        return self.timer.get() > 2

    def end(self, interrupted: bool):
        self.claw.stop()
