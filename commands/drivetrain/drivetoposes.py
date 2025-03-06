from typing import List, Callable, Optional

from commands2 import Command
from wpimath.geometry import Pose2d, Rotation2d, Translation2d, Transform2d

from subsystems.drivetrain import Drivetrain
from ultime.auto import eitherRedBlue
from ultime.autoproperty import autoproperty, FloatProperty, asCallable
from ultime.trapezoidalmotion import TrapezoidalMotion


def pose(x: float, y: float, deg: float) -> Pose2d:
    return Pose2d(x, y, Rotation2d.fromDegrees(deg))


class DriveToPoses(Command):
    @classmethod
    def back(cls, drivetrain: Drivetrain, distance: FloatProperty):
        get_distance = asCallable(distance)

        def get_poses():
            current_pose = drivetrain.getPose()
            needed_pose = current_pose.transformBy(
                Transform2d(-get_distance(), 0.0, 0.0)
            )
            return [needed_pose]

        cmd = cls(drivetrain, get_poses)
        cmd.setName(cmd.getName() + ".back")
        return cmd

    xy_accel = autoproperty(5.0)
    xy_speed_end = autoproperty(12.0)
    xy_tol_pos = autoproperty(0.3)
    xy_tol_pos_last = autoproperty(0.1)
    xy_speed_max = autoproperty(12.0)

    rot_accel = autoproperty(0.2)
    rot_speed_end = autoproperty(10.0)
    rot_tol_pos = autoproperty(50)
    rot_tol_pos_last = autoproperty(10.0)
    rot_speed_max = autoproperty(10.0)

    def __init__(
        self,
        drivetrain: Drivetrain,
        goals: List[Pose2d] | Callable[[], List[Pose2d]],
        speed_constraint: Optional[float] = None,
        end_speed_constraint: Optional[float] = None,
        rotation_speed_constraint: Optional[float] = None,
        rotation_end_speed_constraint: Optional[float] = None,
    ):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.get_goals = goals if callable(goals) else lambda: goals
        self.goals: List[Pose2d] = None
        self.last_goal: Pose2d = None
        self.speed_constraint = speed_constraint
        self.end_speed_constraint = end_speed_constraint
        self.rotation_speed_constraint = rotation_speed_constraint
        self.rotation_end_speed_constraint = rotation_end_speed_constraint

    @staticmethod
    def fromRedBluePoints(
        drivetrain: Drivetrain, red_poses: List[Pose2d], blue_poses: List[Pose2d]
    ) -> Command:
        return eitherRedBlue(
            DriveToPoses(drivetrain, red_poses),
            DriveToPoses(drivetrain, blue_poses),
        )

    def updateMotions(self):
        self.last_goal = self.goals[-1]
        current_pose = self.drivetrain.getPose()
        self.trap_motion_xy = TrapezoidalMotion(
            start_speed=self.speed_constraint,
            end_speed=self.end_speed_constraint,
            max_speed=self.speed_constraint,
            accel=self.xy_accel,
            start_position=(
                self.last_goal.translation().distance(current_pose.translation())
            ),
            end_position=0.0,
        )
        self.start_rotation = current_pose.rotation()
        self.trap_motion_rot = TrapezoidalMotion(
            start_speed=self.rotation_speed_constraint,
            end_speed=self.rotation_end_speed_constraint,
            max_speed=self.rotation_speed_constraint,
            accel=self.rot_accel,
            start_position=(self.last_goal.rotation() - current_pose.rotation()).degrees(),
            end_position=0.0,
        )

    def initialize(self):
        if self.speed_constraint is None:
            self.speed_constraint = self.xy_speed_max

        if self.end_speed_constraint is None:
            self.end_speed_constraint = self.xy_speed_end

        if self.rotation_speed_constraint is None:
            self.rotation_speed_constraint = self.rot_speed_max

        if self.rotation_end_speed_constraint is None:
            self.rotation_end_speed_constraint = self.rot_speed_end

        self.goals = self.get_goals()
        self.currGoal = 0
        self.updateMotions()

    def execute(self):
        current_pose = self.drivetrain.getPose()
        translation_error = (
            self.goals[self.currGoal].translation() - current_pose.translation()
        )

        xy_mag = abs(self.trap_motion_xy.calculate(self.last_goal.translation().distance(current_pose.translation())))
        translation_error_norm = translation_error.norm()

        # Prevent division by zero
        if translation_error_norm < 0.01:
            vel_xy = Translation2d()
        else:
            vel_xy: Translation2d = translation_error * xy_mag / translation_error_norm

        vel_rot = self.trap_motion_rot.calculate(
            (self.last_goal.rotation() - current_pose.rotation()).degrees()
        )

        # print(vel_xy.X(), vel_xy.Y(), vel_rot)

        self.drivetrain.driveRaw(
            vel_xy.X(),
            vel_xy.Y(),
            vel_rot,
            True,
        )

        if (
            self.currGoal < len(self.goals) - 1
            and self.isWithinTolerances()
            or self.currGoal == len(self.goals) - 1
            and self.isWithinLastTolerances()
        ):
            self.currGoal += 1

            if self.currGoal < len(self.goals):
                self.updateMotions()

    def end(self, interrupted):
        self.currGoal = 0
        self.goals: List[Pose2d] = None
        self.drivetrain.stop()

    def isFinished(self):
        return self.currGoal == len(self.goals)

    def isWithinLastTolerances(self) -> bool:
        return (
            self.trap_motion_xy.getRemainingDistance() <= self.xy_tol_pos_last
            and self.trap_motion_rot.getRemainingDistance() <= self.rot_tol_pos_last
        )

    def isWithinTolerances(self) -> bool:
        return (
            self.trap_motion_xy.getRemainingDistance() <= self.xy_tol_pos
            and self.trap_motion_rot.getRemainingDistance() <= self.rot_tol_pos
        )
