from commands.printer.resetright import ResetPrinterRight
from commands2 import SequentialCommandGroup
from commands2.cmd import parallel

from commands.arm.retractarm import RetractArm
from commands.climber.resetclimber import ResetClimber
from commands.elevator.manualmoveelevator import ManualMoveElevator
from commands.elevator.resetelevator import ResetElevator
from commands.intake.resetintake import ResetIntake
from subsystems.arm import Arm
from subsystems.climber import Climber
from subsystems.elevator import Elevator
from subsystems.intake import Intake
from subsystems.printer import Printer
from ultime.command import ignore_requirements


@ignore_requirements(["elevator", "printer", "arm", "intake", "climber"])
class ResetAll(SequentialCommandGroup):
    def __init__(
        self,
        elevator: Elevator,
        printer: Printer,
        arm: Arm,
        intake: Intake,
        climber: Climber,
    ):
        super().__init__(
            ManualMoveElevator.up(elevator).withTimeout(0.5),
            RetractArm(arm),
            parallel(
                ResetElevator(elevator),
                ResetPrinterRight(printer),
                ResetIntake(intake),
                ResetClimber(climber),
            ),
        )
