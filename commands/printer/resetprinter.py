from subsystems.printer import Printer
from ultime.command import Command


class ResetPrinterRight(Command):
    def __init__(self, printer: Printer):
        super().__init__()
        self.printer = printer
        self.addRequirements(printer)
        self.switch_right_was_pressed = False

    def initialize(self):
        self.switch_right_was_pressed = False
        self.printer.state = self.printer.State.Moving

    def execute(self):
        if self.printer.isRight():  # If the down switch is pressed move up.
            self.printer.moveLeft()
            self.switch_right_was_pressed = True
        else:
            self.printer.moveRight()  # if switch is not pressed move down until pressed.

    def isFinished(self) -> bool:
        return not self.printer.isRight() and self.switch_right_was_pressed

    def end(self, interrupted: bool):
        self.printer.state = self.printer.State.Reset
        self.printer.stop()
