from commands2 import (
    SequentialCommandGroup,
    WaitCommand,
    FunctionalCommand,
)
from commands2.cmd import runOnce, parallel, sequence
from wpilib import RobotController, DataLogManager, PowerDistribution

import ports
from commands.arm.extendarm import ExtendArm
from commands.arm.retractarm import RetractArm
from commands.elevator.moveelevator import MoveElevator
from commands.elevator.resetelevator import ResetElevator
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from ultime.autoproperty import autoproperty
from ultime.command import ignore_requirements
from ultime.proxy import proxy


@ignore_requirements(["arm", "elevator"])
class DiagnoseArmMotor(SequentialCommandGroup):
    def __init__(self, arm: Arm, elevator: Elevator, pdp: PowerDistribution):
        super().__init__(
            runOnce(proxy(self.before_command)),
            MoveElevator.toLevel1(elevator),
            parallel(
                ExtendArm(arm),
                sequence(
                    WaitCommand(0.1),
                    FunctionalCommand(
                        lambda: None,
                        proxy(self.while_extending),
                        lambda _: None,
                        proxy(self.is_arm_extended),
                    ),
                ),
            ),
            WaitCommand(0.1),
            RetractArm(arm),
            ResetElevator(elevator),
            runOnce(proxy(self.before_command)),
        )
        self.arm = arm
        self.pdp = pdp

    def before_command(self):
        self.arm.stop()
        if self.pdp.getCurrent(ports.PDP.arm_motor) > 0.1:
            DataLogManager.log(
                f"Arm diagnostics: Motor current measured too high. {self.pdp.getCurrent(ports.PDP.arm_motor)}"
            )
            self.arm.alert_motor_hi.set(True)

    def while_extending(self):
        if self.pdp.getCurrent(ports.PDP.arm_motor) < 0.1:
            DataLogManager.log(
                f"Arm diagnostics: Motor current measured too low. {self.pdp.getCurrent(ports.PDP.arm_motor)}"
            )
            self.arm.alert_motor_lo.set(True)

    def is_arm_extended(self):
        return self.arm.state == Arm.State.Extended
