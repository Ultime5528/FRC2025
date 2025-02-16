from commands2 import Command

from subsystems.climber import Climber
from ultime.command import with_timeout


@with_timeout(10.0)
class ResetClimber(Command):
    def __init__(self, climber: Climber):
        super().__init__()
        self.climber = climber
        self.addRequirements(climber)
        self.touched_switch = False

    def initialize(self):
        self.touched_switch = False
        self.climber.state = self.climber.State.Moving

    def execute(self):
        if self.climber.isClimbed():  # If the switch is pressed move up.
            self.climber.release()
            self.touched_switch = True
        elif self.touched_switch:
            self.climber.release()
        else:
            self.climber.pull()

    def isFinished(self) -> bool:
        return self.touched_switch and self.climber.getPosition() <= 0.0

    def end(self, interrupted: bool):
        if interrupted:
            self.climber.state = self.climber.State.Unknown
        else:
            self.climber.state = self.climber.State.Initial
        self.climber.stop()
