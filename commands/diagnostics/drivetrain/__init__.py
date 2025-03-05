from commands2 import SequentialCommandGroup

from commands.diagnostics.drivetrain.odometry import DiagnoseOdometry
from commands.diagnostics.drivetrain.swerve import DiagnoseSwerveModule
from subsystems.drivetrain import Drivetrain
from ultime.command import ignore_requirements


@ignore_requirements(["drivetrain"])
class DiagnoseDrivetrain(SequentialCommandGroup):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__(
            DiagnoseSwerveModule(
                drivetrain.swerve_module_fl, drivetrain.alert_fl_encoder
            ),
            DiagnoseSwerveModule(
                drivetrain.swerve_module_fr, drivetrain.alert_fr_encoder
            ),
            DiagnoseSwerveModule(
                drivetrain.swerve_module_bl, drivetrain.alert_bl_encoder
            ),
            DiagnoseSwerveModule(
                drivetrain.swerve_module_br, drivetrain.alert_br_encoder
            ),
            DiagnoseOdometry(drivetrain),
        )
