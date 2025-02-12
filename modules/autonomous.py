from typing import Optional

import commands2
import wpilib
from pathplannerlib.auto import AutoBuilder, NamedCommands

from commands.claw.loadcoral import LoadCoral
from commands.elevator.moveelevator import MoveElevator
from commands.printer.moveprinter import MovePrinter
from modules.hardware import HardwareModule
from ultime.module import Module


class AutonomousModule(Module):
    def __init__(self, hardware: HardwareModule):
        super().__init__()
        self.hardware = hardware

        self.setupCommandsOnPathPlanner()

        self.auto_command: Optional[commands2.Command] = None

        self.auto_chooser = AutoBuilder.buildAutoChooser()
        wpilib.SmartDashboard.putData("Autonomous mode", self.auto_chooser)

        self.auto_chooser.setDefaultOption("Nothing", None)



    def setupCommandsOnPathPlanner(self):
        NamedCommands.registerCommand(
            "Printer.toLoading", MovePrinter.toLoading(self.hardware.printer)
        )
        NamedCommands.registerCommand(
            "MoveElevator.toLevel1", MoveElevator.toLevel1(self.hardware.elevator)
        )


    def autonomousInit(self):
        self.auto_command: commands2.Command = self.auto_chooser.getSelected()
        if self.auto_command:
            self.auto_command.schedule()

    def autonomousExit(self):
        if self.auto_command:
            self.auto_command.cancel()
