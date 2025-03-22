import math

from rev import SparkMaxConfig, ClosedLoopConfig, SparkBaseConfig


class SwerveConstants:
    max_speed_per_second = 20
    max_angular_speed = 2 * math.pi

    # 45 teeth on the wheel's bevel gear, 22 teeth on the first-stage spur gear, 15 teeth on the bevel pinion
    drive_motor_pinion_teeth = 13
    drive_motor_gear_ratio = (45.0 * 22) / (drive_motor_pinion_teeth * 15)

    wheel_diameter = 0.0755  # meters
    drive_encoder_position_conversion_factor = (
        math.pi * wheel_diameter / drive_motor_gear_ratio
    )  # meters
    drive_encoder_velocity_conversion_factor = (
        drive_encoder_position_conversion_factor / 60
    )  # meters per second
    drive_motor_free_rps = 5676 / 60  # Neo motor max free RPM into rotations per second
    drive_wheel_free_rps = (
        drive_motor_free_rps * (math.pi * wheel_diameter) / drive_motor_gear_ratio
    )

    turning_encoder_position_conversion_factor = math.pi * 2  # radians
    turning_encoder_velocity_conversion_factor = math.pi * 2 / 60  # radians per second

    turning_encoder_position_PID_min_input = 0
    turning_encoder_position_PID_max_input = turning_encoder_position_conversion_factor


driving_config = SparkMaxConfig()
turning_config = SparkMaxConfig()

# Constants
driving_factor = SwerveConstants.drive_encoder_position_conversion_factor
driving_velocity_factor = SwerveConstants.drive_encoder_velocity_conversion_factor

turning_factor = SwerveConstants.turning_encoder_position_conversion_factor
turning_velocity_factor = SwerveConstants.turning_encoder_velocity_conversion_factor

driving_velocity_feed_forward = 1 / SwerveConstants.drive_wheel_free_rps

# Set up driving config
driving_config.setIdleMode(SparkBaseConfig.IdleMode.kBrake)
driving_config.smartCurrentLimit(50)

driving_config.encoder.positionConversionFactor(driving_factor)
driving_config.encoder.velocityConversionFactor(driving_velocity_factor)

driving_config.closedLoop.setFeedbackSensor(
    ClosedLoopConfig.FeedbackSensor.kPrimaryEncoder
)
driving_config.closedLoop.pid(0.08, 0.0, 0.0)
driving_config.closedLoop.velocityFF(driving_velocity_feed_forward)
driving_config.closedLoop.outputRange(-1, 1)

# Set up turning config
turning_config.setIdleMode(SparkBaseConfig.IdleMode.kBrake)
turning_config.smartCurrentLimit(20)

turning_config.absoluteEncoder.inverted(True)
turning_config.absoluteEncoder.positionConversionFactor(turning_factor)
turning_config.absoluteEncoder.velocityConversionFactor(turning_velocity_factor)

turning_config.closedLoop.setFeedbackSensor(
    ClosedLoopConfig.FeedbackSensor.kAbsoluteEncoder
)
turning_config.closedLoop.pid(0.4, 0.0, 0.0)
turning_config.closedLoop.outputRange(-1, 1)
turning_config.closedLoop.positionWrappingEnabled(True)
turning_config.closedLoop.positionWrappingInputRange(0, turning_factor)
