from commands2 import SequentialCommandGroup
from commands2.cmd import runOnce, deadline, run
from wpilib import DataLogManager, PowerDistribution

import ports
from commands.intake.moveintake import MoveIntake
from commands.intake.resetintake import ResetIntake
from subsystems.intake import Intake
from ultime.command import ignore_requirements
from ultime.proxy import proxy


@ignore_requirements(["intake"])
class DiagnoseExtend(SequentialCommandGroup):
    def __init__(self, intake: Intake, pdp: PowerDistribution):
        super().__init__(
            runOnce(proxy(self.before_command)),
            ResetIntake(intake),
            deadline(MoveIntake.toExtended(intake), run(proxy(self.while_move))),
            runOnce(proxy(self.after_extend)),
        )

        self.intake = intake
        self.pdp = pdp

    def before_command(self):
        self.max_value = 0.0
        if self.pdp.getCurrent(ports.PDP.intake_pivot_motor) > 0.1:
            DataLogManager.log(
                f"Intake diagnostics: Pivot motor current measured too high. {self.pdp.getCurrent(ports.PDP.intake_pivot_motor)}"
            )
            self.intake.alert_pivot_motor_hi.set(True)

    def after_extend(self):
        if self.intake.isRetracted() or self.intake.state != Intake.State.Extended:
            self.intake.alert_extend_failed.set(True)

            if self.intake.isRetracted() and self.intake.state == Intake.State.Extended:
                self.intake.alert_is_retracted_failed.set(True)

        if self.max_value < 0.1:
            DataLogManager.log(
                f"Intake diagnostics: Pivot motor current measured too low. {self.max_value}"
            )
            self.intake.alert_pivot_motor_lo.set(True)

        if self.pdp.getCurrent(ports.PDP.intake_pivot_motor) > 0.1:
            DataLogManager.log(
                f"Intake diagnostics: Pivot motor current measured too high. {self.max_value}"
            )
            self.intake.alert_pivot_motor_hi.set(True)

    def while_move(self):
        self.max_value = max(self.max_value, self.pdp.getCurrent(ports.PDP.intake_pivot_motor))
