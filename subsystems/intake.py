from wpilib import VictorSP, Encoder

import ports
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem
from ultime.switch import Switch


class Intake(Subsystem):
    pivot_speed = autoproperty(0.5)
    grab_speed = autoproperty(0.3)

    def __init__(self):
        super().__init__()

        self.pivot_motor = VictorSP(ports.PWM.intake_motor_pivot)
        self.pivot_encoder = Encoder(ports.DIO.intake_encoder)

        self.grab_motor = VictorSP(ports.PWM.intake_motor_grab)

        self.switch = Switch(
            switch_type=Switch.Type.NormallyOpen,
            port=ports.DIO.intake_switch,
        )

    def retractPivot(self):
        if not self.switch.isPressed():
            self.pivot_motor.set(self.pivot_speed)

    def extendPivot(self):
        self.pivot_motor.set(-1 * self.pivot_speed)

    def grab(self):
        self.grab_motor.set(self.grab_speed)

    def drop(self):
        self.grab_motor.set(-1 * self.grab_speed)

    def getCurrentDrawAmps(self) -> float:
        pass
