import math
from email.policy import default

import rev
from rev import (SparkMaxAlternateEncoder,
                 SparkMax)
from wpilib import RobotBase, RobotController
from wpilib.simulation import FlywheelSim, RoboRioSim
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.system.plant import DCMotor, LinearSystemId

from ultime.autoproperty import autoproperty
from ultime.sparkmaxsim import SparkMaxSim
from ultime.sparkmaxutils import waitForCAN

drive_motor_pinion_teeth = 13
drive_motor_gear_ratio = (45.0 * 22) / (drive_motor_pinion_teeth * 15)

wheel_radius = 0.0725  # meters
drive_encoder_position_conversion_factor = (
    math.pi * wheel_radius / drive_motor_gear_ratio
)  # meters
drive_encoder_velocity_conversion_factor = (
    drive_encoder_position_conversion_factor / 60
)  # meters per second
drive_motor_free_rps = 5676 / 60  # Neo motor max free RPM into rotations per second
drive_wheel_free_rps = drive_motor_free_rps * (2 * math.pi)

turning_encoder_position_conversion_factor = math.pi * 2  # radians
turning_encoder_velocity_conversion_factor = math.pi * 2 / 60  # radians per second

turning_encoder_position_PID_min_input = 0
turning_encoder_position_PID_max_input = turning_encoder_position_conversion_factor

