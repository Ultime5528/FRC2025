from subsystems.printer import Printer
from ultime.autoproperty import autoproperty, FloatProperty, asCallable
from ultime.command import Command


class ManualMovePrinter(Command):
    @classmethod
    def left(cls, printer: Printer):
        cmd = cls(printer, lambda: manual_move_properties.speed)
        cmd.setName(cmd.getName() + ".left")
        return cmd

    @classmethod
    def right(cls, printer: Printer):
        cmd = cls(printer, lambda: -manual_move_properties.speed)
        cmd.setName(cmd.getName() + ".right")
        return cmd

    def __init__(self, printer: Printer, speed: FloatProperty):
        super().__init__()
        self.printer = printer
        self.addRequirements(self.printer)
        self.get_speed = asCallable(speed)

    def execute(self):
        self.printer.setSpeed(self.get_speed())

    def isFinished(self) -> bool:
        if self.get_speed() < 0:
            return self.printer._switch_right.isPressed()
        if self.get_speed() > 0:
            return self.printer._switch_left.isPressed()

    def end(self, interrupted: bool):
        self.printer.stop()


class _ClassProperties:
    speed = autoproperty(0.2, subtable=ManualMovePrinter.__name__)


manual_move_properties = _ClassProperties()
