from modules.hardware import HardwareModule
from ultime.module import Module
from wpilib.simulation import RoboRioSim
from wpilib.simulation import BatterySim


class BatterySimModule(Module):
    def __init__(self, hardware: HardwareModule):
        super().__init__()
        self.subsystems = hardware.subsystems

    def simulationPeriodic(self) -> None:
        RoboRioSim.setVInVoltage(BatterySim.calculate())
