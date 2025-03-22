from commands2 import (
    SequentialCommandGroup,
    InstantCommand,
)
from commands2.cmd import race, run
from commands2.sysid import SysIdRoutine

from modules.systemidentification import SystemIdentificationModule
from subsystems.drivetrain import Drivetrain
from ultime.command import WaitCommand


class SystemIdentificationRoutine(SequentialCommandGroup):
    def __init__(
        self, drivetrain: Drivetrain, sysid_module: SystemIdentificationModule
    ):
        super().__init__(
            # Forward Quasistatic test
            race(run(lambda: drivetrain.setForwardFormation()), WaitCommand(1.0)),
            InstantCommand(lambda: sysid_module.setIsInSafePosition(True)),
            sysid_module.getQuasistaticTest(SysIdRoutine.Direction.kForward),
            sysid_module.getQuasistaticTest(SysIdRoutine.Direction.kReverse),
            InstantCommand(lambda: sysid_module.setIsInSafePosition(False)),
            # Forward Dynamic test
            race(run(lambda: drivetrain.setForwardFormation()), WaitCommand(1.0)),
            InstantCommand(lambda: sysid_module.setIsInSafePosition(True)),
            sysid_module.getDynamicTest(SysIdRoutine.Direction.kForward),
            sysid_module.getDynamicTest(SysIdRoutine.Direction.kReverse),
            InstantCommand(lambda: sysid_module.setIsInSafePosition(False)),
        )
