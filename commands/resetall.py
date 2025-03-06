from commands2 import ParallelCommandGroup

from commands.climber.resetclimber import ResetClimber
from commands.resetallbutclimber import ResetAllButClimber
from subsystems.arm import Arm
from subsystems.climber import Climber
from subsystems.elevator import Elevator
from subsystems.intake import Intake
from subsystems.printer import Printer
from ultime.command import ignore_requirements


@ignore_requirements(["elevator", "printer", "arm", "intake", "climber"])
class ResetAll(ParallelCommandGroup):
    def __init__(
        self,
        elevator: Elevator,
        printer: Printer,
        arm: Arm,
        intake: Intake,
        climber: Climber,
    ):
        super().__init__(
            ResetAllButClimber(elevator, printer, arm, intake),
            ResetClimber(climber),
        )
