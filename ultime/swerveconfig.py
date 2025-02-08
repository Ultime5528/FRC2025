from rev import SparkMaxConfig, ClosedLoopConfig, SparkBaseConfig

from ultime.swerveconstants import Constants


class Configs:
    class MaxServeModule:
        constants = Constants.DriveConstants

        driving_config = SparkMaxConfig()
        turning_config = SparkMaxConfig()

        # Constants
        driving_factor = constants.drive_encoder_position_conversion_factor
        driving_velocity_factor = constants.drive_encoder_velocity_conversion_factor

        turning_factor = constants.turning_encoder_position_conversion_factor
        turning_velocity_factor = constants.turning_encoder_velocity_conversion_factor

        driving_velocity_feed_forward = 1 / constants.drive_motor_free_rps

        # Set up driving config
        driving_config.setIdleMode(SparkBaseConfig.IdleMode.kBrake)
        driving_config.smartCurrentLimit(50)

        driving_config.encoder.positionConversionFactor(driving_factor)
        driving_config.encoder.velocityConversionFactor(driving_velocity_factor)

        driving_config.closedLoop.setFeedbackSensor(
            ClosedLoopConfig.FeedbackSensor.kPrimaryEncoder
        )
        driving_config.closedLoop.pid(0.04, 0.0, 0.0)#0.04
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
