import math

import wpilib
from photonlibpy.photonCamera import PhotonCamera
from wpilib import RobotBase, ADIS16470_IMU
from wpimath.estimator import SwerveDrive4PoseEstimator
from wpimath.geometry import Pose2d, Translation2d, Rotation2d, Twist2d
from wpimath.kinematics import (
    ChassisSpeeds,
    SwerveDrive4Kinematics,
    SwerveModuleState,
    SwerveDrive2Odometry,
    SwerveDrive4Odometry,
)

import ports
from ultime.gyro import ADIS16470
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem
from ultime.swerve import SwerveModule

from ultime.swerveconstants import Constants


class Drivetrain(Subsystem):
    width = 0.597
    length = 0.597
    max_angular_speed = autoproperty(25.0)

    angular_offset_fl = autoproperty(-1.57)
    angular_offset_fr = autoproperty(0.0)
    angular_offset_bl = autoproperty(3.14)
    angular_offset_br = autoproperty(1.57)

    def __init__(self, period: float) -> None:
        super().__init__()
        self.period_seconds = period

        self.constants = Constants.DriveConstants
    def getCurrentDrawAmps(self):
        return 0.0

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

        if RobotBase.isSimulation():
            self.sim_yaw = 0

    def drive(
        self,
        x_speed_input: float,
        y_speed_input: float,
        rot_speed: float,
        is_field_relative: bool,
    ):
        x_speed = x_speed_input * self.constants.max_speed_per_second
        y_speed = y_speed_input * self.constants.max_speed_per_second
        rot_speed = rot_speed * self.max_angular_speed
        self.driveRaw(x_speed, y_speed, rot_speed, is_field_relative)

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
            swerve_module_states, self.constants.max_speed_per_second
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
