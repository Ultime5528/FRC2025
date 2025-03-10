import wpilib
from commands2 import Command

from subsystems.claw import Claw
from subsystems.printer import Printer
from ultime.autoproperty import autoproperty


class LoadCoral(Command):
    def __init__(self, claw: Claw, printer: Printer):
        super().__init__()
        self.claw = claw
        self.printer = printer
        self.addRequirements(claw, printer)
        self.timer = wpilib.Timer()
        self.speed_left_claw = load_coral_properties.claw_speed_left
        self.speed_right_claw = load_coral_properties.claw_speed_right

    def initialize(self):
        self.timer.stop()
        self.timer.reset()

    def execute(self):
        self.claw.setLeft(self.speed_left_claw)
        self.claw.setRight(self.speed_right_claw)

        if not self.claw.seesObject():
            self.timer.start()
        else:
            self.timer.stop()
            self.timer.reset()

        if not self.printer.isRight():
            self.printer.moveRight()
        else:
            self.printer.stop()

    def isFinished(self) -> bool:
        return (
            not self.claw.seesObject()
            and self.timer.get() >= load_coral_properties.delay
        )

    def end(self, interrupted: bool):
        self.claw.stop()
        self.timer.stop()
        if not interrupted:
            self.claw.has_coral = True


class _ClassProperties:
    # Claw Properties #
    delay = autoproperty(0.0, subtable=LoadCoral.__name__)
    claw_speed_left = autoproperty(-0.6, subtable=LoadCoral.__name__)
    claw_speed_right = autoproperty(0.6, subtable=LoadCoral.__name__)


load_coral_properties = _ClassProperties()
