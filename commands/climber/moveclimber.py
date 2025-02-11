from abc import abstractmethod

from subsystems.climber import Climber
from ultime.autoproperty import autoproperty
from ultime.command import Command, with_timeout


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

@with_timeout(5.0)
class ReadyClimber(MoveClimber):
    position = autoproperty(5.0)

    def __init__(self, climber: Climber):
        super().__init__(climber=climber, state=Climber.State.Ready)

    def execute(self):
        self.climber.pull()

    def isFinished(self) -> bool:
        return self.climber.getPosition() >= self.position

@with_timeout(15.0)
class Climb(MoveClimber):
    def __init__(self, climber: Climber):
        super().__init__(climber=climber, state=Climber.State.Climbed)

    def execute(self):
        self.climber.pull()

    def isFinished(self) -> bool:
        return self.climber.isClimbed()

@with_timeout(15.0)
class ReleaseClimber(MoveClimber):
    def __init__(self, climber: Climber):
        super().__init__(climber=climber, state=Climber.State.Initial)

    def execute(self):
        self.climber.release()

    def isFinished(self) -> bool:
        return self.climber.getPosition() <= 0.0
