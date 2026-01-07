from _weakref import proxy
from typing import Optional

import commands2
from commands2 import Command
from pathplannerlib.auto import NamedCommands, AutoBuilder
from pathplannerlib.config import RobotConfig, PIDConstants
from pathplannerlib.controller import PPHolonomicDriveController
from wpilib import DriverStation, SmartDashboard

from commands.alignwithreefside import AlignWithReefSide
from commands.arm.extendarm import ExtendArm
from commands.arm.retractarm import RetractArm
from commands.claw.loadcoral import LoadCoral
from commands.claw.retractcoral import RetractCoral
from commands.claw.waituntilcoral import WaitUntilCoral
from commands.climber.resetclimber import ResetClimber
from commands.dropautonomous import DropAutonomous
from commands.dropprepareloading import DropPrepareLoading
from commands.elevator.moveelevator import MoveElevator
from commands.prepareloading import PrepareLoading
from commands.printer.moveprinter import MovePrinter
from commands.resetall import ResetAll
from commands.resetallbutclimber import ResetAllButClimber
from commands.resetautonomous import ResetAutonomous
from modules.hardware import HardwareModule
from ultime.module import Module
from ultime.autoproperty import autoproperty


def registerNamedCommand(command: Command):
    NamedCommands.registerCommand(command.getName(), command)


class AutonomousModule(Module):

    kp = autoproperty(5)
    ki = autoproperty(0)
    kd = autoproperty(0)

    def __init__(self, hardware: HardwareModule):
        super().__init__()
        self.hardware = proxy(hardware)

        self.auto_command: Optional[commands2.Command] = None

        config = RobotConfig.fromGUISettings()

        AutoBuilder.configure(
            hardware.drivetrain.getPose,
            hardware.drivetrain.resetToPose,
            hardware.drivetrain.getRobotRelativeChassisSpeeds,
            lambda speeds, feedforwards: hardware.drivetrain.driveFromChassisSpeedsFF(
                speeds, feedforwards
            ),
            PPHolonomicDriveController(
                PIDConstants(self.kp, self.ki, self.kd),
                PIDConstants(self.kp, self.ki, self.kd),
            ),
            config,
            self.shouldFlipPath,
            hardware.drivetrain,
        )

        self.auto_chooser = AutoBuilder.buildAutoChooser()
        SmartDashboard.putData("AutoChooser", self.auto_chooser)

    def shouldFlipPath(self):
        return DriverStation.getAlliance() == DriverStation.Alliance.kRed

    def setupCommandsOnPathPlanner(self):
        registerNamedCommand(
            ResetAutonomous(
                self.hardware.elevator, self.hardware.printer, self.hardware.arm
            )
        )
        registerNamedCommand(RetractCoral.retract(self.hardware.claw))
        registerNamedCommand(LoadCoral(self.hardware.claw, self.hardware.printer))
        registerNamedCommand(WaitUntilCoral(self.hardware.claw))
        registerNamedCommand(AlignWithReefSide(self.hardware.drivetrain))
        registerNamedCommand(RetractArm(self.hardware.arm))
        registerNamedCommand(ExtendArm(self.hardware.arm))
        registerNamedCommand(ResetClimber(self.hardware.climber))
        registerNamedCommand(MovePrinter.toMiddleRight(self.hardware.printer))
        registerNamedCommand(MovePrinter.toMiddleLeft(self.hardware.printer))
        registerNamedCommand(MoveElevator.toLevel4(self.hardware.elevator))
        registerNamedCommand(MoveElevator.toLevel1(self.hardware.elevator))
        registerNamedCommand(MoveElevator.toLevel2(self.hardware.elevator))
        registerNamedCommand(MoveElevator.toLevel3(self.hardware.elevator))
        registerNamedCommand(MovePrinter.toLoading(self.hardware.printer))
        registerNamedCommand(
            ResetAll(
                self.hardware.elevator,
                self.hardware.printer,
                self.hardware.arm,
                self.hardware.intake,
                self.hardware.climber,
            )
        )
        registerNamedCommand(
            ResetAllButClimber(
                self.hardware.elevator,
                self.hardware.printer,
                self.hardware.arm,
                self.hardware.intake,
            )
        )
        registerNamedCommand(
            DropPrepareLoading.toRight(
                self.hardware.printer,
                self.hardware.arm,
                self.hardware.elevator,
                self.hardware.drivetrain,
                self.hardware.claw,
                self.hardware.controller,
                True,
            )
        )
        registerNamedCommand(
            DropPrepareLoading.toLeft(
                self.hardware.printer,
                self.hardware.arm,
                self.hardware.elevator,
                self.hardware.drivetrain,
                self.hardware.claw,
                self.hardware.controller,
                True,
            )
        )
        registerNamedCommand(
            DropAutonomous.toLeft(
                self.hardware.printer,
                self.hardware.arm,
                self.hardware.elevator,
                self.hardware.drivetrain,
                self.hardware.claw,
                True,
            )
        )
        registerNamedCommand(
            DropAutonomous.toRight(
                self.hardware.printer,
                self.hardware.arm,
                self.hardware.elevator,
                self.hardware.drivetrain,
                self.hardware.claw,
                True,
            )
        )
        registerNamedCommand(
            PrepareLoading(
                self.hardware.elevator, self.hardware.arm, self.hardware.printer
            )
        )

    def autonomousInit(self):
        self.hardware.drivetrain.swerve_odometry.resetPose(
            self.hardware.drivetrain.getPose()
        )

        self.auto_command: commands2.Command = self.auto_chooser.getSelected()
        if self.auto_command:
            self.auto_command.schedule()

    def autonomousExit(self):
        if self.auto_command:
            self.auto_command.cancel()
