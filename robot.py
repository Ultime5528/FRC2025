#!/usr/bin/env python3
import commands2
import wpilib
from wpilib import RobotBase

from modules.control import ControlModule
from modules.hardware import HardwareModule
from modules.propertysavechecker import PropertySaveCheckerModule
from ultime.module import ModuleList


class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        # robotInit fonctionne mieux avec les tests que __init__.
        wpilib.LiveWindow.enableAllTelemetry()
        wpilib.DriverStation.silenceJoystickConnectionWarning(True)
        self.enableLiveWindowInTest(True)

        self.hardware = HardwareModule()

        self.propertysavechecker = PropertySaveCheckerModule()
        self.control = ControlModule(self.hardware)

        self.modules = ModuleList(
            self.hardware,
            self.propertysavechecker,
            self.control,
        )

        self.modules.robotInit()

        if RobotBase.isSimulation():
            self.modules.simulationInit()

    def robotPeriodic(self):
        self.modules.robotPeriodic()

        if RobotBase.isSimulation():
            self.modules.simulationPeriodic()

    def disabledInit(self):
        self.modules.disabledInit()

    def disabledPeriodic(self):
        self.modules.disabledPeriodic()

    def disabledExit(self):
        self.modules.disabledExit()

    def autonomousInit(self):
        self.modules.autonomousInit()

    def autonomousPeriodic(self):
        self.modules.autonomousPeriodic()

    def autonomousExit(self):
        self.modules.autonomousExit()

    def teleopInit(self):
        self.modules.teleopInit()

    def teleopPeriodic(self):
        self.modules.teleopPeriodic()

    def teleopExit(self):
        self.modules.teleopExit()

    def testInit(self):
        self.modules.testInit()

    def testPeriodic(self):
        self.modules.testPeriodic()

    def testExit(self):
        self.modules.testExit()

    def driverStationConnected(self):
        self.modules.driverStationConnected()
