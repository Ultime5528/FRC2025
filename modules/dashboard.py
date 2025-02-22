import math

import commands2
import wpilib
from commands2 import DeferredCommand
from wpimath.geometry import Pose2d, Transform2d, Translation2d, Rotation2d

from commands.alignwithreefside import AlignWithReefSide
from commands.arm.extendarm import ExtendArm
from commands.arm.retractarm import RetractArm
from commands.claw.autodrop import AutoDrop
from commands.claw.drop import Drop
from commands.claw.loadcoral import LoadCoral
from commands.climber.moveclimber import Climb, ReadyClimber, ReleaseClimber
from commands.climber.resetclimber import ResetClimber
from commands.completedropsequence import CompleteDropSequence
from commands.drivetrain.drivetoposes import DriveToPoses
from commands.drivetrain.resetgyro import ResetGyro
from commands.elevator.maintainelevator import MaintainElevator
from commands.elevator.manualmoveelevator import ManualMoveElevator
from commands.elevator.moveelevator import MoveElevator
from commands.elevator.resetelevator import ResetElevator
from commands.intake.dropalgae import DropAlgae
from commands.intake.grabalgae import GrabAlgae
from commands.intake.moveintake import MoveIntake
from commands.intake.resetintake import ResetIntake
from commands.prepareloading import PrepareLoading
from commands.printer.manualmoveprinter import ManualMovePrinter
from commands.printer.moveprinter import MovePrinter
from commands.printer.resetprinter import ResetPrinterRight
from commands.printer.scanprinter import ScanPrinter
from commands.resetall import ResetAll
from modules.hardware import HardwareModule
from ultime.module import Module, ModuleList


