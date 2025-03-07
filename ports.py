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
    drivetrain_motor_turning_br = 6
    drivetrain_motor_driving_br = 5

    drivetrain_motor_turning_bl = 1
    drivetrain_motor_driving_bl = 2

    drivetrain_motor_turning_fl = 3
    drivetrain_motor_driving_fl = 4

    drivetrain_motor_turning_fr = 7
    drivetrain_motor_driving_fr = 8

    elevator_motor = 10
    climber_motor = 9


class PWM(Immutable):
    claw_motor_right = 1
    claw_motor_left = 0
    arm_motor = 3
    printer_motor = 2
    intake_motor_grab = 5
    intake_motor_pivot = 4
    led_strip = 6


class DIO(Immutable):
    printer_encoder_a = 0
    printer_encoder_b = 1
    printer_switch_left = 2
    printer_switch_right = 3

    printer_photocell = 4

    claw_photocell = 5

    elevator_switch = 6

    intake_encoder_a = 7
    intake_encoder_b = 8
    intake_switch_pivot = 10
    intake_switch_grab = 12

    climber_switch = 9


class PDP(Immutable):
    intake_pivot_motor = 13
    intake_grab_motor = 14
    climber_motor = 16
    elevator_motor = 3
    arm_motor = 12
    printer_motor = 15
    claw_motor_left = "?"
    claw_motor_right = "?"
