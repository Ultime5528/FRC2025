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

    position_conversion_factor = autoproperty(0.184)
    speed = autoproperty(0.5)

    def __init__(self):
        super().__init__()
        self._config = SparkMaxConfig()
        self._config.setIdleMode(SparkBaseConfig.IdleMode.kBrake)
        self._config.smartCurrentLimit(30)
        self._config.inverted(False)
        self._config.encoder.positionConversionFactor(self.position_conversion_factor)

        self._motor = SparkMax(ports.CAN.climber_motor, SparkMax.MotorType.kBrushless)
        self._encoder = self._motor.getEncoder()
        self._switch = Switch(Switch.Type.NormallyClosed, ports.DIO.climber_switch)

        self._motor.configure(
            self._config,
            SparkBase.ResetMode.kResetSafeParameters,
            SparkBase.PersistMode.kPersistParameters,
        )

        self.state = self.State.Initial

        if RobotBase.isSimulation():
            self._sim_motor = SparkMaxSim(self._motor, DCMotor.NEO(1))
            self._sim_encoder = self._sim_motor.getRelativeEncoderSim()

    def simulationPeriodic(self) -> None:
        distance = self._motor.get() * 0.184
        self._sim_encoder.setPosition(self._sim_encoder.getPosition() + distance)

        if self._sim_encoder.getPosition() >= 90:
            self._switch.setSimPressed()
        else:
            self._switch.setSimUnpressed()

    def isInitial(self):
        return self.state == self.State.Initial

    def isClimbed(self):
        return self._switch.isPressed()

    def setSpeed(self, speed: float):
        assert -1.0 <= speed <= 1.0

        if self.isInitial():
            self._motor.set(speed if speed >= 0 else 0)
        elif self.isClimbed():
            self._motor.set(speed if speed <= 0 else 0)
        else:
            self._motor.set(speed)

    def stop(self):
        self._motor.stopMotor()

    def getPosition(self):
        return self._encoder.getPosition()

    def pull(self):
        self.setSpeed(self.speed)

    def release(self):
        self.setSpeed(-self.speed)

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def noop(x):
            pass

        builder.addStringProperty("state", lambda: self.state.name, noop)
        builder.addFloatProperty("motor_input", self._motor.get, noop)
        builder.addFloatProperty("encoder", self._encoder.getPosition, noop)
        builder.addBooleanProperty("climbed", self.isClimbed, noop)
