import math

from rev import SparkMax, SparkBase
from rev import SparkMaxSim
from wpilib import RobotBase
from wpilib.simulation import FlywheelSim, RoboRioSim
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.system.plant import DCMotor, LinearSystemId

from ultime.swerveconfig import Configs


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

        self._driving_closed_loop_controller = (
            self._driving_motor.getClosedLoopController()
        )
        self._turning_closed_loop_controller = (
            self._turning_motor.getClosedLoopController()
        )

        self._driving_motor.configure(
            Configs.MaxServeModule.driving_config,
            SparkBase.ResetMode.kResetSafeParameters,
            SparkBase.PersistMode.kPersistParameters,
        )
        self._turning_motor.configure(
            Configs.MaxServeModule.turning_config,
            SparkBase.ResetMode.kResetSafeParameters,
            SparkBase.PersistMode.kPersistParameters,
        )

        self._chassis_angular_offset = chassis_angular_offset
        self.desired_state.angle = Rotation2d(self._turning_encoder.getPosition())
        self._driving_encoder.setPosition(0)

        if RobotBase.isSimulation():

            # Flywheels allow simulation of a more physically realistic rendering of swerve module properties
            # Magical values for sim pulled from :
            # https://github.com/4201VitruvianBots/2021SwerveSim/blob/main/Swerve2021/src/main/java/frc/robot/subsystems/SwerveModule.java
            turn_motor_gear_ratio = 12.8  # //12 to 1

            self.sim_wheel_turn = FlywheelSim(
                LinearSystemId.identifyVelocitySystemMeters(0.16, 0.0348),
                DCMotor.NEO550(1),
                [0.0],
            )
            self.sim_motor_turn = SparkMaxSim(self._turning_motor, DCMotor.NEO550(1))

            self.sim_wheel_drive = FlywheelSim(
                LinearSystemId.identifyVelocitySystemMeters(3, 1.24),
                DCMotor.NEO(1),
                [0.075],
            )
            self.sim_motor_drive = SparkMaxSim(self._driving_motor, DCMotor.NEO(1))

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
        # module_max_angular_acceleration = 2 * math.pi  # radians per second squared

        # Drive

        self.sim_wheel_drive.setInputVoltage(
            self.sim_motor_drive.getAppliedOutput() * RoboRioSim.getVInVoltage()
        )

        self.sim_wheel_drive.update(period)

        self.sim_motor_drive.iterate(
            radians_per_second_to_rpm(self.sim_wheel_drive.getAngularVelocity()),
            RoboRioSim.getVInVoltage(),
            period,
        )

        # Turn

        self.sim_wheel_turn.setInputVoltage(
            self.sim_motor_turn.getAppliedOutput() * RoboRioSim.getVInVoltage()
        )

        self.sim_wheel_turn.update(period)

        self.sim_motor_turn.iterate(
            radians_per_second_to_rpm(self.sim_wheel_turn.getAngularVelocity()),
            RoboRioSim.getVInVoltage(),
            period,
        )
