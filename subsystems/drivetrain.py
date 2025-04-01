import math
from tkinter.constants import OUTSIDE
from typing import Dict, List, Tuple

import wpilib
import wpimath
from ntcore import NetworkTableInstance
from pathplannerlib.util import DriveFeedforwards
from rev import SparkBase
from wpilib import RobotBase
from wpimath import kinematics
from wpimath.estimator import SwerveDrive4PoseEstimator
from wpimath.geometry import Pose2d, Translation2d, Rotation2d, Twist2d
from wpimath.kinematics import (
    ChassisSpeeds,
    SwerveDrive4Kinematics,
    SwerveModuleState,
    SwerveDrive4Odometry,
    SwerveModulePosition,
)
from wpiutil import SendableBuilder

import ports
from ultime.alert import AlertType
from ultime.autoproperty import autoproperty
from ultime.gyro import ADIS16470
from ultime.subsystem import Subsystem
from ultime.swerve import SwerveModule, SwerveDriveElasticSendable
from ultime.timethis import tt


class Drivetrain(Subsystem):
    width = 0.597
    length = 0.673
    max_angular_speed = autoproperty(25.0)
    max_speed = autoproperty(4.0)

    angular_offset_fl = autoproperty(-1.57)
    angular_offset_fr = autoproperty(0.0)
    angular_offset_bl = autoproperty(3.14)
    angular_offset_br = autoproperty(1.57)

    swerve_temperature_threshold = autoproperty(55.0)

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

        self.swerve_modules = {
            "FL": self.swerve_module_fl,
            "FR": self.swerve_module_fr,
            "BL": self.swerve_module_bl,
            "BR": self.swerve_module_br,
        }

        self.last_module_position = [
            SwerveModulePosition(),
            SwerveModulePosition(),
            SwerveModulePosition(),
            SwerveModulePosition(),
        ]

        self.chassis_speed_goal_pub = (
            NetworkTableInstance.getDefault()
            .getStructTopic("Chassis Speed Goal", ChassisSpeeds)
            .publish()
        )
        self.chassis_speed_goal = ChassisSpeeds()

        self.chassis_speed_pub = (
            NetworkTableInstance.getDefault()
            .getStructTopic("Chassis Speed", ChassisSpeeds)
            .publish()
        )
        self.chassis_speed = ChassisSpeeds()

        # Gyro
        """
        Possibilités : NavX, ADIS16448, ADIS16470, ADXRS, Empty
        """
        self._gyro = ADIS16470()
        # TODO Assert _gyro is subclass of abstract class Gyro
        self.addChild("Gyro", self._gyro)

        self._field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("Field", self._field)

        swerve_drive_sendable = SwerveDriveElasticSendable(
            self.swerve_module_fl,
            self.swerve_module_fr,
            self.swerve_module_bl,
            self.swerve_module_br,
            lambda: self._gyro.getRotation2d().radians(),
        )
        wpilib.SmartDashboard.putData("SwerveDrive", swerve_drive_sendable)

        """
        Pose estimation
        """

        self.swervedrive_kinematics = SwerveDrive4Kinematics(
            self.motor_fl_loc, self.motor_fr_loc, self.motor_bl_loc, self.motor_br_loc
        )

        self.swerve_odometry = SwerveDrive4Odometry(
            self.swervedrive_kinematics,
            self._gyro.getRotation2d(),
            self.last_module_position,
            Pose2d(0, 0, 0),
        )

        self.swerve_estimator = SwerveDrive4PoseEstimator(
            self.swervedrive_kinematics,
            self._gyro.getRotation2d(),
            self.last_module_position,
            Pose2d(0, 0, 0),
        )

        self.vision_pose = self._field.getObject("Vision Pose")
        self.odometry_pose = self._field.getObject("Odometry Pose")

        """
        Alerts
        """

        self.alerts_hot = {
            location: self.createAlert(
                f"{location} Swerve is too hot. Allow swerves to cool down.",
                AlertType.Warning,
            )
            for location in self.swerve_modules.keys()
        }

        self.alerts_faults = {
            location: self.createAlert(
                f"{location} Swerve has active faults/warnings. Check for them on REV Hardware Client.",
                AlertType.Warning,
            )
            for location in self.swerve_modules.keys()
        }

        self.alerts_drive_encoder = {
            location: self.createAlert(
                f"{location} Swerve Drive encoder measured velocity is too low.",
                AlertType.Error,
            )
            for location in self.swerve_modules.keys()
        }

        self.alerts_turning_motor = {
            location: self.createAlert(
                f"{location} Swerve turning motor failed to reach desired state.",
                AlertType.Error,
            )
            for location in self.swerve_modules.keys()
        }

        self.alert_odometry = self.createAlert(
            "Odometry failed to calculate robot position accurately.", AlertType.Error
        )

        if RobotBase.isSimulation():
            self.sim_yaw = 0

    def runVelocity(self, speeds: ChassisSpeeds):
        discrete_speeds = speeds.discretize(speeds, 0.02)
        setpoint_states = self.swervedrive_kinematics.toSwerveModuleStates(
            discrete_speeds
        )
        SwerveDrive4Kinematics.desaturateWheelSpeeds(setpoint_states, self.max_speed)

        self.swerve_module_fl.runSetpoint(setpoint_states[0])
        self.swerve_module_fr.runSetpoint(setpoint_states[1])
        self.swerve_module_bl.runSetpoint(setpoint_states[2])
        self.swerve_module_br.runSetpoint(setpoint_states[3])

    def runCharacterization(self, output: float):
        self.swerve_module_fl.runCharacterization(output)
        self.swerve_module_fr.runCharacterization(output)
        self.swerve_module_bl.runCharacterization(output)
        self.swerve_module_br.runCharacterization(output)

    def stop(self):
        self.runVelocity(ChassisSpeeds())

    def stopWithX(self):
        headings = [Rotation2d(), Rotation2d(), Rotation2d(), Rotation2d()]
        headings[0] = self.swerve_module_fl.getAngleRandians()
        headings[1] = self.swerve_module_fr.getAngleRandians()
        headings[2] = self.swerve_module_bl.getAngleRandians()
        headings[3] = self.swerve_module_br.getAngleRandians()

        self.swervedrive_kinematics.resetHeadings(headings)
        self.stop()

    def getModuleStates(self) -> List[SwerveModuleState]:
        states = [
            SwerveModuleState(),
            SwerveModuleState(),
            SwerveModuleState(),
            SwerveModuleState(),
        ]
        states[0] = self.swerve_module_fl.getState()
        states[1] = self.swerve_module_fr.getState()
        states[2] = self.swerve_module_bl.getState()
        states[3] = self.swerve_module_br.getState()

        return states

    def getModulePosition(self) -> List[SwerveModuleState]:
        positions = [
            SwerveModulePosition(),
            SwerveModulePosition(),
            SwerveModulePosition(),
            SwerveModulePosition(),
        ]
        positions[0] = self.swerve_module_fl.getPosition()
        positions[1] = self.swerve_module_fr.getPosition()
        positions[2] = self.swerve_module_bl.getPosition()
        positions[3] = self.swerve_module_br.getPosition()

        return positions

    def getChassisSpeed(self) -> ChassisSpeeds:
        return self.swervedrive_kinematics.toChassisSpeeds(self.getModuleStates())

    def getWheelRadiusCharacterizationPositions(self):
        values = [0.0, 0.0, 0.0, 0.0]
        values[0] = self.swerve_module_fl.getWheelRadiusCharacterizationPosition()
        values[1] = self.swerve_module_fr.getWheelRadiusCharacterizationPosition()
        values[2] = self.swerve_module_bl.getWheelRadiusCharacterizationPosition()
        values[3] = self.swerve_module_br.getWheelRadiusCharacterizationPosition()

        return values

    def getFFCharacterizationVelocity(self):
        output = 0.0
        output += self.swerve_module_fl.getWheelRadiusCharacterizationPosition() / 4
        output += self.swerve_module_fr.getWheelRadiusCharacterizationPosition() / 4
        output += self.swerve_module_bl.getWheelRadiusCharacterizationPosition() / 4
        output += self.swerve_module_br.getWheelRadiusCharacterizationPosition() / 4

        return output

    def getPose(self):
        return self.swerve_estimator.getEstimatedPosition()

    def getAngle(self):
        """
        Wrapped between -180 and 180
        """
        return self._gyro.getAngle()

    def resetToPose(self, pose: Pose2d):
        self.swerve_estimator.resetPosition(
            self._gyro.getRotation2d(),
            self.getModulePosition(),
            pose,
        )

    def resetGyro(self):
        self._gyro.reset()

    def addVisionMeasurement(self, pose: Pose2d, timestamp: float):
        self.swerve_estimator.addVisionMeasurement(pose, timestamp)
        self.vision_pose.setPose(pose)

    def periodic(self):
        rotation = self._gyro.getRotation2d()
        swerve_positions = (
            self.swerve_module_fl.getPosition(),
            self.swerve_module_fr.getPosition(),
            self.swerve_module_bl.getPosition(),
            self.swerve_module_br.getPosition(),
        )

        chassis_speed = self.getChassisSpeed()

        self.chassis_speed_pub.set(chassis_speed)
        self.chassis_speed = chassis_speed

        self.swerve_estimator.update(rotation, swerve_positions)
        self.swerve_odometry.update(rotation, swerve_positions)

        self.odometry_pose.setPose(self.swerve_odometry.getPose())
        self._field.setRobotPose(self.swerve_estimator.getEstimatedPosition())

        for location, swerve_module in self.swerve_modules.items():
            if (
                swerve_module._driving_motor.getMotorTemperature()
                > self.swerve_temperature_threshold
                or swerve_module._turning_motor.getMotorTemperature()
                > self.swerve_temperature_threshold
            ):
                self.alerts_hot[location].set(True)
            else:
                self.alerts_hot[location].set(False)

            if (
                swerve_module._driving_motor.hasActiveFault()
                or swerve_module._turning_motor.hasActiveFault()
                or swerve_module._driving_motor.hasActiveWarning()
                or swerve_module._turning_motor.hasActiveWarning()
            ):
                self.alerts_faults[location].set(True)
            else:
                self.alerts_faults[location].set(False)

    def simulationPeriodic(self):
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

    def getCurrentDrawAmps(self):
        return 0.0

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def noop(_):
            pass

        builder.addFloatProperty("angle", tt(self.getAngle), noop)
        builder.addFloatProperty(
            "SpeedGoal",
            tt(
                lambda: math.hypot(
                    self.chassis_speed_goal.vx, self.chassis_speed_goal.vy
                )
            ),
            noop,
        )
        builder.addFloatProperty(
            "Speed",
            tt(lambda: math.hypot(self.chassis_speed.vx, self.chassis_speed.vy)),
            noop,
        )
