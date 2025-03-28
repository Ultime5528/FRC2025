from commands2 import (
    SequentialCommandGroup,
    WaitCommand,
    FunctionalCommand,
)
from commands2.cmd import runOnce, parallel, sequence
from wpilib import RobotController, DataLogManager

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
    voltage_change_threshold = autoproperty(0.5)

    def __init__(self, arm: Arm, elevator: Elevator):
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
        )
        self.arm = arm
        self.voltage_before = None
        self.voltage_during = None
        self.voltage_after = None

    def before_command(self):
        self.voltage_before = RobotController.getBatteryVoltage()
        self.arm.stop()

    def while_extending(self):
        self.voltage_during = RobotController.getBatteryVoltage()

    def is_arm_extended(self):
        return self.arm.state == Arm.State.Extended

    def end(self, interrupted: bool):
        super().end(interrupted)
        self.voltage_after = RobotController.getBatteryVoltage()
        self.arm.stop()
        voltage_delta_before = self.voltage_before - self.voltage_during
        voltage_delta_after = self.voltage_after - self.voltage_during
        DataLogManager.log(
            "Arm diagnostics: voltage delta before" + str(voltage_delta_before)
        )
        DataLogManager.log(
            "Arm diagnostics: voltage delta after" + str(voltage_delta_after)
        )
        if (
            voltage_delta_before < self.voltage_change_threshold
            or voltage_delta_after < self.voltage_change_threshold
        ):
            self.arm.alert_motor.set(True)
