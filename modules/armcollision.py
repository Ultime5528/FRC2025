from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.module import Module


class ArmCollision(Module):
    def __init__(self, arm: Arm, printer: Printer, elevator: Elevator):
        super().__init__()

        self.arm = arm
        self.printer = printer
        self.elevator = elevator

    def autonomousInit(self) -> None:
        pass

    def autonomousPeriodic(self) -> None:
        pass

    def autonomousExit(self) -> None:
        pass

    def teleopInit(self) -> None:
        pass

    def teleopPeriodic(self) -> None:
        if

    def teleopExit(self) -> None:
        pass
