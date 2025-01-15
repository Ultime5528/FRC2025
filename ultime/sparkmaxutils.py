from typing import Literal, Optional

import wpilib
from rev import SparkMax, REVLibError, SparkMaxConfig
from wpilib import RobotBase

#IdleMode = Literal["kbrake", "kcoast"]

__all__ = ["configureLeader", "configureFollower", "waitForCAN"]

def waitForCAN(time_second: float):
    if not RobotBase.isSimulation():
        wpilib.wait(time_second)

def configureLeader(
        motor: SparkMax,
        config: SparkMaxConfig,
        mode: SparkMax.IdleMode,
        inverted: bool = False,
        stallLimit: Optional[int] = None,
        freeLimit: Optional[int] = None,
):
    config.inverted(inverted)
    config.smartCurrentLimit(stallLimit, freeLimit)
    config.setIdleMode(mode)

    _configureMotor(motor, config)

def configureFollower(
    follower: SparkMax,
    leader: SparkMax,
    config: SparkMaxConfig,
    mode: SparkMax.IdleMode,
    inverted: bool = False,
    stallLimit: Optional[int] = None,
    freeLimit: Optional[int] = None,
):
    config.inverted(inverted)
    config.smartCurrentLimit(stallLimit, freeLimit)
    config.setIdleMode(mode)
    config.follow(leader.getDeviceId(), inverted)

    _configureMotor(follower, config)

def _configureMotor(
    motor: SparkMax,
    config: SparkMaxConfig,
):
    _handleCanError(motor.configure(config, motor.ResetMode(1), motor.PersistMode(1)), "configure motor", motor)
    _handleCanError(motor.clearFaults(), "clearFaults", motor)

    waitForCAN(1.0)

def _idleModeToEnum(mode: SparkMax.IdleMode):
    if mode == "brake":
        return SparkMax.IdleMode.kBrake
    elif mode == "coast":
        return SparkMax.IdleMode.kCoast
    raise ValueError(f"mode is not 'brake' or 'coast' : {mode}")


def _handleCanError(error: REVLibError, function: str, motor: SparkMax):
    if error != REVLibError.kOk:
        wpilib.reportError(
            f"CANError on motor ID {motor.getDeviceId()} during {function} : {error}",
            printTrace=True,
        )