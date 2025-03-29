from enum import Enum, auto

import wpilib
from wpilib import VictorSP, RobotBase
from wpilib.simulation import PWMSim, EncoderSim
from wpiutil import SendableBuilder

import ports
from ultime.alert import AlertType
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem
from ultime.switch import Switch
from ultime.timethis import tt


class Intake(Subsystem):
    class State(Enum):
        Unknown = auto()
        Moving = auto()
        Extended = auto()
        Retracted = auto()
        Drop = auto()

    speed_pivot = autoproperty(0.3)
    speed_grab = autoproperty(0.8)
    pivot_position_min = autoproperty(0.0)
    threshold_grab = autoproperty(2.0)

    position_conversion_factor = autoproperty(0.445)

    def __init__(self):
        super().__init__()
        self.state = Intake.State.Unknown

        self._pivot_motor = VictorSP(ports.PWM.intake_motor_pivot)
        self._pivot_encoder = wpilib.Encoder(
            ports.DIO.intake_encoder_a,
            ports.DIO.intake_encoder_b,
            reverseDirection=True,
        )

        self._pivot_switch = Switch(
            Switch.Type.NormallyClosed, ports.DIO.intake_switch_pivot
        )

        self._grab_motor = VictorSP(ports.PWM.intake_motor_grab)
        self._grab_switch = Switch(
            Switch.Type.NormallyClosed, ports.DIO.intake_switch_grab
        )

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

        self.alert_has_algae_failed = self.createAlert(
            "Intake didn't return correct value in hasAlgae. Is there an actual algae in the robot?",
            AlertType.Warning,
        )
        self.alert_retract_failed = self.createAlert(
            "Intake didn't retract correctly. Check connections", AlertType.Error
        )
        self.alert_extend_failed = self.createAlert(
            "Intake didn't extend correctly. Check connections", AlertType.Error
        )
        self.alert_is_retracted_failed = self.createAlert(
            "Intake didn't return correct value in isRetracted. Is the sensor properly connected? Check connections.",
            AlertType.Error,
        )
        self.alert_pivot_motor_hi = self.createAlert(
            "Pivot motor current measured too high. Is it connected? "
            + f"PWM={ports.PWM.intake_motor_pivot}",
            AlertType.Error,
        )
        self.alert_pivot_motor_lo = self.createAlert(
            "Pivot motor current measured too low. Is it connected? "
            + f"PWM={ports.PWM.intake_motor_pivot}",
            AlertType.Error,
        )
        self.alert_grab_motor_hi = self.createAlert(
            "Grab motor current measured too high. Is it connected? "
            + f"PWM={ports.PWM.intake_motor_grab}",
            AlertType.Error,
        )
        self.alert_grab_motor_lo = self.createAlert(
            "Grab motor current measured too low. Is it connected? "
            + f"PWM={ports.PWM.intake_motor_grab}",
            AlertType.Error,
        )

    def periodic(self) -> None:
        if not self.hasReset():
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

    def retract(self):
        self.setPivotSpeed(-self.speed_pivot)

    def extend(self):
        self.setPivotSpeed(self.speed_pivot)

    def grab(self):
        self._grab_motor.set(self.speed_grab)

    def drop(self):
        self._grab_motor.set(-1 * self.speed_grab)

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
        return self._grab_switch.isPressed()

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

        builder.addStringProperty("state", tt(lambda: self.state.name), noop)
        builder.addFloatProperty("pivot_motor_input", tt(self._pivot_motor.get), noop)
        builder.addFloatProperty("grab_motor_input", tt(self._grab_motor.get), noop)
        builder.addFloatProperty("pivot_encoder", tt(self._pivot_encoder.get), noop)
        builder.addFloatProperty(
            "offset", tt(lambda: self._offset), lambda x: setOffset(x)
        )
        builder.addFloatProperty("pivot_position", tt(self.getPivotPosition), noop)
        builder.addBooleanProperty(
            "has_reset", tt(lambda: self._has_reset), setHasReset
        )
        builder.addBooleanProperty("hasAlgae", tt(self.hasAlgae), noop)
        builder.addBooleanProperty(
            "pivot_switch", tt(self._pivot_switch.isPressed), noop
        )
        builder.addBooleanProperty("isRetracted", tt(self.isRetracted), noop)
