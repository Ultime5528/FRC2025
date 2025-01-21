from wpilib.simulation import BatterySim
from wpilib.simulation import RoboRioSim

from modules.hardware import HardwareModule
from ultime.module import Module


class BatterySimModule(Module):
    def __init__(self, hardware: HardwareModule):
        super().__init__()
        self.subsystems = hardware.subsystems

    def simulationPeriodic(self) -> None:
        amps = [subsystem.getCurrentDrawAmps() for subsystem in self.subsystems]
        RoboRioSim.setVInVoltage(BatterySim.calculate(amps))
