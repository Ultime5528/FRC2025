from typing import Literal, Optional

import wpilib
from rev import SparkMax, REVLibError, SparkMaxConfig
from wpilib import RobotBase

IdleMode = Literal["brake", "coast"]

__all__ = ["configureLeader", "configureFollower", "waitForCAN"]

def waitForCAN(time_second: float):
    if not RobotBase.isSimulation():
        wpilib.wait(time_second)

def configureLeader(
        motor: SparkMax,
        config: SparkMaxConfig,
        mode: IdleMode,
        inverted: bool = False,
        stallLimit: Optional[int] = None,
        freeLimit: Optional[int] = None,
):
    _handleCanError(motor.ResetMode, "ResetMode", motor)
    motor.setInverted(inverted)
    _configureMotor(motor, mode, stallLimit, freeLimit)

def configureFollower(
    follower: SparkMax,
    leader: SparkMax,
    mode: IdleMode,
    inverted: bool = False,
    stallLimit: Optional[int] = None,
    freeLimit: Optional[int] = None,
):
    _handleCanError(
        follower.ResetMode, "ResetMode", follower
    )
    _handleCanError(follower.isFollower(), "follow", follower)
    _handleCanError(
        follower.setControlFramePeriodMs(SparkMax.PeriodicFrame.kStatus0),
        "set status0 rate",
        follower,
    )
    _handleCanError(
        follower.setControlFramePeriodMs(SparkMax.PeriodicFrame.kStatus1),
        "set status1 rate",
        follower,
    )
    _handleCanError(
        follower.setControlFramePeriodMs(SparkMax.PeriodicFrame.kStatus2),
        "set status2 rate",
        follower,
    )
    _configureMotor(follower, mode, stallLimit, freeLimit)

def _configureMotor(
    motor: SparkMax,
    mode: IdleMode,
    stallLimit: Optional[int],
    freeLimit: Optional[int],
):
    _handleCanError(motor.IdleMode, "setIdleMode", motor)
    _handleCanError(motor.PersistMode, 'setPersistMode', motor)
    _handleCanError(motor.clearFaults(), "clearFaults", motor)

    #if stallLimit is not None and freeLimit is not None:
     #   _handleCanError(
      #      motor.CurrentLimit(stallLimit, freeLimit),#can't find current Limit
       #     "setSmartCurrentLimit",
        #    motor,
#        )
 #   elif (stallLimit is None) != (freeLimit is None):
  #      raise ValueError(
   #         f"stallLimit ({stallLimit}) and freeLimit ({freeLimit}) should both have a value."
    #    )

    waitForCAN(1.0)

def _idleModeToEnum(mode: IdleMode):
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