import commands2

from commands.elevator.maintainelevator import MaintainElevator
from subsystems.drivetrain import Drivetrain
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.module import Module
from ultime.subsystem import Subsystem


class HardwareModule(Module):
    def __init__(self):
        super().__init__()
        self.drivetrain = Drivetrain()

        self.elevator = Elevator()
        self.elevator.setDefaultCommand(MaintainElevator(self.elevator))

        self.controller = commands2.button.CommandXboxController(0)
        self.printer = Printer()

        self.subsystems: list[Subsystem] = [
            self.drivetrain,
            self.printer,
            self.elevator,
        ]
