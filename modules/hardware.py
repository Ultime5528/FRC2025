import commands2
from commands2.button import Trigger

from commands.claw.loadcoral import LoadCoral
from commands.elevator.maintainelevator import MaintainElevator
from subsystems.arm import Arm
from subsystems.claw import Claw
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

        self.claw = Claw()
        Trigger(self.claw.hasCoralInLoader).onTrue(LoadCoral(self.claw))

        self.arm = Arm()

        self.printer = Printer()

        self.controller = commands2.button.CommandXboxController(0)

        self.subsystems: list[Subsystem] = [
            self.drivetrain,
            self.elevator,
            self.claw,
            self.arm,
            self.printer,
        ]
