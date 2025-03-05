from commands2 import SequentialCommandGroup
from commands2.cmd import runOnce, run, waitSeconds, deadline
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModuleState

from ultime.alert import Alert
from ultime.autoproperty import autoproperty
from ultime.proxy import proxy
from ultime.swerve import SwerveModule


class DiagnoseSwerveModule(SequentialCommandGroup):
    min_velocity = autoproperty(0.5)
    angle_tolerance = autoproperty(0.8)
    target_angle = autoproperty(-45)

    def __init__(
        self, swerve: SwerveModule, alert_encoders: Alert, alert_turning_motor: Alert
    ):
        super().__init__(
            deadline(  # for driving motor
                waitSeconds(1.0),
                run(proxy(self.test_encoder)),
            ),
            runOnce(proxy(self.after_encoder_test)),
            deadline(  # for driving motor
                waitSeconds(1.0),
                run(lambda: self.swerve.setDesiredState(self.swerve_module_state_test)),
            ),
            runOnce(proxy(self.after_turning_motor_test)),
        )
        self.swerve_module_state_test = SwerveModuleState(
            0, Rotation2d.fromDegrees(self.target_angle)
        )
        self.swerve = proxy(swerve)
        self.max_velocity = 0
        self.alert_encoders = alert_encoders
        self.alert_turning_motor = alert_turning_motor

    def test_encoder(self):
        self.swerve._driving_motor.set(0.2)
        self.max_velocity = max(self.swerve.getVelocity(), self.max_velocity)

    def after_encoder_test(self):
        self.swerve._driving_motor.set(0.0)
        if self.max_velocity < self.min_velocity:
            self.alert_encoders.set(True)

    def after_turning_motor_test(self):
        angle = self.swerve.getPosition().angle.degrees()
        self.alert_turning_motor.set(True)
        # TODO: add angle check
