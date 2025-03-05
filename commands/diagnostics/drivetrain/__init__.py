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
                drivetrain.swerve_module_fl, drivetrain.alerts_encoder["FL"], drivetrain.alerts_turning_motor["FL"]
            ),
            DiagnoseSwerveModule(
                drivetrain.swerve_module_fr, drivetrain.alerts_encoder["FR"], drivetrain.alerts_turning_motor["FR"]
            ),
            DiagnoseSwerveModule(
                drivetrain.swerve_module_bl, drivetrain.alerts_encoder["BL"], drivetrain.alerts_turning_motor["BL"]
            ),
            DiagnoseSwerveModule(
                drivetrain.swerve_module_br, drivetrain.alerts_encoder["BR"], drivetrain.alerts_turning_motor["BR"]
            ),
            DiagnoseOdometry(drivetrain),
        )