class DashboardModule(Module):
    def __init__(self, hardware: HardwareModule, module_list: ModuleList):
        super().__init__()
        self._hardware = hardware
        self._module_list = module_list

        putCommandOnDashboard("Drivetrain", AlignWithReefSide(hardware.drivetrain))

        """
        Elevator
        """
        putCommandOnDashboard("Elevator", ResetElevator(hardware.elevator))
        putCommandOnDashboard("Elevator", MaintainElevator(hardware.elevator))
        putCommandOnDashboard("Elevator", ManualMoveElevator.down(hardware.elevator))
        putCommandOnDashboard("Elevator", ManualMoveElevator.up(hardware.elevator))
        putCommandOnDashboard("Elevator", MoveElevator.toLevel1(hardware.elevator))
        putCommandOnDashboard("Elevator", MoveElevator.toLevel2(hardware.elevator))
        putCommandOnDashboard("Elevator", MoveElevator.toLevel2Algae(hardware.elevator))
        putCommandOnDashboard("Elevator", MoveElevator.toLevel3(hardware.elevator))
        putCommandOnDashboard("Elevator", MoveElevator.toLevel3Algae(hardware.elevator))
        putCommandOnDashboard("Elevator", MoveElevator.toLevel4(hardware.elevator))
        putCommandOnDashboard(
            "Elevator",
            MoveElevator.toAlgae(hardware.elevator, hardware.arm, hardware.drivetrain),
        )
        putCommandOnDashboard("Elevator", MoveElevator.toLoading(hardware.elevator))

        """
        Printer
        """
        putCommandOnDashboard("Printer", ResetPrinterRight(hardware.printer))
        putCommandOnDashboard("Printer", ManualMovePrinter.left(hardware.printer))
        putCommandOnDashboard("Printer", ManualMovePrinter.right(hardware.printer))
        putCommandOnDashboard("Printer", MovePrinter.toLeft(hardware.printer))
        putCommandOnDashboard("Printer", MovePrinter.toMiddleLeft(hardware.printer))
        putCommandOnDashboard("Printer", MovePrinter.toMiddle(hardware.printer))
        putCommandOnDashboard("Printer", MovePrinter.toMiddleRight(hardware.printer))
        putCommandOnDashboard("Printer", MovePrinter.toRight(hardware.printer))
        putCommandOnDashboard("Printer", MovePrinter.toLoading(hardware.printer))
        putCommandOnDashboard("Printer", MovePrinter.leftUntilReef(hardware.printer))
        putCommandOnDashboard("Printer", MovePrinter.rightUntilReef(hardware.printer))
        putCommandOnDashboard("Printer", ScanPrinter.left(hardware.printer))
        putCommandOnDashboard("Printer", ScanPrinter.right(hardware.printer))

        """
        Claw
        """
        putCommandOnDashboard("Claw", Drop.atLevel1(hardware.claw))
        putCommandOnDashboard("Claw", Drop.atLevel2(hardware.claw))
        putCommandOnDashboard("Claw", Drop.atLevel3(hardware.claw))
        putCommandOnDashboard("Claw", Drop.atLevel4(hardware.claw))
        putCommandOnDashboard("Claw", AutoDrop(hardware.claw, hardware.elevator))
        putCommandOnDashboard("Claw", LoadCoral(hardware.claw))

        """
        Arm
        """
        putCommandOnDashboard("Arm", RetractArm(hardware.arm))
        putCommandOnDashboard("Arm", ExtendArm(hardware.arm))

        """
        Climber
        """
        putCommandOnDashboard("Climber", ReadyClimber(hardware.climber))
        putCommandOnDashboard("Climber", Climb(hardware.climber))
        putCommandOnDashboard("Climber", ReleaseClimber(hardware.climber))
        putCommandOnDashboard("Climber", ResetClimber(hardware.climber))

        """
        Intake
        """
        putCommandOnDashboard("Intake", DropAlgae(hardware.intake))
        putCommandOnDashboard("Intake", GrabAlgae(hardware.intake))
        putCommandOnDashboard("Intake", MoveIntake.toExtended(hardware.intake))
        putCommandOnDashboard("Intake", MoveIntake.toRetracted(hardware.intake))
        putCommandOnDashboard("Intake", ResetIntake(hardware.intake))
        """
        Groups
        """
        putCommandOnDashboard("Drivetrain", ResetGyro(hardware.drivetrain))

        """
        Groups
        """
        putCommandOnDashboard(
            "Group",
            ResetAll(
                hardware.elevator,
                hardware.printer,
                hardware.arm,
                hardware.intake,
                hardware.climber,
            ),
        )
        putCommandOnDashboard(
            "Group", PrepareLoading(hardware.elevator, hardware.arm, hardware.printer)
        )
        putCommandOnDashboard(
            "Group",
            CompleteDropSequence.toLeft(
                hardware.printer, hardware.arm, hardware.elevator, hardware.drivetrain, hardware.claw
            ),
        )
        putCommandOnDashboard(
            "Group",
            CompleteDropSequence.toRight(
                hardware.printer, hardware.arm, hardware.elevator, hardware.drivetrain, hardware.claw
            ),
        )

    def robotInit(self) -> None:
        for subsystem in self._hardware.subsystems:
            wpilib.SmartDashboard.putData(subsystem.getName(), subsystem)

        wpilib.SmartDashboard.putData("Gyro", self._hardware.drivetrain._gyro)

        for module in self._module_list.modules:
            if module.redefines_init_sendable:
                """
                If a module keeps a reference to a subsystem or the HardwareModule,
                it should be wrapped in a weakref.proxy(). For example,
                self.hardware = proxy(hardware)
                """
                print("Putting on dashboard:", module.getName())
                wpilib.SmartDashboard.putData(module.getName(), module)


def putCommandOnDashboard(
    sub_table: str, cmd: commands2.Command, name: str = None, suffix: str = " commands"
) -> commands2.Command:
    if not isinstance(sub_table, str):
        raise ValueError(
            f"sub_table should be a str: '{sub_table}' of type '{type(sub_table)}'"
        )

    if suffix:
        sub_table += suffix

    sub_table += "/"

    if name is None:
        name = cmd.getName()
    else:
        cmd.setName(name)

    wpilib.SmartDashboard.putData(sub_table + name, cmd)

    return cmd
