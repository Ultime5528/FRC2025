import commands2
import wpilib

from modules.hardware import HardwareModule
from ultime.module import Module
from ultime.subsystem import Subsystem
from commands.elevator.resetelevator import ResetElevatorDown
from commands.elevator.moveelevator import MoveElevator


class DashboardModule(Module):
    def __init__(self, hardware: HardwareModule):
        super().__init__()

        for subsystem in hardware.subsystems:
            putSubsystemOnDashboard(subsystem)

        # Classer par subsystem
        # putCommandOnDashboard("Drivetrain", Command(...))
        putCommandOnDashboard("Elevator", ResetElevatorDown(hardware.elevator))
        putCommandOnDashboard("Elevator", MoveElevator.toLevel4(hardware.elevator))
        putCommandOnDashboard("Elevator", MoveElevator.toLevel2(hardware.elevator))


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


def putSubsystemOnDashboard(subsystem: Subsystem, name: str = None):
    if name is None:
        name = subsystem.getName()

    wpilib.SmartDashboard.putData(name, subsystem)
