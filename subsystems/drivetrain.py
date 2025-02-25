import math

import wpilib
import wpimath
from commands2 import Command
from pathplannerlib.auto import AutoBuilder
from pathplannerlib.config import RobotConfig, PIDConstants
from pathplannerlib.controller import PPHolonomicDriveController
from pathplannerlib.path import PathPlannerPath
from pathplannerlib.telemetry import PPLibTelemetry
from pathplannerlib.trajectory import PathPlannerTrajectoryState
from pathplannerlib.util import DriveFeedforwards
from photonlibpy.photonCamera import PhotonCamera
from wpilib import RobotBase, DriverStation
from wpimath._controls._controls.trajectory import Trajectory
from wpimath.estimator import SwerveDrive4PoseEstimator
from wpimath.geometry import Pose2d, Translation2d, Rotation2d, Twist2d
from wpimath.kinematics import (
    ChassisSpeeds,
    SwerveDrive4Kinematics,
    SwerveModuleState,
    SwerveDrive4Odometry,
)
from wpiutil import SendableBuilder

import ports
from ultime.autoproperty import autoproperty
from ultime.gyro import ADIS16470
from ultime.subsystem import Subsystem
from ultime.swerve import SwerveModule
from ultime.swerveconfig import SwerveConstants


class Drivetrain(Subsystem):
    width = 0.597
    length = 0.673
    max_angular_speed = autoproperty(25.0)

    angular_offset_fl = autoproperty(-1.57)
    angular_offset_fr = autoproperty(0.0)
    angular_offset_bl = autoproperty(3.14)
    angular_offset_br = autoproperty(1.57)

    def __init__(self) -> None:
        super().__init__()
        self.period_seconds = 0.02

        # Swerve Module motor positions
        self.motor_fl_loc = Translation2d(self.width / 2, self.length / 2)
        self.motor_fr_loc = Translation2d(self.width / 2, -self.length / 2)
        self.motor_bl_loc = Translation2d(-self.width / 2, self.length / 2)
        self.motor_br_loc = Translation2d(-self.width / 2, -self.length / 2)

        self.swerve_module_fl = SwerveModule(
            ports.CAN.drivetrain_motor_driving_fl,
            ports.CAN.drivetrain_motor_turning_fl,
            self.angular_offset_fl,
        )

        self.swerve_module_fr = SwerveModule(
            ports.CAN.drivetrain_motor_driving_fr,
            ports.CAN.drivetrain_motor_turning_fr,
            self.angular_offset_fr,
        )

        self.swerve_module_bl = SwerveModule(
            ports.CAN.drivetrain_motor_driving_bl,
            ports.CAN.drivetrain_motor_turning_bl,
            self.angular_offset_bl,
        )

        self.swerve_module_br = SwerveModule(
            ports.CAN.drivetrain_motor_driving_br,
            ports.CAN.drivetrain_motor_turning_br,
            self.angular_offset_br,
        )

        # Gyro
        """
        Possibilités : NavX, ADIS16448, ADIS16470, ADXRS, Empty
        """
        self._gyro = ADIS16470()
        # TODO Assert _gyro is subclass of abstract class Gyro
        self.addChild("Gyro", self._gyro)

        self._field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("Field", self._field)

        self.swervedrive_kinematics = SwerveDrive4Kinematics(
            self.motor_fl_loc, self.motor_fr_loc, self.motor_bl_loc, self.motor_br_loc
        )
        self.swerve_odometry = SwerveDrive4Odometry(
            self.swervedrive_kinematics,
            self._gyro.getRotation2d(),
            (
                self.swerve_module_fl.getPosition(),
                self.swerve_module_fr.getPosition(),
                self.swerve_module_bl.getPosition(),
                self.swerve_module_br.getPosition(),
            ),
            Pose2d(0, 0, 0),
        )

        self.swerve_estimator = SwerveDrive4PoseEstimator(
            self.swervedrive_kinematics,
            self._gyro.getRotation2d(),
            (
                self.swerve_module_fl.getPosition(),
                self.swerve_module_fr.getPosition(),
                self.swerve_module_bl.getPosition(),
                self.swerve_module_br.getPosition(),
            ),
            Pose2d(0, 0, 0),
        )
        self.cam = PhotonCamera("mainCamera")
        self.vision_pose = self._field.getObject("Vision Pose")
        self.odometry_pose = self._field.getObject("Odometry Pose")

        # AutoBuilder Configured with base PP functions. Only one that supports Pathfinding
        # Must test which AutoBuilder works best
        AutoBuilder.configure(
            self.getPose,
            self.resetToPose,
            self.getRobotRelativeChassisSpeeds,
            self.driveFromChassisSpeeds,
            PPHolonomicDriveController(
                PIDConstants(5, 0, 0),
                PIDConstants(5, 0, 0),
            ),
            RobotConfig.fromGUISettings(),
            should_flip_path,
            self,
        )

        # Flipping must be done by the command because the AutoBuilder uses custom code
        # AutoBuilder.configureCustom(
        #     self.getCommandFromPathplannerPath, self.resetToPose, True, should_flip_path
        # )

        if RobotBase.isSimulation():
            self.sim_yaw = 0

    def getCommandFromPathplannerPath(self, path: PathPlannerPath):
        return FollowPathplannerPath(path, self)

    def drive(
        self,
        x_speed_input: float,
        y_speed_input: float,
        rot_speed: float,
        is_field_relative: bool,
    ):
        x_speed = x_speed_input * SwerveConstants.max_speed_per_second
        y_speed = y_speed_input * SwerveConstants.max_speed_per_second
        rot_speed = rot_speed * self.max_angular_speed
        self.driveRaw(x_speed, y_speed, rot_speed, is_field_relative)

    def driveFromChassisSpeeds(
        self, speeds: ChassisSpeeds, _ff: DriveFeedforwards
    ) -> None:
        corrected_chassis_speed = self.correctForDynamics(speeds)

        swerve_module_states = self.swervedrive_kinematics.toSwerveModuleStates(
            corrected_chassis_speed
        )

        SwerveDrive4Kinematics.desaturateWheelSpeeds(
            swerve_module_states, SwerveConstants.max_speed_per_second
        )
        self.swerve_module_fl.setDesiredState(swerve_module_states[0])
        self.swerve_module_fr.setDesiredState(swerve_module_states[1])
        self.swerve_module_bl.setDesiredState(swerve_module_states[2])
        self.swerve_module_br.setDesiredState(swerve_module_states[3])

    def driveRaw(
        self,
        x_speed: float,
        y_speed: float,
        rot_speed: float,
        is_field_relative: bool,
    ):
        if is_field_relative:
            base_chassis_speed = ChassisSpeeds.fromFieldRelativeSpeeds(
                x_speed, y_speed, rot_speed, self.getPose().rotation()
            )
        else:
            base_chassis_speed = ChassisSpeeds(x_speed, y_speed, rot_speed)

        corrected_chassis_speed = self.correctForDynamics(base_chassis_speed)

        swerve_module_states = self.swervedrive_kinematics.toSwerveModuleStates(
            corrected_chassis_speed
        )

        SwerveDrive4Kinematics.desaturateWheelSpeeds(
            swerve_module_states, SwerveConstants.max_speed_per_second
        )
        self.swerve_module_fl.setDesiredState(swerve_module_states[0])
        self.swerve_module_fr.setDesiredState(swerve_module_states[1])
        self.swerve_module_bl.setDesiredState(swerve_module_states[2])
        self.swerve_module_br.setDesiredState(swerve_module_states[3])

    def getAngle(self):
        """
        Wrapped between -180 and 180
        """
        return self._gyro.getAngle()

    def resetGyro(self):
        self._gyro.reset()

    def getPose(self):
        return self.swerve_estimator.getEstimatedPosition()

    def setXFormation(self):
        """
        Points all the wheels into the center to prevent movement
        """
        self.swerve_module_fl.setDesiredState(
            SwerveModuleState(0, Rotation2d.fromDegrees(45))
        )
        self.swerve_module_fr.setDesiredState(
            SwerveModuleState(0, Rotation2d.fromDegrees(-45))
        )
        self.swerve_module_bl.setDesiredState(
            SwerveModuleState(0, Rotation2d.fromDegrees(-45))
        )
        self.swerve_module_br.setDesiredState(
            SwerveModuleState(0, Rotation2d.fromDegrees(45))
        )

    def stop(self):
        self.swerve_module_fr.stop()
        self.swerve_module_fl.stop()
        self.swerve_module_bl.stop()
        self.swerve_module_br.stop()

    def correctForDynamics(
        self, original_chassis_speeds: ChassisSpeeds
    ) -> ChassisSpeeds:
        next_robot_pose: Pose2d = Pose2d(
            original_chassis_speeds.vx * self.period_seconds,
            original_chassis_speeds.vy * self.period_seconds,
            Rotation2d(original_chassis_speeds.omega * self.period_seconds),
        )
        pose_twist: Twist2d = Pose2d().log(next_robot_pose)
        updated_speeds: ChassisSpeeds = ChassisSpeeds(
            pose_twist.dx / self.period_seconds,
            pose_twist.dy / self.period_seconds,
            pose_twist.dtheta / self.period_seconds,
        )
        return updated_speeds

    def periodic(self):
        self.swerve_estimator.update(
            self._gyro.getRotation2d(),
            (
                self.swerve_module_fl.getPosition(),
                self.swerve_module_fr.getPosition(),
                self.swerve_module_bl.getPosition(),
                self.swerve_module_br.getPosition(),
            ),
        )

        self.swerve_odometry.update(
            self._gyro.getRotation2d(),
            (
                self.swerve_module_fl.getPosition(),
                self.swerve_module_fr.getPosition(),
                self.swerve_module_bl.getPosition(),
                self.swerve_module_br.getPosition(),
            ),
        )

        self.odometry_pose.setPose(self.swerve_odometry.getPose())
        self._field.setRobotPose(self.swerve_estimator.getEstimatedPosition())

    def simulationPeriodic(self):
        wpilib.SmartDashboard.putNumberArray(
            "SwerveStates",
            [
                self.swerve_module_fl.getState().angle.degrees(),
                self.swerve_module_fl.getState().speed,
                self.swerve_module_fr.getState().angle.degrees(),
                self.swerve_module_fr.getState().speed,
                self.swerve_module_bl.getState().angle.degrees(),
                self.swerve_module_bl.getState().speed,
                self.swerve_module_br.getState().angle.degrees(),
                self.swerve_module_br.getState().speed,
            ],
        )

        self.swerve_module_fl.simulationUpdate(self.period_seconds)
        self.swerve_module_fr.simulationUpdate(self.period_seconds)
        self.swerve_module_bl.simulationUpdate(self.period_seconds)
        self.swerve_module_br.simulationUpdate(self.period_seconds)

        module_states = (
            self.swerve_module_fl.getState(),
            self.swerve_module_fr.getState(),
            self.swerve_module_bl.getState(),
            self.swerve_module_br.getState(),
        )
        chassis_speed = self.swervedrive_kinematics.toChassisSpeeds(module_states)
        chassis_rotation_speed = chassis_speed.omega
        self.sim_yaw += chassis_rotation_speed * self.period_seconds
        self._gyro.setSimAngle(math.degrees(self.sim_yaw))

    def getRobotRelativeChassisSpeeds(self):
        """
        Returns robot relative chassis speeds from current swerve module states
        """
        module_states = (
            self.swerve_module_fl.getState(),
            self.swerve_module_fr.getState(),
            self.swerve_module_bl.getState(),
            self.swerve_module_br.getState(),
        )
        chassis_speed = self.swervedrive_kinematics.toChassisSpeeds(module_states)
        return chassis_speed

    def resetToPose(self, pose: Pose2d):
        self.swerve_estimator.resetPosition(
            self._gyro.getRotation2d(),
            (
                self.swerve_module_fl.getPosition(),
                self.swerve_module_fr.getPosition(),
                self.swerve_module_bl.getPosition(),
                self.swerve_module_br.getPosition(),
            ),
            pose,
        )

    def addVisionMeasurement(self, pose: wpimath.geometry.Pose3d, timestamp: float):
        self.swerve_estimator.addVisionMeasurement(pose, timestamp)
        self.vision_pose.setPose(pose.toPose2d())

    def getCurrentDrawAmps(self):
        return 0.0

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def noop(_):
            pass

        builder.addFloatProperty("angle", self.getAngle, noop)


