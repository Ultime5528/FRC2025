from functools import wraps
from typing import Type

import wpilib
from commands2 import Command
from wpilib import Timer, DataLogManager

from ultime.autoproperty import FloatProperty, asCallable


def ignore_requirements(reqs: list[str]):
    def _ignore(actual_cls: Type[Command]) -> Type[Command]:
        setattr(actual_cls, "__ignore_reqs", reqs)
        return actual_cls

    return _ignore


def with_timeout(seconds: float):
    def add_timeout(CommandClass):
        @wraps(CommandClass, updated=())
        class CommandWithTimeout(CommandClass):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.setName(CommandClass.__name__)
                self.seconds = seconds
                self.timer = Timer()

            def initialize(self):
                super().initialize()
                self.timer.restart()

            def isFinished(self) -> bool:
                return super().isFinished() or self.timer.get() >= self.seconds

            def end(self, interrupted: bool):
                super().end(interrupted)
                self.timer.stop()
                if self.timer.get() >= self.seconds:
                    msg = f"Command {self.getName()} got interrupted after {self.seconds} seconds"
                    wpilib.reportError(msg)
                    DataLogManager.log(msg)

        setattr(CommandWithTimeout, "__wrapped_class", CommandClass)

        return CommandWithTimeout

    return add_timeout


class WaitCommand(Command):
    def __init__(self, seconds: FloatProperty):
        super().__init__()
        self.get_seconds = asCallable(seconds)
        self.timer = wpilib.Timer()

    def initialize(self):
        self.timer.restart()

    def isFinished(self) -> bool:
        return self.timer.hasElapsed(self.get_seconds())
