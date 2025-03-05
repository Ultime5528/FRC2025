from commands2 import ParallelCommandGroup, InstantCommand

from commands.printer.resetprinter import ResetPrinterRight
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.intake import Intake
from subsystems.printer import Printer
from subsystems.climber import Climber
from ultime.command import ignore_requirements


@ignore_requirements(["elevator", "printer", "arm", "intake", "climber"])
class ResetAutonomous(ParallelCommandGroup):
    def __init__(
        self,
        elevator: Elevator,
        printer: Printer,
        arm: Arm,
        intake: Intake,
        climber: Climber,
    ):
        super().__init__(
            InstantCommand(lambda: elevator.setReset()),
            InstantCommand(lambda: intake.setReset()),
            InstantCommand(lambda: arm.setReset()),
            InstantCommand(lambda: climber.setReset()),
            ResetPrinterRight(printer),
        )
