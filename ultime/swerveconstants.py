import math

from ultime.immutable import Immutable

class Constants:
    class DriveConstants:
        max_speed_per_second = 4.6
        max_angular_speed = 2 * math.pi

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
