from enum import Enum, auto

from rev import SparkMax, SparkMaxConfig, SparkBaseConfig, SparkBase, SparkMaxSim
from wpilib import RobotBase
from wpimath._controls._controls.plant import DCMotor
from wpiutil import SendableBuilder

import ports
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem
from ultime.switch import Switch
from ultime.timethis import tt


class Climber(Subsystem):
    class State(Enum):
        Unknown = auto()
        Moving = auto()
        Initial = auto()
        Ready = auto()
        Climbed = auto()

    height_max = autoproperty(90.0)
    position_conversion_factor = autoproperty(0.205)
    speed = autoproperty(1.0)

    def __init__(self):
        super().__init__()
        self._config = SparkMaxConfig()
        self._config.setIdleMode(SparkBaseConfig.IdleMode.kBrake)
        self._config.smartCurrentLimit(40)
        self._config.inverted(True)

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
            self._offset = (
                self.height_max / self.position_conversion_factor
                - self.getRawEncoderPosition()
            )
            self._has_reset = True
        self._prev_is_down = self._switch.isPressed()

    def simulationPeriodic(self) -> None:
        distance = self._motor.get()
        self._sim_encoder.setPosition(
            self._sim_encoder.getPosition() + distance / self.position_conversion_factor
        )

        if self.getPosition() >= 90:
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
        return self.position_conversion_factor * (
            self.getRawEncoderPosition() + self._offset
        )

    def getRawEncoderPosition(self):
        return self._encoder.getPosition()

    def pull(self):
        self.setSpeed(self.speed)

    def release(self):
        self.setSpeed(-self.speed)

    def getMotorInput(self):
        return self._motor.get()

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def setOffset(value: float):
            self._offset = value

        def setHasReset(value: bool):
            self._has_reset = value

        def noop(x):
            pass

        builder.addStringProperty("state", tt(lambda: self.state.name), noop)
        builder.addFloatProperty("motor_input", tt(self.getMotorInput), noop)
        builder.addFloatProperty("encoder", tt(self.getRawEncoderPosition), noop)
        builder.addFloatProperty("position", tt(self.getPosition), noop)
        builder.addFloatProperty(
            "offset", tt(lambda: self._offset), lambda x: setOffset(x)
        )
        builder.addBooleanProperty("isClimbed", tt(self.isClimbed), noop)
        builder.addBooleanProperty(
            "has_reset", tt(lambda: self._has_reset), setHasReset
        )
