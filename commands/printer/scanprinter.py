from commands2 import SequentialCommandGroup
from commands2.cmd import either, none
from wpiutil import SendableBuilder

from commands.printer.moveprinter import MovePrinter
from subsystems.printer import Printer
from ultime.autoproperty import FloatProperty, autoproperty, asCallable
from ultime.command import Command
from ultime.timethis import tt


class ScanPrinter(Command):
    @staticmethod
    def right(printer: Printer):
        cmd = SequentialCommandGroup(
            MovePrinter.toRight(printer),
            _ScanPrinter.left(printer),
            either(none(), MovePrinter.toRight(printer), lambda: printer.scanned),
        )
        cmd.setName(ScanPrinter.__name__ + ".right")
        return cmd

    @staticmethod
    def left(printer: Printer):
        cmd = SequentialCommandGroup(
            MovePrinter.toLeft(printer),
            _ScanPrinter.right(printer),
            either(none(), MovePrinter.toLeft(printer), lambda: printer.scanned),
        )
        cmd.setName(ScanPrinter.__name__ + ".left")
        return cmd


class _ScanPrinter(Command):
    @classmethod
    def right(cls, printer: Printer):
        cmd = cls(printer, lambda: -scan_printer_properties.speed)
        cmd.setName(_ScanPrinter.__name__ + ".right")
        return cmd

    @classmethod
    def left(cls, printer: Printer):
        cmd = cls(printer, lambda: scan_printer_properties.speed)
        cmd.setName(_ScanPrinter.__name__ + ".left")
        return cmd

    def __init__(self, printer: Printer, speed: FloatProperty):
        super().__init__()
        self.printer = printer
        self.addRequirements(printer)
        self._list_point = []
        self.get_speed = asCallable(speed)
        self.scanned = False
        self.object_width: float = 0.0

    def initialize(self):
        self._list_point = []
        self.printer.scanned = False
        self.needed_position = 0.0
        self.printer.state = self.printer.State.Moving
        self.object_width = 0.0

    def execute(self):
        if not self.printer.scanned:
            self.printer.setSpeed(self.get_speed())

            if self.printer.seesReef():
                self._list_point.append(self.printer.getPosition())

            if self._list_point and (not self.printer.seesReef()):
                self.object_width = abs(self._list_point[-1] - self._list_point[0])
                if self.object_width <= scan_printer_properties.coral_width:
                    self.scanned = True
                    self.needed_position = (
                        self._list_point[0] + self._list_point[-1]
                    ) / 2
                else:
                    self._list_point = []

        if self.printer.scanned:
            self.printer.setSpeed(-self.get_speed())

    def isFinished(self) -> bool:
        if (self.get_speed() > 0 and self.printer.isLeft()) or (
            self.get_speed() < 0 and self.printer.isRight()
        ):
            return True

        if not self.printer.scanned:
            return False

        if self.get_speed() > 0:
            return (
                self.printer.getPosition() <= self.needed_position
                or self.printer.isRight()
            )
        else:
            return (
                self.printer.getPosition() >= self.needed_position
                or self.printer.isLeft()
            )

    def end(self, interrupted: bool):
        self.printer.stop()
        self.printer.state = self.printer.State.Unknown

    def initSendable(self, builder: SendableBuilder) -> None:
        def noop(x):
            pass

        builder.addFloatProperty("ObjectWidth", tt(lambda: self.object_width), noop)


class _ClassProperties:
    speed = autoproperty(0.5, subtable=ScanPrinter.__name__)
    coral_width = autoproperty(3.0, subtable=ScanPrinter.__name__)


scan_printer_properties = _ClassProperties()
