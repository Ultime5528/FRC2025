from _weakref import proxy
from typing import List

import commands2
from commands2 import CommandScheduler
from wpilib import RobotController

from commands.diagnostics.claw import DiagnoseClaw
from commands.diagnostics.intake import DiagnoseIntake
from commands.diagnostics.diagnoseall import DiagnoseAll
from modules.hardware import HardwareModule
from ultime.module import Module, ModuleList


class DiagnosticsModule(Module):
    def __init__(self, hardware: HardwareModule, module_list: ModuleList):
        super().__init__()
        self.components_tests: List[commands2.Command] = [
            DiagnoseIntake(hardware.intake),
            DiagnoseClaw(hardware.claw)
        ]

        self._hardware: HardwareModule = proxy(hardware)
        self._module_list = proxy(module_list)
        self._battery_voltage: List[float] = []
        self._is_test = False

        self._run_all_command = DiagnoseAll(self._hardware, self.components_tests)

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

        builder.addBooleanProperty("Ready", lambda: True, noop)
        builder.addStringArrayProperty("Components", getComponentsNames, noop)
        builder.addDoubleArrayProperty("BatteryVoltage", getBatteryVoltage, noop)
