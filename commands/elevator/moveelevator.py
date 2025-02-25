from enum import Enum, auto

import wpilib
from commands2 import SelectCommand
from wpilib import DriverStation
from wpiutil import SendableBuilder

from commands.alignwithreefside import getSextantFromPosition, reef_centers
from subsystems.arm import Arm
from subsystems.drivetrain import Drivetrain
from subsystems.elevator import Elevator
from ultime.autoproperty import autoproperty, FloatProperty, asCallable
from ultime.command import Command, with_timeout
from ultime.trapezoidalmotion import TrapezoidalMotion


@with_timeout(10.0)
class MoveElevator(Command):
    class AlgaePosition(Enum):
        Unknown = auto()
        Up = auto()
        Down = auto()

    @staticmethod
    def _getAlgaeLevelPosition(drivetrain: Drivetrain):
        alliance = DriverStation.getAlliance()
        sextant = getSextantFromPosition(drivetrain.getPose(), reef_centers[alliance])

        if alliance == alliance.kBlue:
            if sextant == 0 or sextant == 2 or sextant == 4:
                MoveElevator.AlgaePosition = MoveElevator.AlgaePosition.Down
            else:
                MoveElevator.AlgaePosition = MoveElevator.AlgaePosition.Up
        elif alliance.kRed:
            if sextant == 0 or sextant == 2 or sextant == 4:
                MoveElevator.AlgaePosition = MoveElevator.AlgaePosition.Up
            else:
                MoveElevator.AlgaePosition = MoveElevator.AlgaePosition.Down
        else:
            MoveElevator.AlgaePosition = MoveElevator.AlgaePosition.Unknown

        return MoveElevator.AlgaePosition

    @classmethod
    def toLevel1(cls, elevator: Elevator):
        cmd = cls(
            elevator,
            lambda: move_elevator_properties.position_level1,
            Elevator.State.Level1,
        )
        cmd.setName(cmd.getName() + ".toLevel1")
        return cmd

    @classmethod
    def toLevel2(cls, elevator: Elevator):
        cmd = cls(
            elevator,
            lambda: move_elevator_properties.position_level2,
            Elevator.State.Level2,
        )
        cmd.setName(cmd.getName() + ".toLevel2")
        return cmd

    @classmethod
    def toLevel2Algae(cls, elevator: Elevator):
        cmd = cls(
            elevator,
            lambda: move_elevator_properties.position_level2_algae,
            Elevator.State.Level2Algae,
        )
        cmd.setName(cmd.getName() + ".toLevel2Algae")
        return cmd

    @classmethod
    def toLevel3(cls, elevator: Elevator):
        cmd = cls(
            elevator,
            lambda: move_elevator_properties.position_level3,
            elevator.State.Level3,
        )
        cmd.setName(cmd.getName() + ".toLevel3")
        return cmd

    @classmethod
    def toLevel3Algae(cls, elevator: Elevator):
        cmd = cls(
            elevator,
            lambda: move_elevator_properties.position_level3_algae,
            Elevator.State.Level3Algae,
        )
        cmd.setName(cmd.getName() + ".toLevel3Algae")
        return cmd

    @classmethod
    def toLevel4(cls, elevator: Elevator):
        cmd = cls(
            elevator,
            lambda: move_elevator_properties.position_level4,
            Elevator.State.Level4,
        )
        cmd.setName(cmd.getName() + ".toLevel4")
        return cmd

    @classmethod
    def toLoading(cls, elevator: Elevator):
        cmd = cls(
            elevator,
            lambda: move_elevator_properties.position_loading,
            Elevator.State.Loading,
        )
        cmd.setName(cmd.getName() + ".toLoading")
        return cmd

    @classmethod
    def toAlgae(cls, elevator: Elevator, drivetrain: Drivetrain):
        cmd = SelectCommand(
            {
                MoveElevator.AlgaePosition.Up: cls.toLevel3Algae(elevator),
                MoveElevator.AlgaePosition.Down: cls.toLevel2Algae(elevator),
            },
            lambda: cls._getAlgaeLevelPosition(drivetrain),
        )

        cmd.setName(cmd.getName() + ".toAlgae")

        return cmd

    def __init__(
        self, elevator: Elevator, end_position: FloatProperty, new_state: Elevator.State
    ):
        super().__init__()
        self.end_position_getter = asCallable(end_position)
        self.elevator = elevator
        self.new_state = new_state
        self.addRequirements(elevator)
        self.AlgaePosition = self.AlgaePosition.Unknown

    def initialize(self):
        self.motion = TrapezoidalMotion(
            start_position=self.elevator.getHeight(),
            end_position=self.end_position_getter(),
            start_speed=max(
                move_elevator_properties.speed_min, abs(self.elevator.getMotorInput())
            ),
            end_speed=move_elevator_properties.speed_min,
            max_speed=move_elevator_properties.speed_max,
            accel=move_elevator_properties.accel,
        )
        self.elevator.state = Elevator.State.Moving

    def execute(self):
        height = self.elevator.getHeight()
        self.motion.setPosition(height)
        self.elevator.setSpeed(self.motion.getSpeed())

    def isFinished(self) -> bool:
        return self.motion.isFinished() or not self.elevator.hasReset()

    def end(self, interrupted: bool) -> None:
        if not self.elevator.hasReset():
            wpilib.reportError("Elevator has not reset: cannot MoveElevator")

        self.elevator.stop()

        if interrupted:
            self.elevator.state = Elevator.State.Unknown
        else:
            self.elevator.state = self.new_state

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def setOffset(value: float):
            self._offset = value

        def noop(x):
            pass

        def setHasReset(value: bool):
            self._has_reset = value

        # builder.addStringProperty("algae_state", lambda: self.AlgaePosition.name, noop)


class _ClassProperties:
    position_level1 = autoproperty(0.12, subtable=MoveElevator.__name__)
    position_level2 = autoproperty(0.35, subtable=MoveElevator.__name__)
    position_level2_algae = autoproperty(0.8, subtable=MoveElevator.__name__)
    position_level3 = autoproperty(0.75, subtable=MoveElevator.__name__)
    position_level3_algae = autoproperty(1.215, subtable=MoveElevator.__name__)
    position_level4 = autoproperty(1.35, subtable=MoveElevator.__name__)
    position_loading = autoproperty(0.0, subtable=MoveElevator.__name__)

    speed_min = autoproperty(0.12, subtable=MoveElevator.__name__)
    speed_max = autoproperty(1.0, subtable=MoveElevator.__name__)
    accel = autoproperty(7.0, subtable=MoveElevator.__name__)


move_elevator_properties = _ClassProperties()
