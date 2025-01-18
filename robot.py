#!/usr/bin/env python3
import wpilib

from modules.control import ControlModule
from modules.hardware import HardwareModule
from ultime.modulerobot import ModuleRobot


class Robot(ModuleRobot):
    # robotInit fonctionne mieux avec les tests que __init__
    def robotInit(self):
        wpilib.LiveWindow.enableAllTelemetry()
        wpilib.DriverStation.silenceJoystickConnectionWarning(True)
        self.enableLiveWindowInTest(True)

        self.hardware = HardwareModule()
        self.control = ControlModule(self.hardware)

        self.addModules(self.hardware, self.control)
