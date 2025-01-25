import wpilib
from ntcore import NetworkTableType
from ntcore.util import ntproperty
from wpilib import RobotController

from modules.hardware import HardwareModule
from ultime.module import Module


class DiagnosticsModule(Module):
    def __init__(self, hardware: HardwareModule):
        super().__init__()
        self._hardware = hardware
        self._subsystems = self._hardware.subsystems

        self._nt_subsystem_list = ntproperty("/Diagnostics/SubsystemList", [subsystem.getName() for subsystem in self._subsystems])
        self._battery_voltage = []
        # self._nt_battery_voltage = ntproperty("/Diagnostics/BatteryVoltage", self._battery_voltage, type=NetworkTableType.kFloatArray)

    def robotPeriodic(self) -> None:
        pass
        # self._battery_voltage.append(RobotController.getBatteryVoltage())
        self._battery_voltage = self._battery_voltage[-100:]

    def testPeriodic(self) -> None:
        pass# self._nt_battery_voltage.fset(None, self._battery_voltage)

    def testExit(self) -> None:
        pass# self._nt_battery_voltage.fset(None, [])

    def initSendable(self, builder):
        def noop(_):
            pass

        builder.addFloatArrayProperty("BatteryVoltage", lambda: self._battery_voltage, noop)
