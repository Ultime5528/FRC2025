from commands2 import SequentialCommandGroup

from commands.diagnostics.arm.armmotor import DiagnoseArmMotor
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from ultime.command import ignore_requirements


@ignore_requirements(["arm", "elevator"])
class DiagnoseArm(SequentialCommandGroup):
    def __init__(self, arm: Arm, elevator: Elevator):
        super().__init__(DiagnoseArmMotor(arm, elevator))
