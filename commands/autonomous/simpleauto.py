from commands2 import SequentialCommandGroup
from commands2.cmd import parallel, sequence, deadline
from wpimath.geometry import Pose2d, Rotation2d, Transform2d, Translation2d

from commands.alignwithreefside import align_with_reef_side_properties
from commands.arm.extendarm import ExtendArm
from commands.claw.retractcoral import RetractCoral
from commands.drivetrain.driverelative import DriveRelative
from commands.drivetrain.drivetoposes import DriveToPosesAutoFlip
from commands.dropprepareloading import DropPrepareLoading
from commands.elevator.maintainelevator import MaintainElevator
from commands.elevator.moveelevator import MoveElevator
from commands.resetautonomous import ResetAutonomous
from modules.hardware import HardwareModule
from ultime.vision import april_tag_field_layout


class SimpleAutonomous(SequentialCommandGroup):
    def __init__(self, hardware: HardwareModule):
        super().__init__()

        offset_drop_right = 0.0
        offset_backward_1 = align_with_reef_side_properties.backwards_1_offset
        offset_backward_2 = align_with_reef_side_properties.backwards_2_offset

        el = hardware.elevator
        pr = hardware.printer
        arm = hardware.arm
        claw = hardware.claw
        driv = hardware.drivetrain
        control = hardware.controller

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
                ),
            ]

        pose_tag_21 = GetTagWithOffset(21, offset_drop_right)

        def GoTo(pose: list[Pose2d]):
            return DriveToPosesAutoFlip(pose, driv)

        self.addCommands(
            ResetAutonomous(el, pr, arm),
            parallel(
                MoveElevator.toLevel4(el),
                RetractCoral.retract(claw),
                ExtendArm(arm),
            ),
            deadline(
                GoTo(pose_tag_21).withTimeout(3.0),
                MaintainElevator(el),
            ),
            DropPrepareLoading(pr, arm, el, driv, claw, control, "right", True),
            DriveRelative(driv, Translation2d(0.2, 0)).withTimeout(3.0)
        )
