from subsystems.printer import Printer
from ultime.command import Command


class ResetPrinterLeft(Command):
    def __init__(self, printer: Printer):
        super().__init__()
        self.printer = printer
        self.addRequirements(printer)
        self.switch_left_was_pressed = False

    def initialize(self):
        self.switch_left_was_pressed = False
        self.printer.state = self.printer.State.Moving

    def execute(self):
        if self.printer.isLeft():  # If the down switch is pressed move up.
            self.printer.moveRight()
            self.switch_left_was_pressed = True
        else:
            self.printer.moveLeft()  # if switch is not pressed move down until pressed.

    def isFinished(self) -> bool:
        return not self.printer.isLeft() and self.switch_left_was_pressed

    def end(self, interrupted: bool):
        self.printer.state = self.printer.State.Reset
        self.printer.stop()
