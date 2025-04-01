import math
from typing import Callable

from rev import SparkMax, SparkBase, SparkSim, ClosedLoopSlot, SparkClosedLoopController
from wpilib import RobotBase
from wpilib.simulation import RoboRioSim
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from wpimath.system.plant import DCMotor
from wpiutil import Sendable, SendableBuilder

from ultime import swerveconfig
from ultime.swerveconfig import SwerveConstants
from ultime.timethis import tt


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
        self._driving_encoder.setPosition(0.0)

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

    def setDriveVoltage(self, voltage: float):
        self._driving_motor.setVoltage(voltage)

    def setTurnVoltage(self, voltage: float):
        self._turning_motor.setVoltage(voltage)

    def setDriveVelocity(self, velocity_deg_per_sec: float):
        ff_volts = (
            SwerveConstants.driveKs
            + (velocity_deg_per_sec / abs(velocity_deg_per_sec))
            + SwerveConstants.driveKv * velocity_deg_per_sec
        )
        self._driving_closed_loop_controller.setReference(
            velocity_deg_per_sec,
            SparkBase.ControlType.kVelocity,
            ClosedLoopSlot.kSlot0,
            ff_volts,
            SparkClosedLoopController.ArbFFUnits.kVoltage,
        )

    def setTurnPosition(self, rotation: Rotation2d):
        modulus = SwerveConstants.turning_encoder_position_conversion_factor
        rotation = rotation.radians()
        setpoint = (rotation - self._chassis_angular_offset) % modulus
        self._turning_closed_loop_controller.setReference(
            setpoint, SparkBase.ControlType.kPosition
        )

    def runSetpoint(self, state: SwerveModuleState):
        current_rotation = Rotation2d(self._turning_encoder.getPosition())

        state.optimize(current_rotation)
        state.cosineScale(state.angle)

        self.setDriveVelocity(state.speed / (SwerveConstants.wheel_diameter / 2))
        self.setTurnPosition(state.angle)

    def runCharacterization(self, output: float):
        self.setDriveVoltage(output)
        self.setTurnPosition(Rotation2d())

    def stop(self):
        self.setDriveVoltage(0.0)
        self.setTurnVoltage(0.0)

    def getAngleRandians(self) -> Rotation2d:
        return Rotation2d(self._turning_encoder.getPosition())

    def getPositionMeters(self):
        return self._driving_encoder.getPosition() * (
            SwerveConstants.wheel_diameter / 2
        )

    def getVelocityMetersPerSec(self):
        return self._driving_encoder.getVelocity() * (
            SwerveConstants.wheel_diameter / 2
        )

    def getPosition(self) -> SwerveModulePosition:
        return SwerveModulePosition(self.getPositionMeters(), self.getAngleRandians())

    def getState(self) -> SwerveModuleState:
        return SwerveModuleState(
            self.getVelocityMetersPerSec(), self.getAngleRandians()
        )

    def getWheelRadiusCharacterizationPosition(self):
        return self._driving_encoder.getPosition()

    def getFFCharacterizationVelocity(self):
        return self._driving_encoder.getVelocity()

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

        builder.addDoubleProperty(
            "Front Left Angle",
            tt(lambda: self.module_fl.getPosition().angle.radians()),
            noop,
        )
        builder.addDoubleProperty(
            "Front Left Velocity", tt(self.module_fl.getFFCharacterizationVelocity), noop
        )

        builder.addDoubleProperty(
            "Front Right Angle",
            tt(lambda: self.module_fr.getPosition().angle.radians()),
            noop,
        )
        builder.addDoubleProperty(
            "Front Right Velocity", tt(self.module_fr.getFFCharacterizationVelocity), noop
        )

        builder.addDoubleProperty(
            "Back Left Angle",
            tt(lambda: self.module_bl.getPosition().angle.radians()),
            noop,
        )
        builder.addDoubleProperty(
            "Back Left Velocity", tt(self.module_bl.getFFCharacterizationVelocity), noop
        )

        builder.addDoubleProperty(
            "Back Right Angle",
            tt(lambda: self.module_br.getPosition().angle.radians()),
            noop,
        )
        builder.addDoubleProperty(
            "Back Right Velocity", tt(self.module_br.getFFCharacterizationVelocity), noop
        )

        builder.addDoubleProperty("Robot Angle", tt(self.get_robot_angle_radians), noop)
