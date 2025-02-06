import commands2
import wpilib

from commands.arm.extendarm import ExtendArm
from commands.arm.retractarm import RetractArm
from commands.claw.drop import Drop
from commands.elevator.maintainelevator import MaintainElevator
from commands.elevator.manualmoveelevator import ManualMoveElevator
from commands.elevator.moveelevator import MoveElevator
from commands.elevator.resetelevator import ResetElevator
from commands.printer.manualmoveprinter import ManualMovePrinter
from commands.printer.moveprinter import MovePrinter
from commands.printer.resetright import ResetPrinterRight
from modules.hardware import HardwareModule
from ultime.module import Module, ModuleList


class DashboardModule(Module):
    def __init__(self, hardware: HardwareModule, module_list: ModuleList):
        super().__init__()
        self._hardware = hardware
        self._module_list = module_list

        """
        Elevator
        """
        putCommandOnDashboard("Elevator", ResetElevator(hardware.elevator))
        putCommandOnDashboard("Elevator", MaintainElevator(hardware.elevator))
        putCommandOnDashboard("Elevator", ManualMoveElevator.down(hardware.elevator))
        putCommandOnDashboard("Elevator", ManualMoveElevator.up(hardware.elevator))
        putCommandOnDashboard("Elevator", MoveElevator.toLevel1(hardware.elevator))
        putCommandOnDashboard("Elevator", MoveElevator.toLevel2(hardware.elevator))
        putCommandOnDashboard("Elevator", MoveElevator.toLevel3(hardware.elevator))
        putCommandOnDashboard("Elevator", MoveElevator.toLevel4(hardware.elevator))
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

        """
        Claw
        """
        putCommandOnDashboard("Claw", Drop.atLevel1(hardware.claw))
        putCommandOnDashboard("Claw", Drop.atLevel2(hardware.claw))
        putCommandOnDashboard("Claw", Drop.atLevel3(hardware.claw))
        putCommandOnDashboard("Claw", Drop.atLevel4(hardware.claw))

        """
        Arm
        """
        putCommandOnDashboard("Arm", RetractArm(hardware.arm))
        putCommandOnDashboard("Arm", ExtendArm(hardware.arm))

    def robotInit(self) -> None:
        for subsystem in self._hardware.subsystems:
            wpilib.SmartDashboard.putData(subsystem.getName(), subsystem)

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
