from commands2 import SequentialCommandGroup
from commands2.cmd import parallel

from commands.arm.retractarm import RetractArm
from commands.elevator.manualmoveelevator import ManualMoveElevator
from commands.elevator.resetelevator import ResetElevator
from commands.intake.resetintake import ResetIntake
from commands.printer.resetprinter import ResetPrinterRight
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.intake import Intake
from subsystems.printer import Printer
from ultime.command import ignore_requirements


@ignore_requirements(["elevator", "printer", "arm", "intake"])
class ResetAllButClimber(SequentialCommandGroup):
    def __init__(
        self,
        elevator: Elevator,
        printer: Printer,
        arm: Arm,
        intake: Intake,
    ):
        super().__init__(
            parallel(
                ManualMoveElevator.up(elevator).withTimeout(1.5),
            ),
            RetractArm(arm),
            parallel(
                ResetPrinterRight(printer),
                ResetElevator(elevator),
                ResetIntake(intake),
            ),
        )
