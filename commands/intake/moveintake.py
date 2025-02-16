import wpilib
from commands2 import Command

from subsystems.intake import Intake
from ultime.autoproperty import autoproperty, FloatProperty, asCallable
from ultime.command import with_timeout
from ultime.trapezoidalmotion import TrapezoidalMotion


@with_timeout(5.0)
class MoveIntake(Command):
    @classmethod
    def toExtended(cls, intake: Intake):
        cmd = cls(
            intake,
            lambda: move_intake_properties.position_extended,
            Intake.State.Extended,
        )
        cmd.setName(cmd.getName() + ".toExtended")
        return cmd

    @classmethod
    def toRetracted(cls, intake: Intake):
        cmd = cls(
            intake,
            lambda: move_intake_properties.position_retracted,
            Intake.State.Retracted,
        )
        cmd.setName(cmd.getName() + ".toRetracted")
        return cmd

    def __init__(
        self, intake: Intake, end_position: FloatProperty, new_state: Intake.State
    ):
        super().__init__()
        self.end_position_getter = asCallable(end_position)
        self.intake = intake
        self.addRequirements(intake)
        self.new_state = new_state

    def initialize(self):
        self.motion = TrapezoidalMotion(
            start_position=self.intake.getPivotPosition(),
            end_position=self.end_position_getter(),
            start_speed=max(
                move_intake_properties.speed_min,
                abs(self.intake.getPivotMotorInput()),
            ),
            end_speed=move_intake_properties.speed_min,
            max_speed=move_intake_properties.speed_max,
            accel=move_intake_properties.accel,
        )
        self.intake.state = Intake.State.Moving

    def execute(self):
        pos = self.intake.getPivotPosition()
        self.motion.setPosition(pos)
        self.intake.setPivotSpeed(self.motion.getSpeed())

    def isFinished(self) -> bool:
        return self.motion.isFinished() or not self.intake.hasReset()

    def end(self, interrupted: bool):
        if not self.intake.hasReset():
            wpilib.reportError("Intake has not reset: cannot MoveIntake")

        if interrupted:
            self.intake.state = Intake.State.Unknown
        else:
            self.intake.state = self.new_state

        self.intake.stopPivot()


class _ClassProperties:
    position_extended = autoproperty(90.0, subtable=MoveIntake.__name__)
    position_retracted = autoproperty(0.0, subtable=MoveIntake.__name__)

    speed_min = autoproperty(0.5, subtable=MoveIntake.__name__)
    speed_max = autoproperty(0.8, subtable=MoveIntake.__name__)
    accel = autoproperty(0.01, subtable=MoveIntake.__name__)


move_intake_properties = _ClassProperties()
