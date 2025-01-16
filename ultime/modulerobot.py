import commands2
import wpilib
from wpilib import RobotBase

from ultime.module import ModuleList


class ModuleRobot(commands2.TimedCommandRobot):
    def __init__(self):
        super().__init__()
        self.modules = ModuleList()

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
