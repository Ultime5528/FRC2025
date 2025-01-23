from wpilib import DataLogManager, DriverStation

DataLogManager.start()
DriverStation.startDataLog(DataLogManager.getLog())