from commands2 import Command
from commands2.sysid import SysIdRoutine
from wpilib import RobotController
from wpilib._wpilib.sysid import SysIdRoutineLog

from subsystems.drivetrain import Drivetrain
from ultime.module import Module


class SystemIdentificationModule(Module):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__()

        self.is_in_safe_position = False

        self.drivetrain = drivetrain

        self.sysid_routine = SysIdRoutine(
            SysIdRoutine.Config(),
            SysIdRoutine.Mechanism(
                self.driveSwervesFromVoltage, self.logSysId, drivetrain
            ),
        )

    def getQuasistaticTest(self, direction: SysIdRoutine.Direction) -> Command:
        return self.sysid_routine.quasistatic(direction)

    def getDynamicTest(self, direction: SysIdRoutine.Direction) -> Command:
        return self.sysid_routine.dynamic(direction)

    def logSysId(self, log: SysIdRoutineLog):
        (
            log.motor("swerve fl")
            .position(self.drivetrain.swerve_module_fl._driving_encoder.getPosition())
            .voltage(
                self.drivetrain.swerve_module_fl._driving_motor.get()
                * RobotController.getBatteryVoltage()
            )
            .velocity(self.drivetrain.swerve_module_fl.getVelocity())
        )
        (
            log.motor("swerve fr")
            .position(self.drivetrain.swerve_module_fr._driving_encoder.getPosition())
            .voltage(
                self.drivetrain.swerve_module_fr._driving_motor.get()
                * RobotController.getBatteryVoltage()
            )
            .velocity(self.drivetrain.swerve_module_fr.getVelocity())
        )

        (
            log.motor("swerve bl")
            .position(self.drivetrain.swerve_module_bl._driving_encoder.getPosition())
            .voltage(
                self.drivetrain.swerve_module_bl._driving_motor.get()
                * RobotController.getBatteryVoltage()
            )
            .velocity(self.drivetrain.swerve_module_bl.getVelocity())
        )
        (
            log.motor("swerve br")
            .position(self.drivetrain.swerve_module_br._driving_encoder.getPosition())
            .voltage(
                self.drivetrain.swerve_module_br._driving_motor.get()
                * RobotController.getBatteryVoltage()
            )
            .velocity(self.drivetrain.swerve_module_br.getVelocity())
        )

    def driveSwervesFromVoltage(self, voltage: float):
        if self.is_in_safe_position:
            self.drivetrain.swerve_module_fl._driving_motor.setVoltage(voltage)
            self.drivetrain.swerve_module_fr._driving_motor.setVoltage(voltage)
            self.drivetrain.swerve_module_bl._driving_motor.setVoltage(voltage)
            self.drivetrain.swerve_module_br._driving_motor.setVoltage(voltage)
