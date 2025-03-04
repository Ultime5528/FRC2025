from commands2 import SequentialCommandGroup, ParallelCommandGroup, FunctionalCommand
from wpilib import RobotController

from commands.arm.extendarm import ExtendArm
from commands.arm.retractarm import RetractArm
from commands.diagnostics.utils.runonce import RunOnce
from commands.elevator.moveelevator import MoveElevator
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from ultime.autoproperty import autoproperty
from ultime.command import ignore_requirements, WaitCommand


@ignore_requirements(["arm", "elevator"])
class DiagnoseArmMotor(SequentialCommandGroup):
    voltage_change_threshold = autoproperty(0.5)

    def __init__(self, arm: Arm, elevator: Elevator):
        super().__init__(
            RunOnce(self.before_command),
            MoveElevator.toLevel1(elevator),
            ParallelCommandGroup(
                ExtendArm(arm),
                SequentialCommandGroup(
                    WaitCommand(0.1),
                    FunctionalCommand(
                        lambda: None,
                        self.while_extending,
                        lambda interrupted: None,
                        lambda: arm.state == arm.State.Extended,
                    ),
                ),
            ),
            WaitCommand(0.1),
            RetractArm(arm),
        )
        self.arm = arm
        self.voltage_before = None
        self.voltage_during = None
        self.voltage_after = None

    def before_command(self):
        print("before_command")
        self.voltage_before = RobotController.getBatteryVoltage()
        self.arm.stop()

    def while_extending(self):
        print("while_extending")
        self.voltage_during = RobotController.getBatteryVoltage()

    def end(self, interrupted: bool):
        super().end(interrupted)
        self.voltage_after = RobotController.getBatteryVoltage()
        self.arm.stop()
        voltage_delta_before = self.voltage_before - self.voltage_during
        voltage_delta_after = self.voltage_after - self.voltage_during
        print("Voltage delta before:", voltage_delta_before)
        print("Voltage delta after:", voltage_delta_after)
        if voltage_delta_before < self.voltage_change_threshold:
            self.arm.alert_motor.set(True)
        elif voltage_delta_after < self.voltage_change_threshold:
            self.arm.alert_motor.set(True)
