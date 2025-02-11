import wpilib
from commands2.cmd import sequence

from commands.printer.manualmoveprinter import ManualMovePrinter
from subsystems.printer import Printer
from ultime.autoproperty import autoproperty, FloatProperty, asCallable
from ultime.command import Command
from ultime.trapezoidalmotion import TrapezoidalMotion


class MovePrinter:
    @staticmethod
    def toLeft(printer: Printer):
        cmd = _MovePrinterSetpoint(
            printer,
            lambda: move_printer_properties.position_left,
            Printer.State.Left,
        )
        cmd.setName(MovePrinter.__name__ + ".toLeft")
        return cmd

    @staticmethod
    def toMiddle(printer: Printer):
        cmd = _MovePrinterSetpoint(
            printer,
            lambda: move_printer_properties.position_middle,
            Printer.State.Middle,
        )
        cmd.setName(MovePrinter.__name__ + ".toMiddle")
        return cmd

    @staticmethod
    def toRight(printer: Printer):
        cmd = _MovePrinterSetpoint(
            printer,
            lambda: move_printer_properties.position_right,
            printer.State.Right,
        )
        cmd.setName(MovePrinter.__name__ + ".toRight")
        return cmd

    @staticmethod
    def toLoading(printer: Printer):
        cmd = _MovePrinterSetpoint(
            printer,
            lambda: move_printer_properties.position_loading,
            Printer.State.Loading,
        )
        cmd.setName(MovePrinter.__name__ + ".toLoading")
        return cmd

    @staticmethod
    def toMiddleLeft(printer: Printer):
        cmd = _MovePrinterSetpoint(
            printer,
            lambda: move_printer_properties.position_middle_left,
            Printer.State.MiddleLeft,
        )
        cmd.setName(MovePrinter.__name__ + ".toLeftMiddle")
        return cmd

    @staticmethod
    def toMiddleRight(printer: Printer):
        cmd = _MovePrinterSetpoint(
            printer,
            lambda: move_printer_properties.position_middle_right,
            Printer.State.MiddleRight,
        )
        cmd.setName(MovePrinter.__name__ + ".toRightMiddle")
        return cmd

    @staticmethod
    def leftUntilReef(printer: Printer):
        cmd = sequence(
            MovePrinter.toMiddleLeft(printer), _MovePrinterWithSensor.left(printer)
        )
        cmd.setName(MovePrinter.__name__ + ".leftUntilReef")
        return cmd

    @staticmethod
    def rightUntilReef(printer: Printer):
        cmd = sequence(
            MovePrinter.toMiddleRight(printer), _MovePrinterWithSensor.right(printer)
        )
        cmd.setName(MovePrinter.__name__ + ".rightUntilReef")
        return cmd


class _MovePrinterSetpoint(Command):
    def __init__(
        self, printer: Printer, end_position: FloatProperty, new_state: Printer.State
    ):
        super().__init__()
        self.end_position_getter = asCallable(end_position)
        self.printer = printer
        self.addRequirements(printer)
        self.new_state = new_state

    def initialize(self):
        self.motion = TrapezoidalMotion(
            start_position=self.printer.getPose(),
            end_position=self.end_position_getter(),
            start_speed=max(
                move_printer_properties.speed_min, abs(self.printer.getMotorInput())
            ),
            end_speed=move_printer_properties.speed_min,
            max_speed=move_printer_properties.speed_max,
            accel=move_printer_properties.accel,
        )
        self.printer.state = Printer.State.Moving

    def execute(self):
        height = self.printer.getPose()
        self.motion.setPosition(height)
        self.printer.setSpeed(self.motion.getSpeed())

    def isFinished(self) -> bool:
        return self.motion.isFinished() or not self.printer.hasReset()

    def end(self, interrupted: bool) -> None:
        if not self.printer.hasReset():
            wpilib.reportError("Elevator has not reset: cannot MoveElevator")

        self.printer.stop()

        if interrupted:
            self.printer.state = Printer.State.Unknown
        else:
            self.printer.state = self.new_state


class _MovePrinterWithSensor(Command):
    @staticmethod
    def left(printer: Printer):
        cmd = ManualMovePrinter.left(printer).until(lambda: printer.seesReef())
        return cmd

    @staticmethod
    def right(printer: Printer):
        cmd = ManualMovePrinter.right(printer).until(lambda: printer.seesReef())
        return cmd


class _ClassProperties:
    position_left = autoproperty(0.4, subtable=MovePrinter.__name__)
    position_middle = autoproperty(0.2, subtable=MovePrinter.__name__)
    position_right = autoproperty(0.0, subtable=MovePrinter.__name__)
    position_loading = autoproperty(0.05, subtable=MovePrinter.__name__)

    position_middle_left = autoproperty(0.3, subtable=MovePrinter.__name__)
    position_middle_right = autoproperty(0.2, subtable=MovePrinter.__name__)

    speed_min = autoproperty(0.2, subtable=MovePrinter.__name__)
    speed_max = autoproperty(0.4, subtable=MovePrinter.__name__)
    accel = autoproperty(0.01, subtable=MovePrinter.__name__)


move_printer_properties = _ClassProperties()