class SwerveModule:
    max_speed = autoproperty(35.0)

    driving_PID_P = autoproperty(0.04)
    driving_PID_I = autoproperty(0.0)
    driving_PID_D = autoproperty(0.0)
    driving_PID_feedforward = autoproperty(0.0016823989756014307)
    driving_PID_output_min = autoproperty(-1.0)
    driving_PID_output_max = autoproperty(1.0)

    turning_PID_P = autoproperty(0.4)
    turning_PID_I = autoproperty(0.0)
    turning_PID_D = autoproperty(0.0)
    turning_PID_feedforward = autoproperty(0.0)
    turning_PID_output_min = autoproperty(-1.0)
    turning_PID_output_max = autoproperty(1.0)

    def __init__(self, drive_motor_port, turning_motor_port, chassis_angular_offset: float):
        self._drive_motor = SparkMax(
            drive_motor_port, SparkMax.MotorType.kBrushless
        )

        self._turning_motor = SparkMax(
            turning_motor_port, SparkMax.MotorType.kBrushless
        )

        self._drive_motor.ResetMode(1)# 1 for kResetSafeParameters
        self._turning_motor.ResetMode(1)# 1 for kResetSafeParameters

        self._drive_encoder = self._drive_motor.getEncoder()
        self._turning_encoder = self._turning_motor.getAbsoluteEncoder()
        self._drive_PIDController = self._drive_motor.getClosedLoopController()
        self._turning_PIDController = self._turning_motor.getClosedLoopController()
        self._drive_PIDController.setFeedbackDevice(self._drive_encoder)
        self._turning_PIDController.setFeedbackDevice(self._turning_encoder)



        self._drive_encoder.setPositionConversionFactor(
            drive_encoder_position_conversion_factor
        )
        self._drive_encoder.setVelocityConversionFactor(
            drive_encoder_velocity_conversion_factor
        )
        self._turning_encoder.setPositionConversionFactor(
            turning_encoder_position_conversion_factor
        )
        self._turning_encoder.setVelocityConversionFactor(
            turning_encoder_velocity_conversion_factor
        )

        self._turning_encoder.setInverted(True)

        self._turning_PIDController.setPositionPIDWrappingEnabled(True)
        self._turning_PIDController.setPositionPIDWrappingMinInput(
            turning_encoder_position_PID_min_input
        )
        self._turning_PIDController.setPositionPIDWrappingMaxInput(
            turning_encoder_position_PID_max_input
        )

        self._drive_PIDController.setP(self.driving_PID_P)
        self._drive_PIDController.setI(self.driving_PID_I)
        self._drive_PIDController.setD(self.driving_PID_D)
        self._drive_PIDController.setFF(self.driving_PID_feedforward)
        self._drive_PIDController.setOutputRange(
            self.driving_PID_output_min, self.driving_PID_output_max
        )

        self._turning_PIDController.setP(self.turning_PID_P)
        self._turning_PIDController.setI(self.turning_PID_I)
        self._turning_PIDController.setD(self.turning_PID_D)
        self._turning_PIDController.setFF(self.turning_PID_feedforward)
        self._turning_PIDController.setOutputRange(
            self.turning_PID_output_min, self.turning_PID_output_max
        )

        self._drive_motor.IdleMode(1)# 1 for kbrake
        self._turning_motor.IdleMode(1)# 1 for kbrake
        #self._drive_motor.setSmartCurrentLimit(25)
        #don't know Current limit in 2025
        #self._turning_motor.setSmartCurrentLimit(25)

        # Save the SPARK MAX configurations. If a SPARK MAX browns out during
        # operation, it will maintain the above configurations.
        self._drive_motor.PersistMode(1)# 1 for kPersistParameters
        self._turning_motor.PersistMode(1)# 1 for kPersistParameters

        self._chassis_angular_offset = chassis_angular_offset
        self._drive_encoder.setPosition(0)

        waitForCAN(4.0)

        if RobotBase.isSimulation():
            # Simulation things
            self.sim_drive_encoder = SparkMaxSim(self._drive_motor)
            self.sim_turn_encoder = SparkMaxSim(self._turning_motor)

            self.sim_turn_encoder_distance: float = 0.0
            self.sim_drive_encoder_distance: float = 0.0

            # Flywheels allow simulation of a more physically realistic rendering of swerve module properties
            # Magical values for sim pulled from :
            # https://github.com/4201VitruvianBots/2021SwerveSim/blob/main/Swerve2021/src/main/java/frc/robot/subsystems/SwerveModule.java
            turn_motor_gear_ratio = 12.8  # //12 to 1

            self.sim_turn_motor = FlywheelSim(
                LinearSystemId.identifyVelocitySystemMeters(0.16, 0.0348),
                DCMotor.NEO550(1),
                turn_motor_gear_ratio,
            )
            self.sim_drive_motor = FlywheelSim(
                LinearSystemId.identifyVelocitySystemMeters(3, 1.24),
                DCMotor.NEO550(1),
                drive_motor_gear_ratio,
            )

    def getVelocity(self) -> float:
        return self._drive_encoder.getVelocity()

    def getTurningRadians(self) -> float:
        """
        Returns radians
        """
        return self._turning_encoder.getPosition()

    def getState(self) -> SwerveModuleState:
        return SwerveModuleState(
            self.getVelocity(),
            Rotation2d(self.getTurningRadians() - self._chassis_angular_offset),
        )

    def getModuleEncoderPosition(self) -> float:
        return self._drive_encoder.getPosition()

    def getPosition(self) -> SwerveModulePosition:
        return SwerveModulePosition(
            self.getModuleEncoderPosition(),
            Rotation2d(self.getTurningRadians() - self._chassis_angular_offset),
        )

    def setDesiredState(self, desired_state: SwerveModuleState):
        corrected_desired_state = SwerveModuleState()
        corrected_desired_state.speed = desired_state.speed
        corrected_desired_state.angle = desired_state.angle.rotateBy(
            Rotation2d(self._chassis_angular_offset)
        )
        current_rotation = Rotation2d(self._turning_encoder.getPosition())

        optimized_desired_state = SwerveModuleState.optimize(
            corrected_desired_state, current_rotation
        )

        optimized_desired_state.speed *= (
                current_rotation - optimized_desired_state.angle
        ).cos()

        self._drive_PIDController.setReference(
            optimized_desired_state.speed, SparkMax.ControlType.kVelocity
        )
        self._turning_PIDController.setReference(
            optimized_desired_state.angle.radians(), SparkMax.ControlType.kPosition
        )

    def stop(self):
        self._drive_motor.setVoltage(0.0)
        self._turning_motor.setVoltage(0.0)

    def simulationUpdate(self, period: float):
        module_max_angular_acceleration = 2 * math.pi  # radians per second squared

        self.sim_turn_motor.setInputVoltage(
            self.sim_turn_encoder.getVelocity()
            / module_max_angular_acceleration
            * RobotController.getBatteryVoltage()
        )
        self.sim_drive_motor.setInputVoltage(
            self.sim_drive_encoder.getVelocity()
            / self.max_speed
            * RobotController.getBatteryVoltage()
        )

        self.sim_drive_motor.update(period)
        self.sim_turn_motor.update(period)

        self.sim_turn_encoder_distance += (
                self.sim_turn_motor.getAngularVelocity() * period
        )

        self.sim_turn_encoder.setPosition(self.sim_turn_encoder_distance)
        self.sim_turn_encoder.setVelocity(self.sim_turn_motor.getAngularVelocity())

        self.sim_drive_encoder_distance += (
                self.sim_drive_motor.getAngularVelocity() * period
        )
        self.sim_drive_encoder.setPosition(self.sim_drive_encoder_distance)
        self.sim_drive_encoder.setVelocity(self.sim_drive_motor.getAngularVelocity())
