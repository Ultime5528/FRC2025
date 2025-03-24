from commands2 import SequentialCommandGroup
from commands2.cmd import runOnce, deadline, run
from wpilib import RobotController, PowerDistribution, DataLogManager

import ports
from commands.climber.moveclimber import ReadyClimber, Climb
from commands.climber.resetclimber import ResetClimber
from subsystems.climber import Climber
from ultime.autoproperty import autoproperty
from ultime.command import ignore_requirements, WaitCommand
from ultime.proxy import proxy


@ignore_requirements(["climber"])
class DiagnoseSwitchAndMotor(SequentialCommandGroup):
    voltage_change_threshold = autoproperty(0.5)

    def __init__(self, climber: Climber, pdp: PowerDistribution):
        super().__init__(
            runOnce(proxy(self.before_climb)),
            ReadyClimber(climber),
            deadline(Climb(climber), run(proxy(self.during_climb))),
            WaitCommand(0.1),
            runOnce(proxy(self.after_climb)),
            ResetClimber(climber),
        )
        self.pdp = pdp
        self.climber = climber

    def before_climb(self):
        self.max_value = 0.0

        if self.pdp.getCurrent(ports.PDP.climber_motor) > 0.1:
            DataLogManager.log(
                f"Climber diagnostics: Motor current measured too high. {self.pdp.getCurrent(ports.PDP.climber_motor)}"
            )
            self.climber.alert_motor_hi.set(True)
        if self.climber.isClimbed():
            self.climber.alert_switch.set(True)

    def during_climb(self):
        self.max_value = max(self.max_value, self.pdp.getCurrent(ports.PDP.climber_motor))

    def after_climb(self):
        if self.pdp.getCurrent(ports.PDP.climber_motor) > 0.1:
            DataLogManager.log(
                f"Climber diagnostics: Motor current measured too high. {self.pdp.getCurrent(ports.PDP.climber_motor)}"
            )
            self.climber.alert_motor_hi.set(True)

        if self.max_value < 0.1:
            DataLogManager.log(
                f"Climber diagnostics: Motor current measured too low. {self.pdp.getCurrent(ports.PDP.climber_motor)}"
            )
            self.climber.alert_motor_lo.set(True)

        if not self.climber.isClimbed():
            self.climber.alert_switch.set(True)

