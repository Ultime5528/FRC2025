from subsystems.elevator import Elevator
from ultime.autoproperty import autoproperty, FloatProperty, asCallable
from ultime.command import Command


class ManualMoveElevator(Command):
    @classmethod
    def up(cls, elevator: Elevator):
        cmd = cls(elevator, lambda: manual_move_properties.speed)
        cmd.setName(cmd.getName() + ".up")
        return cmd

    @classmethod
    def down(cls, elevator: Elevator):
        cmd = cls(elevator, lambda: -manual_move_properties.speed)
        cmd.setName(cmd.getName() + ".down")
        return cmd

    def __init__(self, elevator: Elevator, speed: FloatProperty):
        super().__init__()
        self.elevator = elevator
        self.addRequirements(self.elevator)
        self.get_speed = asCallable(speed)

    def execute(self):
        if self.get_speed() < 0.0 and self.elevator.isDown():
            self.elevator.setSpeed(0.0)
        else:
            self.elevator.setSpeed(self.get_speed())

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.elevator.stop()


class _ClassProperties:
    speed = autoproperty(0.15, subtable=ManualMoveElevator.__name__)


manual_move_properties = _ClassProperties()
