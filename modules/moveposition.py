from commands.printer.moveprinter import MovePrinter
from subsystems.printer import Printer
from subsystems.claw import Claw
from ultime.module import Module


class MovePositionPrinterModule(Module):
    def __init__(self, claw: Claw, printer: Printer):
        super().__init__()
        self.claw = claw
        self.printer = printer
        self.cmd = MovePrinter.toMiddleRight(self.printer)

    def robotPeriodic(self) -> None:
        if self.claw.has_coral and self.printer.state != self.printer.State.MiddleRight and self.printer.State == self.printer.State.Loading:
            self.cmd.schedule()
