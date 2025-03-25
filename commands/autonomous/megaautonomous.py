from commands2 import SequentialCommandGroup
from commands2.cmd import parallel, sequence, either, waitSeconds
from wpimath.geometry import Pose2d, Rotation2d, Transform2d

from commands.claw.loadcoral import LoadCoral
from commands.claw.retractcoral import RetractCoral
from commands.claw.waituntilcoral import WaitUntilCoral
from commands.drivetrain.drivetoposes import DriveToPoses, DriveToPosesAutoFlip
from commands.dropautonomous import DropAutonomous
from commands.elevator.moveelevator import MoveElevator
from commands.prepareloading import PrepareLoading
from commands.resetautonomous import ResetAutonomous
from modules.hardware import HardwareModule
from ultime.vision import april_tag_field_layout


class MegaAutonomous(SequentialCommandGroup):
    @classmethod
    def left(cls, hardware: HardwareModule):
        cmd = MegaAutonomous(hardware, True)
        cmd.setName(MegaAutonomous.__name__ + ".left")
        return cmd

    @classmethod
    def right(cls, hardware: HardwareModule):
        cmd = MegaAutonomous(hardware, False)
        cmd.setName(MegaAutonomous.__name__ + ".right")
        return cmd

    def __init__(self, hardware: HardwareModule, is_left_side: bool):
        super().__init__()

        offset_drop_right = 0.11
        offset_drop_left = 0.45
        offset_backward_1 = 1.0
        offset_backward_2 = 0.48

        el = hardware.elevator
        pr = hardware.printer
        arm = hardware.arm
        claw = hardware.claw
        driv = hardware.drivetrain

        def GetTagWithOffset(tag: int, offset: float):
            tag_pose = april_tag_field_layout.getTagPose(tag).toPose2d()
            flipped_tag = Pose2d(
                tag_pose.translation(),
                tag_pose.rotation() + Rotation2d.fromDegrees(180),
            )
            return [
                flipped_tag.transformBy(
                    Transform2d(-offset_backward_1, offset, Rotation2d())
                ),
                flipped_tag.transformBy(
                Transform2d(-offset_backward_2, offset, Rotation2d())
            )]

        pose_tag_20 = GetTagWithOffset(20, offset_drop_right)
        pose_tag_22 = GetTagWithOffset(22, offset_drop_right)
        pose_tag_17_drop_right = GetTagWithOffset(17, offset_drop_right)
        pose_tag_17_drop_left = GetTagWithOffset(17, offset_drop_left)
        pose_tag_19_drop_right = GetTagWithOffset(19, offset_drop_right)
        pose_tag_19_drop_left = GetTagWithOffset(19, offset_drop_left)

        right_coral = Pose2d(1.1, 0.87, Rotation2d.fromDegrees(-35.0))
        pose_right_coral_station = [
            right_coral.transformBy(Transform2d(0.0, 2.0, 0.0)),
            Pose2d(1.1, 0.8, Rotation2d.fromDegrees(-35.0))
        ]
        pose_left_coral_station = Pose2d(1.187, 7.130, Rotation2d.fromDegrees(210))

        def GoTo(pose: list[Pose2d]):
            return DriveToPosesAutoFlip(pose, driv)

        def Drop():
            return DropAutonomous(
                hardware.printer,
                hardware.arm,
                hardware.elevator,
                driv,
                hardware.claw,
                "none",
                True,
            )

        self.addCommands(
            parallel(
                sequence(
                    ResetAutonomous(el, pr, arm),
                    parallel(
                        MoveElevator.toLevel3(el),
                        RetractCoral.retract(claw),
                    ),
                ),
                either(
                    GoTo(pose_tag_20),
                    GoTo(pose_tag_22),
                    lambda: is_left_side,
                ),
            ),
            Drop(),
            # coral 2
            parallel(
                either(
                    GoTo([pose_left_coral_station]),
                    GoTo(pose_right_coral_station),
                    lambda: is_left_side,
                ),
                PrepareLoading(el, arm, pr),
            ),
            WaitUntilCoral(claw),
            parallel(
                sequence(
                    LoadCoral(claw, pr),
                    RetractCoral.retract(claw),
                ),
                sequence(
                    parallel(
                        either(
                            GoTo(pose_tag_19_drop_right),
                            GoTo(pose_tag_17_drop_right),
                            lambda: is_left_side,
                        ),
                        sequence(
                            waitSeconds(0.7),
                            MoveElevator.toLevel4(el),
                        ),
                    ),
                ),
            ),
            Drop(),
            # Coral 3
            parallel(
                either(
                    GoTo([pose_left_coral_station]),
                    GoTo(pose_right_coral_station),
                    lambda: is_left_side,
                ),
                PrepareLoading(el, arm, pr),
            ),
            WaitUntilCoral(claw),
            parallel(
                sequence(
                    LoadCoral(claw, pr),
                    RetractCoral.retract(claw),
                ),
                sequence(
                    parallel(
                        either(
                            # TODO new paths with left offset
                            GoTo(pose_tag_19_drop_left),
                            GoTo(pose_tag_17_drop_left),
                            lambda: is_left_side,
                        ),
                        sequence(
                            waitSeconds(0.7),
                            MoveElevator.toLevel4(el),
                        ),
                    ),
                ),
            ),
        )
