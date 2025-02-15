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
    drivetrain_motor_turning_br = 7
    drivetrain_motor_driving_br = 8

    drivetrain_motor_turning_bl = 6
    drivetrain_motor_driving_bl = 5

    drivetrain_motor_turning_fl = 1
    drivetrain_motor_driving_fl = 2

    drivetrain_motor_turning_fr = 4
    drivetrain_motor_driving_fr = 3

    elevator_motor = 10
    climber_motor = 9


class PWM(Immutable):
    claw_motor_right = 1
    claw_motor_left = 0
    arm_motor = 3
    printer_motor = 2
    intake_motor_grab = 5
    intake_motor_pivot = 4


class DIO:
    elevator_switch = 6

    printer_switch_right = 3
    printer_switch_left = 2
    printer_encoder_a = 0
    printer_encoder_b = 1

    printer_photocell = 4
    claw_photocell = 5

    climber_switch = 9

    intake_switch_grab = 10
    intake_encoder_a = 7
    intake_encoder_b = 8


class PDP:
    pass
