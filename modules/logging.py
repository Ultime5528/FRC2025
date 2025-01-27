from wpilib import DataLogManager, DriverStation

from ultime.module import Module


class LoggingModule(Module):
    def __init__(self):
        super().__init__()
        DataLogManager.start()
        DriverStation.startDataLog(DataLogManager.getLog())
