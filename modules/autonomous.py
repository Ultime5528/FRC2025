from typing import Optional

import commands2
import wpilib
from pathplannerlib.auto import AutoBuilder, NamedCommands

from ultime.module import Module


class AutonomousModule(Module):
    def __init__(self):
        super().__init__()

        self.auto_command: Optional[commands2.Command] = None

        self.auto_chooser = AutoBuilder.buildAutoChooser()
        wpilib.SmartDashboard.putData("Autonomous mode", self.auto_chooser)

        self.auto_chooser.setDefaultOption("Nothing", None)

    def setupCommandsOnPathPlanner(self):
        NamedCommands.registerCommand(
            "print_shizzle", commands2.PrintCommand("shizzle")
        )
        NamedCommands.registerCommand(
            "print_bingus", commands2.PrintCommand("bingus")
        )

    def autonomousInit(self):
        self.auto_command: commands2.Command = self.auto_chooser.getSelected()
        if self.auto_command:
            self.auto_command.schedule()

    def autonomousExit(self):
        if self.auto_command:
            self.auto_command.cancel()
