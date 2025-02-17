from enum import Enum, auto

import wpilib
from wpilib import VictorSP, RobotBase
from wpilib.simulation import PWMSim, EncoderSim, AnalogInputSim
from wpiutil import SendableBuilder

import ports
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem
from ultime.switch import Switch


class Intake(Subsystem):
    class State(Enum):
        Unknown = auto()
        Moving = auto()
        Extended = auto()
        Retracted = auto()

    grab_speed = autoproperty(0.3)
    pivot_position_min = autoproperty(0.0)
    threshold_grab = autoproperty(2.0)
    position_conversion_factor = autoproperty(0.18)

    def __init__(self):
        super().__init__()
        self.state = Intake.State.Unknown

        self._pivot_motor = VictorSP(ports.PWM.intake_motor_pivot)
        self._pivot_encoder = wpilib.Encoder(
            ports.DIO.intake_encoder_a,
            ports.DIO.intake_encoder_b,
            reverseDirection=False,
        )

        self._pivot_encoder.setDistancePerPulse(self.position_conversion_factor)
        self._pivot_switch = Switch(
            Switch.Type.NormallyClosed, ports.DIO.intake_switch_pivot
        )

        self._grab_motor = VictorSP(ports.PWM.intake_motor_grab)
        self._grab_sensor = wpilib.AnalogInput(ports.Analog.intake_grab_sensor)

        self.addChild("pivot_motor", self._pivot_motor)
        self.addChild("grab_motor", self._grab_motor)
        self.addChild("pivot_encoder", self._pivot_encoder)

        self._has_reset = False
        self._prev_is_retracted = False
        self._offset = 0.0

        if RobotBase.isSimulation():
            self._sim_grab_motor = PWMSim(self._grab_motor)
            self._sim_pivot_motor = PWMSim(self._pivot_motor)
            self._sim_encoder = EncoderSim(self._pivot_encoder)
            self._sim_pos_initial = 0.3
            self._sim_pos = self._sim_pos_initial
            self._sim_grab_sensor = AnalogInputSim(self._grab_sensor)

    def periodic(self) -> None:
        if self._prev_is_retracted and not self.isRetracted():
            self._offset = self.pivot_position_min - self._pivot_encoder.get()
            self._has_reset = True
        self._prev_is_retracted = self.isRetracted()

    def simulationPeriodic(self) -> None:
        distance = self._pivot_motor.get() * 3

        self._sim_pos += distance
        self._sim_encoder.setCount(
            int(
                (self._sim_pos - self._sim_pos_initial)
                / self.position_conversion_factor
            )
        )

        if self._sim_pos <= -0.01:
            self._pivot_switch.setSimPressed()
        else:
            self._pivot_switch.setSimUnpressed()

    def stopPivot(self):
        self._pivot_motor.stopMotor()

    def setPivotSpeed(self, speed: float):
        if speed < 0.0 and self.isRetracted():
            speed = 0.0
        self._pivot_motor.set(speed)

    def grab(self):
        self._grab_motor.set(self.grab_speed)

    def drop(self):
        self._grab_motor.set(-1 * self.grab_speed)

    def stopGrab(self):
        self._grab_motor.stopMotor()

    def getPivotPosition(self):
        return (
            self._pivot_encoder.get() + self._offset
        ) * self.position_conversion_factor

    def hasReset(self):
        return self._has_reset

    def isRetracted(self):
        return self._pivot_switch.isPressed()

    def hasAlgae(self):
        return self._grab_sensor.getVoltage() >= self.threshold_grab

    def getPivotMotorInput(self):
        return self._pivot_motor.get()

    def getCurrentDrawAmps(self) -> float:
        return 0.0

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def setOffset(value: float):
            self._offset = value

        def noop(x):
            pass

        def setHasReset(value: bool):
            self._has_reset = value

        builder.addStringProperty("state", lambda: self.state.name, noop)
        builder.addFloatProperty("pivot_motor_input", self._pivot_motor.get, noop)
        builder.addFloatProperty("grab_motor_input", self._grab_motor.get, noop)
        builder.addFloatProperty("pivot_encoder", self._pivot_encoder.get, noop)
        builder.addFloatProperty("offset", lambda: self._offset, lambda x: setOffset(x))
        builder.addFloatProperty("pivot_position", self.getPivotPosition, noop)
        builder.addBooleanProperty("has_reset", lambda: self._has_reset, setHasReset)
        builder.addBooleanProperty("hasAlgae", self.hasAlgae, noop)
        builder.addFloatProperty("grab_voltage", self._grab_sensor.getVoltage, noop)
        builder.addFloatProperty(
            "grab_voltage_average", self._grab_sensor.getAverageVoltage, noop
        )
        builder.addBooleanProperty("pivot_switch", self._pivot_switch.isPressed, noop)
        builder.addBooleanProperty("isRetracted", self.isRetracted, noop)
