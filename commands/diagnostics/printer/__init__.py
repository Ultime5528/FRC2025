from commands2 import SequentialCommandGroup
from wpilib import PowerDistribution

from commands.diagnostics.printer.motor import DiagnoseMotor
from commands.diagnostics.printer.switch import DiagnoseSwitch
from subsystems.printer import Printer
from ultime.command import ignore_requirements


@ignore_requirements(["printer"])
class DiagnosePrinter(SequentialCommandGroup):
    def __init__(self, printer: Printer, pdp: PowerDistribution):
        super().__init__(DiagnoseSwitch(printer), DiagnoseMotor(printer, pdp))
