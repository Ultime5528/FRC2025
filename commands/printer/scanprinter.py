from ultime.autoproperty import FloatProperty, autoproperty, asCallable
from ultime.command import Command
from subsystems.printer import Printer


class ScanPrinter(Command):
    @staticmethod
    def right(cls, printer: Printer):
        cmd = cls(printer, lambda: -scan_printer_properties.speed)
        cmd.setName(ScanPrinter.__name__ + ".right")
        return cmd

    @staticmethod
    def left(cls, printer: Printer):
        cmd = cls(printer, lambda: scan_printer_properties.speed)
        cmd.setName(ScanPrinter.__name__ + ".left")
        return cmd

    def __init__(self, printer: Printer, speed: FloatProperty):
        super().__init__()
        self.printer = printer
        self._list_point = []
        self.get_speed = asCallable(speed)
        self.scanned = False

    def initialize(self):
        self._list_point = []
        self.scanned = False
        self.needed_position = 0.0
        self.printer.state = self.printer.State.Moving

    def execute(self):
        if not self.scanned:
            self.printer.setSpeed(self.get_speed())

        if self.printer.seesReef() and not self.scanned:
            self._list_point.append(self.printer.getPosition())
            self.needed_position = (
                self._list_point[0] + self._list_point[len(self._list_point)]
            ) / 2
        elif not self.printer.seesReef() and len(self._list_point) > 0:
            self.scanned = True
            if self.get_speed() > 0:
                self.printer.moveRight()
            elif self.get_speed() < 0:
                self.printer.moveLeft()

    def isFinished(self) -> bool:
        if self.get_speed() > 0:
            return self.printer.getPosition() > self.needed_position
        else:
            return self.printer.getPosition() < self.needed_position

    def end(self, interrupted: bool):
        self.printer.stop()
        self.printer.state = self.printer.State.Unknown


class _ClassProperties:
    speed = autoproperty(0.15, subtable=ScanPrinter.__name__)


scan_printer_properties = _ClassProperties()
