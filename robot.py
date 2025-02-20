#!/usr/bin/env python3
import wpilib

from modules.armcollision import ArmCollision
from modules.autonomous import AutonomousModule
from modules.batterysim import BatterySimModule
from modules.control import ControlModule
from modules.dashboard import DashboardModule
from modules.diagnostics import DiagnosticsModule
from modules.hardware import HardwareModule
from modules.logging import LoggingModule
from modules.propertysavechecker import PropertySaveCheckerModule
from modules.vision import VisionModule
from ultime.modulerobot import ModuleRobot


class Robot(ModuleRobot):
    # robotInit fonctionne mieux avec les tests que __init__
    def __init__(self):
        super().__init__()

        wpilib.LiveWindow.enableAllTelemetry()
        wpilib.DriverStation.silenceJoystickConnectionWarning(True)
        self.enableLiveWindowInTest(True)

        self.hardware = HardwareModule()
        self.control = ControlModule(self.hardware)
        self.autonomous = AutonomousModule(self.hardware)
        self.dashboard = DashboardModule(self.hardware, self.modules)
        self.diagnostics = DiagnosticsModule(self.hardware, self.modules)
        self.logging = LoggingModule()
        self.property_save_checker = PropertySaveCheckerModule()
        self.battery_sim = BatterySimModule(self.hardware)
        self.arm_collision = ArmCollision(self.hardware)
        self.vision = VisionModule()

        self.addModules(
            self.hardware,
            self.control,
            self.autonomous,
            self.dashboard,
            self.diagnostics,
            self.logging,
            self.property_save_checker,
            self.vision,
            self.arm_collision,
            # self.battery_sim,  # Current becomes so low, robot stops working
        )
