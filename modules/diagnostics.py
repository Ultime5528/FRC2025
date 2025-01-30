from _weakref import proxy
from typing import List

import commands2
from commands2 import CommandScheduler
from ntcore.util import ntproperty
from wpilib import RobotController

from modules.hardware import HardwareModule
from ultime.module import Module, ModuleList


class DiagnosticsModule(Module):
    def __init__(self, hardware: HardwareModule, module_list: ModuleList):
        super().__init__()
        self.components_tests: List[commands2.Command] = []

        self._hardware = hardware
        self._module_list = module_list
        self._battery_voltage: List[float] = []
        self._is_test = False

    def robotInit(self) -> None:
        ntproperty("/Diagnostics/Ready", True)

    def robotPeriodic(self) -> None:
        self._battery_voltage.append(RobotController.getBatteryVoltage())
        self._battery_voltage = self._battery_voltage[-100:]

    def testInit(self) -> None:
        CommandScheduler.getInstance().enable()
        for component_test in self.components_tests:
            component_test.schedule()
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

        builder.addStringArrayProperty("Components", getComponentsNames, noop)
        builder.addFloatArrayProperty("BatteryVoltage", getBatteryVoltage, noop)
