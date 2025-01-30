from _weakref import proxy

import commands2
import wpilib

from commands.elevator.moveelevator import MoveElevator
from commands.elevator.resetelevator import ResetElevator
from modules.hardware import HardwareModule
from ultime.module import Module
from ultime.subsystem import Subsystem


class DashboardModule(Module):
    def __init__(self, hardware: HardwareModule):
        super().__init__()

        for subsystem in hardware.subsystems:
            putSubsystemOnDashboard(subsystem)

        # Classer par subsystem
        # putCommandOnDashboard("Drivetrain", Command(...))
        putCommandOnDashboard("Elevator", ResetElevator(hardware.elevator))
        putCommandOnDashboard("Elevator", MoveElevator.toLevel4(hardware.elevator))
        putCommandOnDashboard("Elevator", MoveElevator.toLevel2(hardware.elevator))


        for subsystem in self._hardware.subsystems:
            wpilib.SmartDashboard.putData(subsystem.getName(), subsystem)

        for module in self._module_list.modules:
            if module.redefines_init_sendable:
                """
                If a module keeps a reference to a subsystem or the HardwareModule,
                it should be wrapped in a weakref.proxy(). For example,
                self.hardware = proxy(hardware)
                """
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


def putSubsystemOnDashboard(subsystem: Subsystem, name: str = None):
    if name is None:
        name = subsystem.getName()

    wpilib.SmartDashboard.putData(name, subsystem)
