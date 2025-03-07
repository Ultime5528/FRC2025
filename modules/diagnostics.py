from typing import List

from commands2 import CommandScheduler
from commands2.cmd import sequence
from wpilib import RobotController

from commands.diagnostics.arm import DiagnoseArm
from commands.diagnostics.claw import DiagnoseClaw
from commands.diagnostics.climber import DiagnoseClimber
from commands.diagnostics.diagnoseall import DiagnoseAll
from commands.diagnostics.elevator import DiagnoseElevator
from commands.diagnostics.drivetrain import DiagnoseDrivetrain
from commands.diagnostics.intake import DiagnoseIntake
from commands.diagnostics.printer import DiagnosePrinter
from commands.diagnostics.utils.setrunningtest import SetRunningTest
from modules.hardware import HardwareModule
from ultime.module import Module, ModuleList
from ultime.timethis import tt


class DiagnosticsModule(Module):
    def __init__(self, hardware: HardwareModule, module_list: ModuleList):
        super().__init__()
        self.components = hardware.subsystems + module_list.modules

        self.components_tests = {
            hardware.drivetrain: DiagnoseDrivetrain(hardware.drivetrain),
            hardware.elevator: DiagnoseElevator(hardware.elevator, hardware.pdp),
            hardware.intake: DiagnoseIntake(hardware.intake, hardware.pdp),
            hardware.claw: DiagnoseClaw(hardware.claw, hardware.pdp),
            hardware.arm: DiagnoseArm(hardware.arm, hardware.elevator, hardware.pdp),
            hardware.printer: DiagnosePrinter(hardware.printer, hardware.pdp),
            hardware.climber: DiagnoseClimber(hardware.climber, hardware.pdp),
        }

        self._battery_voltage: List[float] = []
        self._is_test = False
        self._run_all_command = DiagnoseAll(
            hardware,
            [
                sequence(
                    SetRunningTest(component, True),
                    test,
                    SetRunningTest(component, False),
                )
                for component, test in self.components_tests.items()
            ],
        )

    def robotPeriodic(self) -> None:
        self._battery_voltage.append(RobotController.getBatteryVoltage())
        self._battery_voltage = self._battery_voltage[-100:]

    def testInit(self) -> None:
        CommandScheduler.getInstance().enable()
        for component in self.components:
            component.clearAlerts()
        self._run_all_command.schedule()
        self._is_test = True

    def testExit(self) -> None:
        CommandScheduler.getInstance().disable()
        self._is_test = False

    def initSendable(self, builder):
        def noop(_):
            pass

        def getComponentsNames() -> List[str]:
            return [
                component.getName()
                for component in self.components
                if len(component.registered_alerts) > 1
            ]

        def getBatteryVoltage() -> List[float]:
            if self._is_test:
                return self._battery_voltage
            else:
                return []

        builder.publishConstBoolean("Ready", True)
        builder.publishConstInteger("ComponentCount", len(self.components))
        builder.publishConstStringArray("Components", getComponentsNames())
        builder.addDoubleArrayProperty("BatteryVoltage", tt(getBatteryVoltage), noop)
