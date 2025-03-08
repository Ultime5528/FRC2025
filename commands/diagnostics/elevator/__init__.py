from commands2 import SequentialCommandGroup
from wpilib import PowerDistribution

from commands.diagnostics.elevator.motor import DiagnoseMotor
from commands.diagnostics.elevator.switch import DiagnoseSwitch
from subsystems.elevator import Elevator
from ultime.command import ignore_requirements


@ignore_requirements(["elevator"])
class DiagnoseElevator(SequentialCommandGroup):
    def __init__(self, elevator: Elevator, pdp: PowerDistribution):
        super().__init__(DiagnoseSwitch(elevator), DiagnoseMotor(elevator, pdp))
