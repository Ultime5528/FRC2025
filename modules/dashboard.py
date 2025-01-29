import commands2
import wpilib

from commands.elevator.moveelevator import MoveElevator
from commands.elevator.resetelevator import ResetElevator
from modules.hardware import HardwareModule
from ultime.module import Module, ModuleList


class DashboardModule(Module):
    def __init__(self, hardware: HardwareModule, module_list: ModuleList):
        super().__init__()
        self._hardware = hardware
        self._module_list = module_list

        # Classer par subsystem
        # putCommandOnDashboard("Drivetrain", Command(...))
        putCommandOnDashboard("Elevator", ResetElevator(hardware.elevator))
        putCommandOnDashboard("Elevator", MoveElevator.toLevel4(hardware.elevator))
        putCommandOnDashboard("Elevator", MoveElevator.toLevel2(hardware.elevator))

    def robotInit(self) -> None:
        components = self._hardware.subsystems + self._module_list.modules

        for component in components:
            wpilib.SmartDashboard.putData(component.getName(), component)


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
