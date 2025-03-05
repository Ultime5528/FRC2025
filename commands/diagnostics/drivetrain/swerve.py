import wpilib
from commands2 import SequentialCommandGroup, FunctionalCommand
from commands2.cmd import runOnce, parallel

from ultime.alert import Alert
from ultime.autoproperty import autoproperty
from ultime.proxy import proxy
from ultime.swerve import SwerveModule


class DiagnoseSwerveModule(SequentialCommandGroup):
    min_velocity = autoproperty(0.5)

    def __init__(self, swerve: SwerveModule, alert_encoders: Alert = None):
        super().__init__(
            runOnce(proxy(self.before_test)),
            parallel(
                FunctionalCommand(
                    lambda: None,
                    lambda: self.swerve._driving_motor.set(0.2),
                    lambda b: None,
                    lambda: self.timer.get() > 1,
                ),
                FunctionalCommand(
                    lambda: None,
                    proxy(self.test_encoder),
                    lambda b: None,
                    lambda: self.timer.get() > 1,
                ),
            ),
            runOnce(proxy(self.after_encoder_test)),
        )
        self.timer = wpilib.Timer()
        self.swerve = proxy(swerve)
        self.max_velocity = 0
        self.alert_encoders = alert_encoders

    def before_test(self):
        self.timer.reset()
        self.timer.start()

    def test_encoder(self):
        if self.timer.get() > 0.1:
            self.max_velocity = max(self.swerve.getVelocity(), self.max_velocity)

    def after_encoder_test(self):
        if self.max_velocity < self.min_velocity:
            self.alert_encoders.set(True)
