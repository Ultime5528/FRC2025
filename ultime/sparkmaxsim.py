from rev import SparkMax
from wpilib.simulation import SimDeviceSim

class SparkMaxSim:
    def __init__(self, spark_max: SparkMax):
        self.sim_device = SimDeviceSim(f"SPARK MAX [{spark_max.getDeviceId()}")
        self._voltage = self.sim_device.getDouble("Analog Voltage")
        self._position = self.sim_device.getDouble("Position")
        self._velocity = self.sim_device.getDouble("Velocity")

    def getPosition(self):
        return self._position.get()

    def setPosition(self, value: float):
        self._position.set(value)

    def getVelocity(self):
        return  self._velocity.get()

    def setVelocity(self, value: float):
        self._velocity(value)

    def getVoltage(self):
        return self._voltage.get()

    def setVoltage(self, value: float):
        self._voltage.set(value)