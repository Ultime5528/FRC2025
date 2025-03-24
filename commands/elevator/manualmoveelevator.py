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

    def initialize(self):
        self.elevator.state = Elevator.State.Moving

    def execute(self):
        self.elevator.setSpeed(self.get_speed())

    def isFinished(self) -> bool:
        return self.elevator.getMotorInput() < 0.0 and self.elevator.isDown()

    def end(self, interrupted: bool):
        self.elevator.stop()
        self.elevator.state = Elevator.State.Unknown


class _ClassProperties:
    speed = autoproperty(0.15, subtable=ManualMoveElevator.__name__)


manual_move_properties = _ClassProperties()
