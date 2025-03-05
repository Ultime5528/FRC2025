from commands2 import SequentialCommandGroup
from commands2.cmd import runOnce

from commands.elevator.moveelevator import MoveElevator
from commands.elevator.resetelevator import ResetElevator
from subsystems.elevator import Elevator
from ultime.command import ignore_requirements


@ignore_requirements(["elevator"])
class DiagnoseSwitch(SequentialCommandGroup):
    def __init__(self, elevator: Elevator):
        super().__init__(
            runOnce(
                lambda: elevator.alert_is_down.set(not elevator.isDown())
            ),  # Elevator should be down and so should the limit switch
            MoveElevator.toLevel1(elevator),
            runOnce(
                lambda: elevator.alert_is_up.set(elevator.isDown())
            ),  # Elevator should be up and so should the limit switch
            runOnce(
                lambda: elevator.alert_is_down.set(
                    elevator.alert_is_down.get() or not elevator.isDown()
                )
            ),  # Elevator shouldn't be down and so shouldn't the limit switch
            ResetElevator(elevator),
        )
