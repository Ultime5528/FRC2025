from sys import modules
from typing import Optional

import commands2
import wpilib

from ultime.module import Module


class AutonomousModule(Module):
    def __init__(self):
        super().__init__()

        self.auto_command: Optional[commands2.Command] = None

        self.auto_chooser = wpilib.SendableChooser()
        wpilib.SmartDashboard.putData("Autonomous mode", self.auto_chooser)

        self.auto_chooser.setDefaultOption("Nothing", None)

        # self.auto_chooser.addOption(
        #     Auto1.__name__,
        #     CenterShoot(
        #         self.drivetrain, self.shooter, self.pivot, self.intake, self.vision
        #     ),
        # )

    def autonomousInit(self):
        self.auto_command: commands2.Command = self.auto_chooser.getSelected()
        if self.auto_command:
            self.auto_command.schedule()

    def autonomousExit(self):
        if self.auto_command:
            self.auto_command.cancel()
