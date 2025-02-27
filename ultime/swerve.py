import math
from typing import Callable

from rev import SparkMax, SparkBase, SparkSim
from wpilib import RobotBase
from wpilib.simulation import RoboRioSim
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.system.plant import DCMotor
from wpiutil import Sendable, SendableBuilder

from ultime import swerveconfig


def radians_per_second_to_rpm(rps: float):
    return rps * 60 / 2 / math.pi


class SwerveModule:
    def __init__(
        self,
        drive_motor_port,
        turning_motor_port,
        chassis_angular_offset: float,
    ):
        self._driving_motor = SparkMax(drive_motor_port, SparkMax.MotorType.kBrushless)
        self._turning_motor = SparkMax(
            turning_motor_port, SparkMax.MotorType.kBrushless
        )
        self.desired_state = SwerveModuleState(0.0, Rotation2d())

        self._driving_encoder = self._driving_motor.getEncoder()
        self._turning_encoder = self._turning_motor.getAbsoluteEncoder()

        self._driving_motor.configure(
            swerveconfig.driving_config,
            SparkBase.ResetMode.kResetSafeParameters,
            SparkBase.PersistMode.kPersistParameters,
        )
        self._turning_motor.configure(
            swerveconfig.turning_config,
            SparkBase.ResetMode.kResetSafeParameters,
            SparkBase.PersistMode.kPersistParameters,
        )

        self._driving_closed_loop_controller = (
            self._driving_motor.getClosedLoopController()
        )
        self._turning_closed_loop_controller = (
            self._turning_motor.getClosedLoopController()
        )

        self._chassis_angular_offset = chassis_angular_offset
        self.desired_state.angle = Rotation2d(self._turning_encoder.getPosition())
        self._driving_encoder.setPosition(0)

        if RobotBase.isSimulation():
            self.sim_driving_motor = SparkSim(self._driving_motor, DCMotor.NEO())
            self.sim_encoder_drive = self.sim_driving_motor.getRelativeEncoderSim()

            self.sim_turning_motor = SparkSim(self._turning_motor, DCMotor.NEO550())
            self.sim_encoder_turn = self.sim_turning_motor.getAbsoluteEncoderSim()

    def getVelocity(self) -> float:
        return self._driving_encoder.getVelocity()

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
        return self._driving_encoder.getPosition()

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

        corrected_desired_state.optimize(current_rotation)

        corrected_desired_state.speed *= (
            current_rotation - corrected_desired_state.angle
        ).cos()

        self._driving_closed_loop_controller.setReference(
            corrected_desired_state.speed, SparkBase.ControlType.kVelocity
        )
        self._turning_closed_loop_controller.setReference(
            corrected_desired_state.angle.radians(), SparkBase.ControlType.kPosition
        )
        self.desired_state = desired_state

    def stop(self):
        self._driving_motor.setVoltage(0.0)
        self._turning_motor.setVoltage(0.0)

    def simulationUpdate(self, period: float):
        # Drive motor simulation
        drive_voltage = (
            self._driving_motor.getAppliedOutput() * RoboRioSim.getVInVoltage()
        )
        self.sim_driving_motor.iterate(
            drive_voltage, RoboRioSim.getVInVoltage(), period
        )

        # Update drive encoder
        self.sim_encoder_drive.setPosition(self.sim_driving_motor.getPosition())
        self.sim_encoder_drive.setVelocity(self.sim_driving_motor.getVelocity())

        # Turn motor simulation
        turn_voltage = (
            self._turning_motor.getAppliedOutput() * RoboRioSim.getVInVoltage()
        )
        self.sim_turning_motor.iterate(turn_voltage, RoboRioSim.getVInVoltage(), period)

        # Update turn encoder
        current_turn_pos = self.sim_turning_motor.getPosition()
        # Normalize angle to -π to π
        normalized_pos = ((current_turn_pos + math.pi) % (2 * math.pi)) - math.pi
        self.sim_encoder_turn.setPosition(normalized_pos)
        self.sim_encoder_turn.setVelocity(self.sim_turning_motor.getVelocity())


class SwerveDriveElasticSendable(Sendable):
    def __init__(
            self,
            module_fl: SwerveModule,
            module_fr: SwerveModule,
            module_bl: SwerveModule,
            module_br: SwerveModule,
            get_robot_angle_radians: Callable[[], float],
    ):
        super().__init__()
        self.module_fl = module_fl
        self.module_fr = module_fr
        self.module_bl = module_bl
        self.module_br = module_br
        self.get_robot_angle_radians = get_robot_angle_radians

    def initSendable(self, builder: SendableBuilder):
        def noop(_):
            pass

        builder.setSmartDashboardType("SwerveDrive")

        builder.addDoubleProperty("Front Left Angle", lambda: self.module_fl.getPosition().angle.radians(), noop)
        builder.addDoubleProperty("Front Left Velocity", self.module_fl.getVelocity, noop)

        builder.addDoubleProperty("Front Right Angle", lambda: self.module_fr.getPosition().angle.radians(), noop)
        builder.addDoubleProperty("Front Right Velocity", self.module_fr.getVelocity, noop)

        builder.addDoubleProperty("Back Left Angle", lambda: self.module_bl.getPosition().angle.radians(), noop)
        builder.addDoubleProperty("Back Left Velocity", self.module_bl.getVelocity, noop)

        builder.addDoubleProperty("Back Right Angle", lambda: self.module_br.getPosition().angle.radians(), noop)
        builder.addDoubleProperty("Back Right Velocity", self.module_br.getVelocity, noop)

        builder.addDoubleProperty("Robot Angle", self.get_robot_angle_radians, noop)