from abc import abstractmethod

from commands2 import ParallelCommandGroup

from commands.printer.moveprinter import MovePrinter
from subsystems.climber import Climber
from subsystems.printer import Printer
from ultime.autoproperty import autoproperty
from ultime.command import Command, ignore_requirements


class MoveClimber(Command):
    def __init__(self, climber: Climber, state: Climber.State):
        super().__init__()
        self.climber = climber
        self.addRequirements(self.climber)
        self.new_state = state

    def initialize(self):
        self.climber.state = Climber.State.Moving

    @abstractmethod
    def execute(self):
        raise NotImplementedError()

    @abstractmethod
    def isFinished(self) -> bool:
        raise NotImplementedError()

    def end(self, interrupted: bool):
        self.climber.stop()
        if interrupted:
            self.climber.state = Climber.State.Unknown
        else:
            self.climber.state = self.new_state


@ignore_requirements(["printer", "climber"])
class ReadyClimberAndBalance(ParallelCommandGroup):
    def __init__(self, printer: Printer, climber: Climber):
        super().__init__(ReadyClimber(climber), MovePrinter.toRight(printer))


class ReadyClimber(MoveClimber):
    position = autoproperty(30)

    def __init__(self, climber: Climber):
        super().__init__(climber=climber, state=Climber.State.Ready)

    def execute(self):
        self.climber.pull()

    def isFinished(self) -> bool:
        return self.climber.getPosition() >= self.position


class Climb(MoveClimber):
    def __init__(self, climber: Climber):
        super().__init__(climber=climber, state=Climber.State.Climbed)

    def execute(self):
        self.climber.pull()

    def isFinished(self) -> bool:
        return self.climber.isClimbed()


class ReleaseClimber(MoveClimber):
    def __init__(self, climber: Climber):
        super().__init__(climber=climber, state=Climber.State.Initial)

    def execute(self):
        self.climber.release()

    def isFinished(self) -> bool:
        return self.climber.getPosition() <= 0.0
