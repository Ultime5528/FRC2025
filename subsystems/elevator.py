from enum import Enum, auto

from rev import SparkMax, SparkMaxConfig, SparkBaseConfig, SparkBase, SparkMaxSim
from wpilib import RobotBase
from wpimath._controls._controls.plant import DCMotor
from wpiutil import SendableBuilder

import ports
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem
from ultime.switch import Switch


class Elevator(Subsystem):
    class State(Enum):
        Unknown = auto()
        Moving = auto()
        Loading = auto()
        Reset = auto()
        Level1 = auto()
        Level2 = auto()
        Level3 = auto()
        Level4 = auto()
        Level2Algae = auto()
        Level3Algae = auto()

    class MovementState(Enum):
        AvoidLowerZone = auto()
        FreeToMove = auto()
        Unknown = auto()

    speed_up = autoproperty(0.1)
    speed_down = autoproperty(-0.1)
    speed_maintain = autoproperty(0.02)
    height_min = autoproperty(0.0)
    height_max = autoproperty(1.37)
    height_maintain = autoproperty(0.0)
    height_lower_zone = autoproperty(0.12)

    position_conversion_factor = autoproperty(0.00623)

    def __init__(self):
        super().__init__()
        self._config = SparkMaxConfig()
        self._config.setIdleMode(SparkBaseConfig.IdleMode.kBrake)
        self._config.smartCurrentLimit(30)
        self._config.inverted(False)

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
        self.state = Elevator.State.Unknown
        self.movement_state = Elevator.MovementState.Unknown

        self.alert_retracts_while_arm = self.createAlert(
            "Elevator had a downwards motion in LowerZone while Arm was extended"
        )

        if RobotBase.isSimulation():
            self._sim_motor = SparkMaxSim(self._motor, DCMotor.NEO(1))
            self._sim_encoder = self._sim_motor.getRelativeEncoderSim()
            self._sim_height = 0.1

    def periodic(self) -> None:
        if self._prev_is_down and not self._switch.isPressed():
            self._offset = self.height_min - self._encoder.getPosition()
            self._has_reset = True
        self._prev_is_down = self._switch.isPressed()

        if (
            self.movement_state == self.MovementState.AvoidLowerZone
            and self.isInLowerZone()
            and self._motor.get() > 0
        ):
            self.alert_retracts_while_arm.set(True)

    def simulationPeriodic(self) -> None:
        # On applique la gravité si l'élévateur est plus haut que 0
        if self._sim_height > 0.0:
            gravity = self.speed_maintain
        else:
            gravity = 0.0

        distance = (self._motor.get() - gravity) * 0.051

        self._sim_height += distance
        self._sim_encoder.setPosition(
            self._sim_encoder.getPosition() + distance / self.position_conversion_factor
        )

        if self._sim_height <= self.height_min:
            self._switch.setSimPressed()
        else:
            self._switch.setSimUnpressed()

        assert not (
            self.isUp() and self.isDown()
        ), "Both switches are on at the same time which doesn't make any sense"

    def moveUp(self):
        self.setSpeed(self.speed_up)

    def moveDown(self):
        self.setSpeed(self.speed_down)

    def setSpeed(self, speed: float):
        if (
            self.movement_state == Elevator.MovementState.AvoidLowerZone
            and self.isInLowerZone()
            and speed < 0
        ):
            speed = self.speed_maintain
        elif self.isDown():
            speed = speed if speed >= 0.0 else 0.0
        elif self.isUp():
            speed = speed if speed <= 0.0 else self.speed_maintain

        self._motor.set(speed)

    def maintain(self):
        self.setSpeed(self.speed_maintain)

    def isDown(self) -> bool:
        return self._switch.isPressed()

    def isUp(self) -> bool:
        return self._has_reset and self.getHeight() >= self.height_max

    def stop(self):
        self._motor.stopMotor()

    def setHeight(self, reset_value):
        self._offset = reset_value - self._encoder.getPosition()

    def getHeight(self):
        return self.position_conversion_factor * (
            self._encoder.getPosition() + self._offset
        )

    def isInLowerZone(self) -> bool:
        return self.getHeight() <= self.height_lower_zone

    def getMotorInput(self):
        return self._motor.get()

    def hasReset(self):
        return self._has_reset

    def getCurrentDrawAmps(self) -> float:
        return self._motor.getOutputCurrent()

    def shouldMaintain(self):
        return self.getHeight() >= self.height_maintain and self.hasReset()

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def setOffset(value: float):
            self._offset = value

        def noop(x):
            pass

        def setHasReset(value: bool):
            self._has_reset = value

        builder.addStringProperty("state", lambda: self.state.name, noop)
        builder.addStringProperty(
            "state_movement", lambda: self.movement_state.name, noop
        )
        builder.addFloatProperty("motor_input", self._motor.get, noop)
        builder.addFloatProperty("encoder", self._encoder.getPosition, noop)
        builder.addFloatProperty("offset", lambda: self._offset, lambda x: setOffset(x))
        builder.addFloatProperty("height", self.getHeight, noop)
        builder.addBooleanProperty("has_reset", lambda: self._has_reset, setHasReset)
        builder.addBooleanProperty("switch_down", self._switch.isPressed, noop)
        builder.addBooleanProperty("isUp", self.isUp, noop)
        builder.addBooleanProperty("isDown", self.isDown, noop)
        builder.addBooleanProperty("shouldMaintain", self.shouldMaintain, noop)
        builder.addBooleanProperty("isInLowerZone", self.isInLowerZone, noop)
