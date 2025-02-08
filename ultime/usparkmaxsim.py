from rev import SparkMax
from wpilib.simulation import SimDeviceSim


class USparkMaxSim:
    def __init__(self, spark_max: SparkMax):
        self.sim_device_motor = SimDeviceSim(f"SPARK MAX [{spark_max.getDeviceId()}]")
        self.sim_device_relative_encoder = SimDeviceSim(
            f"SPARK MAX [{spark_max.getDeviceId()}] RELATIVE ENCODER"
        )
        self.sim_device_absolute_encoder = SimDeviceSim(
            f"SPARK MAX [{spark_max.getDeviceId()}] ABSOLUTE ENCODER"
        )

        self._voltage_motor = self.sim_device_motor.getDouble("Applied Output")
        self._position_motor = self.sim_device_motor.getDouble("Position")
        self._velocity_motor = self.sim_device_motor.getDouble("Velocity")

        self._position_relative_encoder = self.sim_device_relative_encoder.getDouble(
            "Position"
        )
        self._velocity_relative_encoder = self.sim_device_relative_encoder.getDouble(
            "Velocity"
        )

        self._position_absolute_encoder = self.sim_device_absolute_encoder.getDouble(
            "Position"
        )
        self._velocity_absolute_encoder = self.sim_device_absolute_encoder.getDouble(
            "Velocity"
        )

    def getPosition(self) -> float:
        return self._position_motor.get()

    def setPosition(self, value: float):
        self._position_motor.set(value)
        self._position_relative_encoder.set(value)
        self._position_absolute_encoder.set(value)

    def getVelocity(self) -> float:
        return self._velocity_motor.get()

    def setVelocity(self, value: float):
        self._velocity_motor.set(value)
        self._velocity_relative_encoder.set(value)
        self._velocity_absolute_encoder.set(value)

    def getVoltage(self) -> float:
        return self._voltage_motor.get()

    def setVoltage(self, value: float):
        self._voltage_motor.set(value)
