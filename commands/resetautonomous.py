from commands2 import InstantCommand, SequentialCommandGroup
from commands2.cmd import parallel

from commands.elevator.resetelevator import ResetElevator
from commands.printer.resetprinter import ResetPrinterRight
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.command import ignore_requirements


@ignore_requirements(["elevator", "printer", "arm", "intake", "climber"])
class ResetAutonomous(SequentialCommandGroup):
    def __init__(
        self,
        elevator: Elevator,
        printer: Printer,
        arm: Arm,
    ):
        def setArmRetracted():
            arm.state = Arm.State.Retracted

        super().__init__(
            InstantCommand(setArmRetracted),
            parallel(
                ResetPrinterRight(printer),
                ResetElevator(elevator),
            ),
        )
