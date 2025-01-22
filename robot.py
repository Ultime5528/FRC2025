#!/usr/bin/env python3
import wpilib

from modules.autonomous import AutonomousModule
from modules.batterysim import BatterySimModule
from modules.control import ControlModule
from modules.dashboard import DashboardModule
from modules.hardware import HardwareModule
from modules.propertysavechecker import PropertySaveCheckerModule
from ultime.modulerobot import ModuleRobot


class Robot(ModuleRobot):
    # robotInit fonctionne mieux avec les tests que __init__
    def robotInit(self):
        wpilib.LiveWindow.enableAllTelemetry()
        wpilib.DriverStation.silenceJoystickConnectionWarning(True)
        self.enableLiveWindowInTest(True)

        self.hardware = HardwareModule()
        self.autonomous = AutonomousModule()
        self.control = ControlModule(self.hardware)
        self.property_save_checker = PropertySaveCheckerModule()
        self.dashboard = DashboardModule(self.hardware)
        self.battery_sim = BatterySimModule(self.hardware)

        self.addModules(
            self.hardware,
            self.autonomous,
            self.control,
            self.property_save_checker,
            self.battery_sim,
            self.dashboard,
        )
