from commands2 import SequentialCommandGroup
from commands2.cmd import runOnce

from commands.printer.moveprinter import MovePrinter
from commands.printer.resetprinter import ResetPrinterRight
from subsystems.printer import Printer
from ultime.command import ignore_requirements
from ultime.proxy import proxy


@ignore_requirements(["printer"])
class DiagnoseSwitch(SequentialCommandGroup):
    def __init__(self, printer: Printer):
        super().__init__(
            MovePrinter.toLeft(printer),
            runOnce(proxy(self.check_switches_left)),
            MovePrinter.toRight(printer),
            runOnce(proxy(self.check_switches_right)),
            ResetPrinterRight(printer),
        )
        self.printer = printer

    def check_switches_left(self):
        if not self.printer.isLeft():
            self.printer.alert_switch_left.set(True)
        if self.printer.isRight():
            self.printer.alert_switch_right.set(True)

    def check_switches_right(self):
        if not self.printer.isRight():
            self.printer.alert_switch_right.set(True)
        if self.printer.isLeft():
            self.printer.alert_switch_left.set(True)
