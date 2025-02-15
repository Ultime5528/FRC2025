from enum import Enum, auto

from rev import SparkMax, SparkMaxConfig, SparkBaseConfig, SparkBase, SparkMaxSim
from wpilib import RobotBase
from wpimath._controls._controls.plant import DCMotor
from wpiutil import SendableBuilder

import ports
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem
from ultime.switch import Switch


class Climber(Subsystem):
    class State(Enum):
        Unknown = auto()
        Moving = auto()
        Initial = auto()
        Ready = auto()
        Climbed = auto()

    height_max = autoproperty(90.0)
    position_conversion_factor = autoproperty(0.180)
    speed = autoproperty(1)

    def __init__(self):
        super().__init__()
        self._config = SparkMaxConfig()
        self._config.setIdleMode(SparkBaseConfig.IdleMode.kBrake)
        self._config.smartCurrentLimit(30)
        self._config.inverted(False)

        self._motor = SparkMax(ports.CAN.climber_motor, SparkMax.MotorType.kBrushless)
        self._encoder = self._motor.getEncoder()
        self._switch = Switch(Switch.Type.NormallyClosed, ports.DIO.climber_switch)

        self._motor.configure(
            self._config,
            SparkBase.ResetMode.kResetSafeParameters,
            SparkBase.PersistMode.kPersistParameters,
        )

        self.state = self.State.Unknown
        self._prev_is_down = False
        self._has_reset = False
        self._offset = 0.0

        if RobotBase.isSimulation():
            self._sim_height = 5.0
            self._sim_motor = SparkMaxSim(self._motor, DCMotor.NEO(1))
            self._sim_encoder = self._sim_motor.getRelativeEncoderSim()

    def periodic(self) -> None:
        if self._prev_is_down and not self._switch.isPressed():
            self._offset = self.height_max - self.getPosition()
            self._has_reset = True
        self._prev_is_down = self._switch.isPressed()


    def simulationPeriodic(self) -> None:
        distance = self._motor.get()
        self._sim_height += distance
        self._sim_encoder.setPosition(self._sim_encoder.getPosition() + distance)

        if self.position_conversion_factor * self._sim_height >= self.height_max:
            self._switch.setSimPressed()
        else:
            self._switch.setSimUnpressed()

    def isClimbed(self):
        return self._switch.isPressed()

    def setSpeed(self, speed: float):
        if self.getPosition() <= 0.0:
            self._motor.set(speed if speed >= 0 else 0)
        elif self.isClimbed():
            self._motor.set(speed if speed <= 0 else 0)
        else:
            self._motor.set(speed)

    def stop(self):
        self._motor.stopMotor()

    def getPosition(self):
        return self.position_conversion_factor * (self._encoder.getPosition() + self._offset)

    def pull(self):
        self.setSpeed(self.speed)

    def release(self):
        self.setSpeed(-self.speed)

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)
        def setOffset(value: float):
            self._offset = value

        def setHasReset(value: bool):
            self._has_reset = value

        def noop(x):
            pass

        builder.addStringProperty("state", lambda: self.state.name, noop)
        builder.addFloatProperty("motor_input", self._motor.get, noop)
        builder.addFloatProperty("encoder", self._encoder.getPosition, noop)
        builder.addFloatProperty("position", self.getPosition, noop)
        builder.addFloatProperty("offset", lambda: self._offset, lambda x: setOffset(x))
        builder.addBooleanProperty("isClimbed", self.isClimbed, noop)
        builder.addBooleanProperty("has_reset", lambda: self._has_reset, setHasReset)