def should_flip_path():
    # Boolean supplier that controls when the path will be mirrored for the red alliance
    # This will flip the path being followed to the red side of the field.
    # THE ORIGIN WILL REMAIN ON THE BLUE SIDE
    return DriverStation.getAlliance() == DriverStation.Alliance.kRed


class FollowPathplannerPath(Command):
    delta_t = autoproperty(0.08)
    pos_tolerance = autoproperty(0.3)
    rot_tolerance = autoproperty(0.5)

    def __init__(self, pathplanner_path: PathPlannerPath, drivetrain: Drivetrain):
        super().__init__()
        self.sampled_trajectory = None
        self.drivetrain = drivetrain
        self.pathplanner_path_base = pathplanner_path
        self.addRequirements(drivetrain)
        self.sampled_trajectory: list[PathPlannerTrajectoryState] = []
        self.current_goal = 0
        self.flipped_path = pathplanner_path.flipPath()

    def initialize(self):
        self.current_goal = 0
        self.sampled_trajectory = []

        pathplanner_path = (
            self.flipped_path if should_flip_path() else self.pathplanner_path_base
        )
        PPLibTelemetry.setCurrentPath(pathplanner_path)
        trajectory = pathplanner_path.getIdealTrajectory(RobotConfig.fromGUISettings())
        states = []
        for state in trajectory.getStates():
            # Calculate acceleration from velocity change if needed
            acceleration = 0.0  # Or calculate based on velocity differences
            heading_rad = state.heading.radians()
            states.append(
                Trajectory.State(
                    state.timeSeconds,
                    state.linearVelocity,
                    acceleration,
                    state.pose,
                    heading_rad,
                )
            )
        self.drivetrain._field.getObject("traj").setTrajectory(Trajectory(states))
        for i in range(math.ceil(trajectory.getEndState().timeSeconds / self.delta_t)):
            self.sampled_trajectory.append(trajectory.sample(i * self.delta_t))

    def execute(self):
        PPLibTelemetry.setCurrentPose(self.drivetrain.getPose())
        PPLibTelemetry.setTargetPose(
            Pose2d(
                self.sampled_trajectory[self.current_goal].pose.X(),
                self.sampled_trajectory[self.current_goal].pose.Y(),
                self.sampled_trajectory[self.current_goal].pose.rotation(),
            )
        )
        position_error = (
            self.sampled_trajectory[self.current_goal].pose.translation()
            - self.drivetrain.getPose().translation()
        )
        rotation_error: Rotation2d = (
            self.sampled_trajectory[self.current_goal].pose.rotation()
            - self.drivetrain.getPose().rotation()
        )
        if (
            math.hypot(position_error.X(), position_error.Y()) <= self.pos_tolerance
            and rotation_error.degrees() <= self.rot_tolerance
        ):
            self.current_goal += 1
        else:
            PPLibTelemetry.setVelocities(
                math.hypot(
                    self.drivetrain.getRobotRelativeChassisSpeeds().vx,
                    self.drivetrain.getRobotRelativeChassisSpeeds().vy,
                ),
                math.copysign(
                    min(
                        self.sampled_trajectory[self.current_goal].linearVelocity,
                        abs(position_error.X()),
                    ),
                    position_error.X(),
                ),
                rotation_error.radians(),
                self.drivetrain.getRobotRelativeChassisSpeeds().omega,
            )
            self.drivetrain.drive(
                math.copysign(
                    min(
                        self.sampled_trajectory[self.current_goal].linearVelocity,
                        abs(
                            position_error.X()
                            * self.sampled_trajectory[self.current_goal].linearVelocity
                        ),
                    ),
                    position_error.X(),
                ),
                math.copysign(
                    min(
                        self.sampled_trajectory[self.current_goal].linearVelocity,
                        abs(
                            position_error.Y()
                            * self.sampled_trajectory[self.current_goal].linearVelocity
                        ),
                    ),
                    position_error.Y(),
                ),
                rotation_error.radians(),
                True,
            )

    def isFinished(self) -> bool:
        return self.current_goal >= len(self.sampled_trajectory)

    def end(self, interrupted: bool):
        self.drivetrain.drive(0, 0, 0, True)

        if interrupted:
            self.current_goal = 0
            self.sampled_trajectory = []
