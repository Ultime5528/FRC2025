from enum import Enum, auto

from rev import SparkMax, SparkMaxConfig, SparkBaseConfig, SparkBase, SparkMaxSim
from wpilib import RobotBase, RobotController
from wpilib.simulation import FlywheelSim, ElevatorSim, RoboRioSim
from wpimath._controls._controls.plant import LinearSystemId, DCMotor

import ports
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem
from ultime.switch import Switch


class Elevator(Subsystem):
    class State(Enum):
        Invalid = auto()
        Moving = auto()
        Level1 = auto()
        Level2 = auto()
        Level3 = auto()
        Level4 = auto()

    speed_up = autoproperty(1.0)
    speed_down = autoproperty(-1.0)
    speed_maintain = autoproperty(-0.25)
    height_min = autoproperty(0.0)
    height_max = autoproperty(10.0)

    def __init__(self):
        super().__init__()
        self._config = SparkMaxConfig()
        self._config.setIdleMode(SparkBaseConfig.IdleMode.kBrake)
        self._config.smartCurrentLimit(30)
        self._config.inverted(False)
        self._config.encoder.positionConversionFactor(1)

        self._switch = Switch(Switch.Type.NormallyClosed, ports.DIO.elevator_switch)
        self._motor = SparkMax(ports.CAN.elevator_motor, SparkMax.MotorType.kBrushless)
        self._encoder = self._motor.getEncoder()

        self._motor.configure(
            self._config,
            SparkBase.ResetMode.kResetSafeParameters,
            SparkBase.PersistMode.kPersistParameters,
        )

        self._offset = 0.0
        self._has_reset = False
        self._prev_is_down = False
        self.state = Elevator.State.Invalid

        if RobotBase.isSimulation():
            self._elevator_sim = ElevatorSim(
                DCMotor.NEO(1), 10.0, 4.0, 0.05, -100, 100, True, 0, [0.01, 0.0]
            )
            self.sim_motor = SparkMaxSim(self._motor, DCMotor.NEO(1))

    def periodic(self) -> None:
        if self._prev_is_down and not self._switch.isPressed():
            self._offset = self.height_min - self._encoder.getDistance()
            self._has_reset = True
        self._prev_is_down = self._switch.isPressed()

    def simulationPeriodic(self) -> None:
        assert not (
            self.isUp() and self.isDown()
        ), "Both switches are on at the same time which doesn't make any sense"

        self._elevator_sim.setInputVoltage(
            self.sim_motor.getAppliedOutput() * RobotController.getBatteryVoltage()
        )
        self._elevator_sim.update(0.02)

        self.sim_motor.iterate(
            500 * self._elevator_sim.getVelocity(),
            RoboRioSim.getVInVoltage(),
            0.02,
        )

        if self.getHeight() < self.height_min:
            self._switch.setSimPressed()
        else:
            self._switch.setSimUnpressed()

    def moveUp(self):
        self.setSpeed(self.speed_up)

    def moveDown(self):
        self.setSpeed(self.speed_down)

    def setSpeed(self, speed: float):
        assert -1.0 <= speed <= 1.0

        if self.isDown():
            self._motor.set(speed if speed >= 0 else 0)
        elif self.isUp():
            self._motor.set(speed if speed <= 0 else 0)
        else:
            self._motor.set(speed)

    def maintain(self):
        self.setSpeed(self.speed_maintain)

    def isDown(self) -> bool:
        return self._switch.isPressed()

    def isUp(self) -> bool:
        return self._has_reset and self.getHeight() > self.height_max

    def stop(self):
        self._motor.stopMotor()

    def setHeight(self, reset_value):
        self._offset = reset_value - self._encoder.getPosition()

    def getHeight(self):
        return self._encoder.getPosition() + self._offset

    def getMotorInput(self):
        return self._motor.get()

    def hasReset(self):
        return self._has_reset
