import math

from pyfrc.physics.units import units
from rev import SparkMax, SparkBaseConfig, SparkBase, ClosedLoopConfig, SparkLowLevel
from rev import SparkMaxSim
from wpilib import RobotBase, RobotController
from wpilib.simulation import FlywheelSim, RoboRioSim
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.system.plant import DCMotor, LinearSystemId

from subsystems import drivetrain
from ultime.autoproperty import autoproperty
from ultime.usparkmaxsim import USparkMaxSim
from ultime.sparkmaxutils import waitForCAN

# 45 teeth on the wheel's bevel gear, 22 teeth on the first-stage spur gear, 15 teeth on the bevel pinion
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


def radians_per_second_to_rpm(rps: float):
    return rps * 60 / 2 / math.pi


class SwerveModule:
    max_speed = autoproperty(50.0)

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

    def __init__(
        self,
        drive_motor_port,
        turning_motor_port,
        chassis_angular_offset: float,
    ):
        self._drive_motor = SparkMax(drive_motor_port, SparkMax.MotorType.kBrushless)

        self._turning_motor = SparkMax(
            turning_motor_port, SparkMax.MotorType.kBrushless
        )

        # Restore SparkMax controllers to factory defaults
        drive_config = SparkBaseConfig()
        turn_config = SparkBaseConfig()

        (
            drive_config.setIdleMode(SparkBaseConfig.IdleMode.kBrake).smartCurrentLimit(
                25
            )
        )

        (
            drive_config.encoder.velocityConversionFactor(
                drive_encoder_velocity_conversion_factor
            ).positionConversionFactor(drive_encoder_position_conversion_factor)
        )

        (
            drive_config.closedLoop.pid(
                self.driving_PID_P,
                self.driving_PID_I,
                self.driving_PID_D,
            )
            .velocityFF(self.driving_PID_feedforward)
            .positionWrappingEnabled(True)
            .outputRange(-1.0, 1.0)
        )

        (turn_config.setIdleMode(SparkBaseConfig.IdleMode.kBrake).smartCurrentLimit(25))

        (
            turn_config.absoluteEncoder.velocityConversionFactor(
                turning_encoder_velocity_conversion_factor
            )
            .positionConversionFactor(turning_encoder_position_conversion_factor)
            .inverted(True)
        )

        (
            turn_config.closedLoop.pidf(
                self.turning_PID_P,
                self.turning_PID_I,
                self.turning_PID_D,
                self.turning_PID_feedforward,
            )
            .setFeedbackSensor(ClosedLoopConfig.FeedbackSensor.kAbsoluteEncoder)
            .positionWrappingEnabled(True)
            .positionWrappingInputRange(
                0, turning_encoder_position_conversion_factor
            )
            .outputRange(-1.0, 1.0)
        )

        self._drive_motor.configure(
            drive_config,
            SparkBase.ResetMode.kNoResetSafeParameters,
            SparkBase.PersistMode.kPersistParameters,
        )
        self._turning_motor.configure(
            turn_config,
            SparkBase.ResetMode.kNoResetSafeParameters,
            SparkBase.PersistMode.kPersistParameters,
        )

        self._drive_PIDController = self._drive_motor.getClosedLoopController()
        self._turning_PIDController = self._turning_motor.getClosedLoopController()

        self._drive_encoder = self._drive_motor.getEncoder()
        self._turning_encoder = self._turning_motor.getAbsoluteEncoder()
        self._chassis_angular_offset = chassis_angular_offset
        self._drive_encoder.setPosition(0)

        waitForCAN(4.0)

        if RobotBase.isSimulation():
            # Simulation things
            self.sim_encoder_distance_turn: float = 0.0
            self.sim_encoder_distance_drive: float = 0.0

            # Flywheels allow simulation of a more physically realistic rendering of swerve module properties
            # Magical values for sim pulled from :
            # https://github.com/4201VitruvianBots/2021SwerveSim/blob/main/Swerve2021/src/main/java/frc/robot/subsystems/SwerveModule.java
            turn_motor_gear_ratio = 12.8  # //12 to 1

            self.sim_wheel_turn = FlywheelSim(
                LinearSystemId.identifyVelocitySystemMeters(0.1, 0.02),
                DCMotor.NEO550(1),
                [0.0],
            )
            self.sim_motor_turn = SparkMaxSim(self._turning_motor, DCMotor.NEO550(1))

            self.sim_wheel_drive = FlywheelSim(
                LinearSystemId.identifyVelocitySystemMeters(2, 1.0),
                DCMotor.NEO(1),
                [0.0],
            )
            self.sim_motor_drive = SparkMaxSim(self._drive_motor, DCMotor.NEO(1))

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

    def  getModuleEncoderPosition(self) -> float:
        return self._drive_encoder.getPosition()

    def getPosition(self) -> SwerveModulePosition:
        return SwerveModulePosition(
            self.getModuleEncoderPosition(),
            Rotation2d(self.getTurningRadians() - self._chassis_angular_offset),
        )

    # def getHolonomicPathFollowerConfig(self) -> HolonomicPathFollowerConfig:
    #     return HolonomicPathFollowerConfig(
    #         PIDConstants(self.driving_PID_P, self.driving_PID_I, self.driving_PID_D),
    #         PIDConstants(self.turning_PID_P, self.turning_PID_I, self.turning_PID_D),
    #         self.max_speed,
    #         math.sqrt((drivetrain.width / 2) ** 2 + (drivetrain.length / 2) ** 2),
    #         # Recalculates path often because robot doesn't follow path very closely
    #         ReplanningConfig(enableDynamicReplanning=False),
    #     )

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

        self._drive_PIDController.setReference(
            corrected_desired_state.speed, SparkMax.ControlType.kVelocity
        )
        self._turning_PIDController.setReference(
            corrected_desired_state.angle.radians(), SparkMax.ControlType.kPosition
        )

    def stop(self):
        self._drive_motor.setVoltage(0.0)
        self._turning_motor.setVoltage(0.0)

    def simulationUpdate(self, period: float):
        # module_max_angular_acceleration = 2 * math.pi  # radians per second squared

        # Drive

        self.sim_wheel_drive.setInputVoltage(
            self.sim_motor_drive.getAppliedOutput()
            * RoboRioSim.getVInVoltage()
        )

        self.sim_wheel_drive.update(period)

        self.sim_motor_drive.iterate(
            radians_per_second_to_rpm(self.sim_wheel_drive.getAngularVelocity()),
            RoboRioSim.getVInVoltage(),
            period,
        )

        # Turn

        self.sim_wheel_turn.setInputVoltage(
            self.sim_motor_turn.getAppliedOutput()
            * RoboRioSim.getVInVoltage()
        )

        self.sim_wheel_turn.update(period)

        self.sim_motor_turn.iterate(
            radians_per_second_to_rpm(self.sim_wheel_turn.getAngularVelocity()),
            RoboRioSim.getVInVoltage(),
            period,
        )


