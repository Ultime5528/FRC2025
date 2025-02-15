from commands2 import SequentialCommandGroup, ParallelCommandGroup

from commands.arm.retractarm import RetractArm
from commands.elevator.moveelevator import MoveElevator
from commands.elevator.resetelevator import ResetElevator
from commands.intake.resetintake import ResetIntake
from commands.printer.resetright import ResetPrinterRight
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.intake import Intake
from subsystems.printer import Printer


class ResetAll(SequentialCommandGroup):
    def __init__(self, elevator: Elevator, printer: Printer, arm: Arm, intake: Intake):
        super().__init__(
            ParallelCommandGroup(
                ResetElevator(elevator),
                ResetPrinterRight(printer),
            ),
            MoveElevator.toLevel1(elevator),
            ParallelCommandGroup(
                RetractArm(arm),
                # ResetClimber,
                ResetIntake(intake),
            ),
            MoveElevator.toLoading(elevator),
        )
