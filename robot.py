#!/usr/bin/env python3
import commands2
import wpilib
from wpilib import RobotBase

from modules.hardware import HardwareModule
from ultime.module import ModuleList
from ultime.modulerobot import ModuleRobot


class Robot(ModuleRobot):
    # robotInit fonctionne mieux avec les tests que __init__
    def robotInit(self):
        wpilib.LiveWindow.enableAllTelemetry()
        wpilib.DriverStation.silenceJoystickConnectionWarning(True)
        self.enableLiveWindowInTest(True)

        self.hardware = HardwareModule()

        self.modules.addModules(self.hardware)
