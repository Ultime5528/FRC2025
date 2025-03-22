from typing import Literal

import wpilib
from commands2 import SelectCommand
from wpilib import DriverStation
from wpimath.geometry import Pose2d

from commands.alignwithreefside import getCurrentSextant
from subsystems.drivetrain import Drivetrain
from subsystems.elevator import Elevator
from ultime.autoproperty import autoproperty, FloatProperty, asCallable
from ultime.command import Command, with_timeout
from ultime.trapezoidalmotion import TrapezoidalMotion


@with_timeout(10.0)
class MoveElevator(Command):
    @staticmethod
    def _getAlgaeLevelPosition(pose: Pose2d) -> Literal["None", "Level2", "Level3"]:
        alliance = DriverStation.getAlliance()
        sextant = getCurrentSextant(pose)
        if alliance is not None:
            if alliance == alliance.kBlue:
                if sextant in {0, 2, 4}:
                    return "Level2"
                else:
                    return "Level3"
            elif alliance.kRed:
                if sextant in {0, 2, 4}:
                    return "Level3"
                else:
                    return "Level2"
        else:
            return "None"

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
                "Level3": cls.toLevel3Algae(elevator),
                "Level2": cls.toLevel2Algae(elevator),
            },
            lambda: MoveElevator._getAlgaeLevelPosition(drivetrain.getPose()),
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

    def initialize(self):
        start = self.elevator.getHeight()
        end = self.end_position_getter()
        self.motion = TrapezoidalMotion(
            start_position=start,
            end_position=end,
            start_speed=max(
                move_elevator_properties.speed_start, abs(self.elevator.getMotorInput())
            ),
            end_speed=move_elevator_properties.speed_end,
            max_speed=(
                move_elevator_properties.speed_max_up
                if end > start
                else move_elevator_properties.speed_max_down
            ),
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


class _ClassProperties:
    position_level1 = autoproperty(0.14, subtable=MoveElevator.__name__)
    position_level2 = autoproperty(0.345, subtable=MoveElevator.__name__)
    position_level2_algae = autoproperty(0.8, subtable=MoveElevator.__name__)
    position_level3 = autoproperty(0.72, subtable=MoveElevator.__name__)
    position_level3_algae = autoproperty(1.215, subtable=MoveElevator.__name__)
    position_level4 = autoproperty(1.345, subtable=MoveElevator.__name__)
    position_loading = autoproperty(0.0, subtable=MoveElevator.__name__)

    speed_end = autoproperty(0.15, subtable=MoveElevator.__name__)
    speed_start = autoproperty(0.2, subtable=MoveElevator.__name__)
    speed_max_up = autoproperty(1.0, subtable=MoveElevator.__name__)
    speed_max_down = autoproperty(0.7, subtable=MoveElevator.__name__)
    accel = autoproperty(2.0, subtable=MoveElevator.__name__)


move_elevator_properties = _ClassProperties()
