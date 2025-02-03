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


class PWM(Immutable):
    intake_motor_pivot = 0
    intake_motor_grab = 1


class DIO:
    elevator_switch = 0
    intake_encoder = 1
    intake_switch_pivot = 2
    intake_switch_grab = 3


class PDP:
    pass
