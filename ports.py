from ultime.immutable import Immutable

"""
Respect the naming convention : "subsystem" _ "component type" _ "precision"

Put port variables into the right category: CAN - PWM - DIO

Order port numbers, ex:
    shooter_motor = 0
    drivetrain_motor_fr = 1
    drivetrain_motor_rr = 2
"""


class CAN(Immutable):
    drivetrain_motor_turning_br = 1
    drivetrain_motor_driving_br = 2
    drivetrain_motor_turning_bl = 3
    drivetrain_motor_driving_bl = 4
    drivetrain_motor_driving_fl = 5
    drivetrain_motor_turning_fl = 6
    drivetrain_motor_turning_fr = 7
    drivetrain_motor_driving_fr = 8
    elevator_motor = 9
    climber_motor = 10


class PWM(Immutable):
    claw_motor_right = 0
    claw_motor_left = 1
    arm_motor = 2
    printer_motor = 3
    intake_motor_grab = 4
    intake_motor_pivot = 5


class DIO:
    elevator_switch = 0
    printer_switch_right = 1
    printer_switch_left = 2
    printer_encoder_a = 3
    printer_encoder_b = 4
    printer_photocell = 5
    claw_photocell = 6
    climber_switch = 7
    intake_switch_grab = 8
    intake_encoder_a = 9
    intake_encoder_b = 10
    intake_switch_pivot = 11


class PDP:
    pass
