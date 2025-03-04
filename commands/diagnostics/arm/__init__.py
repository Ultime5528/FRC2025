from commands2 import SequentialCommandGroup

from commands.diagnostics.arm.armmotor import DiagnoseArmMotor
from subsystems.arm import Arm
from subsystems.elevator import Elevator


class DiagnoseArm(SequentialCommandGroup):
    def __init__(self, arm: Arm, elevator: Elevator):
        super().__init__(
            DiagnoseArmMotor(arm, elevator)
        )