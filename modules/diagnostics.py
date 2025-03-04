from _weakref import proxy
from typing import List

import commands2
from commands2 import CommandScheduler
from commands2.cmd import sequence
from wpilib import RobotController

from commands.diagnostics.arm import DiagnoseArm
from commands.diagnostics.claw import DiagnoseClaw
from commands.diagnostics.intake import DiagnoseIntake
from commands.diagnostics.diagnoseall import DiagnoseAll
from commands.diagnostics.utils.setrunningtest import SetRunningTest
from modules.hardware import HardwareModule
from ultime.module import Module, ModuleList


class DiagnosticsModule(Module):
    def __init__(self, hardware: HardwareModule, module_list: ModuleList):
        super().__init__()
        self.components_tests = {
            hardware.intake: DiagnoseIntake(hardware.intake),
            hardware.claw: DiagnoseClaw(hardware.claw),
            hardware.arm: DiagnoseArm(hardware.arm, hardware.elevator),
        }

        self._hardware = proxy(hardware)
        self._module_list = proxy(module_list)
        self._battery_voltage: List[float] = []
        self._is_test = False
        self._run_all_command = DiagnoseAll(
            self._hardware,
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
        for component in self._hardware.subsystems + self._module_list.modules:
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
                subsystem.getName()
                for subsystem in self._hardware.subsystems + self._module_list.modules
            ]

        def getBatteryVoltage() -> List[float]:
            if self._is_test:
                return self._battery_voltage
            else:
                return []

        builder.publishConstBoolean("Ready", True)
        builder.publishConstStringArray("Components", getComponentsNames())
        builder.addDoubleArrayProperty("BatteryVoltage", getBatteryVoltage, noop)
