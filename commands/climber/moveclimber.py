from abc import abstractmethod

from subsystems.climber import Climber
from ultime.autoproperty import autoproperty
from ultime.command import Command


class MoveClimber:
    @staticmethod
    def toReadyPosition(climber: Climber):
        cmd = ReadyClimber(climber)
        cmd.setName(MoveClimber.__name__ + ".toReadyPosition")
        return cmd

    @staticmethod
    def toClimbedPosition(climber: Climber):
        cmd = ClimbClimber(climber)
        cmd.setName(MoveClimber.__name__ + ".toClimbedPosition")
        return cmd

    @staticmethod
    def toInitialPosition(climber: Climber):
        cmd = ReleaseClimber(climber)
        cmd.setName(MoveClimber.__name__ + ".toInitialPosition")
        return cmd


class MovingClimber(Command):
    def __init__(self, climber: Climber, state: Climber.State):
        super().__init__()
        self.climber = climber
        self.addRequirements(self.climber)
        self.new_state = state

    def initialize(self):
        self.climber.state = Climber.State.Moving

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    @abstractmethod
    def isFinished(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def end(self, interrupted: bool):
        self.climber.stop()
        if interrupted:
            self.climber.state = Climber.State.Invalid
        else:
            self.climber.state = self.new_state


class ReadyClimber(MovingClimber):
    position_ready = autoproperty(5.0)

    def __init__(self, climber: Climber):
        super().__init__(climber=climber, state=Climber.State.Ready)

    def execute(self):
        self.climber.pull()

    def isFinished(self) -> bool:
        return self.climber.getPosition() >= self.position_ready


class ClimbClimber(MovingClimber):
    def __init__(self, climber: Climber):
        super().__init__(climber=climber, state=Climber.State.Climbed)

    def execute(self):
        self.climber.pull()

    def isFinished(self) -> bool:
        return self.climber._switch.isPressed()


class ReleaseClimber(MovingClimber):
    def __init__(self, climber: Climber):
        super().__init__(climber=climber, state=Climber.State.Initial)

    def execute(self):
        self.climber.release()

    def isFinished(self) -> bool:
        return self.climber.getPosition() <= 0.0
