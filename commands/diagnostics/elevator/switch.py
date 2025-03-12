from commands2 import SequentialCommandGroup
from commands2.cmd import runOnce

from commands.elevator.moveelevator import MoveElevator
from commands.elevator.resetelevator import ResetElevator
from subsystems.elevator import Elevator
from ultime.command import ignore_requirements
from ultime.proxy import proxy


@ignore_requirements(["elevator"])
class DiagnoseSwitch(SequentialCommandGroup):
    def __init__(self, elevator: Elevator):
        super().__init__(
            runOnce(proxy(self.before_test)),
            MoveElevator.toLevel1(elevator),
            runOnce(proxy(self.after_level1)),
            ResetElevator(elevator),
        )
        self.elevator = elevator

    def before_test(self):
        if not self.elevator.isDown():
            self.elevator.alert_is_down.set(True)

    def after_level1(self):
        if self.elevator.isUp():
            self.elevator.alert_is_up.set(True)
        if self.elevator.isDown():
            self.elevator.alert_is_down.set(True)
