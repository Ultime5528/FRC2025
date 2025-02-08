from typing import Type

import wpilib
from commands2 import Command, ParallelRaceGroup, WaitCommand
from wpilib import Timer


def ignore_requirements(reqs: list[str]):
    def _ignore(actual_cls: Type[Command]) -> Type[Command]:
        setattr(actual_cls, "__ignore_reqs", reqs)
        return actual_cls

    return _ignore


class WaitCommandError(Command):
    def __init__(self, seconds: float, cmd: Command):
        super().__init__()
        self.seconds = seconds
        self.cmd = cmd
        self.timer = Timer()

    def initialize(self):
        self.timer.restart()

    def isFinished(self) -> bool:
        return self.timer.get() >= self.seconds

    def end(self, interrupted: bool):
        if not interrupted:
            wpilib.reportError(f"Command {self.cmd.getName()} got interrupted after {self.seconds} seconds")


def with_timeout(seconds: float, print_error=True):
    def add_timeout(CommandClass):
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
                    wpilib.reportError(f"Command {self.getName()} got interrupted after {self.seconds} seconds")

        return CommandWithTimeout

    return add_timeout