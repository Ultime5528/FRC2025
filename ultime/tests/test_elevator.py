from rev import SparkBase, SparkBaseConfig

from robot import Robot
from ultime.switch import Switch


def test_ports(robot: Robot):
    elevator = robot.hardware.elevator

    assert elevator._motor.getChannel() == 9
    assert elevator._switch.getChannel() == 0


def test_settings(robot: Robot):
    elevator = robot.hardware.elevator

    assert not elevator._motor.getInverted()
    assert elevator._switch_up.getType() == Switch.Type.NormallyClosed
    assert elevator._motor.getMotorType() == SparkBase.MotorType.kBrushless

    assert not elevator._motor.configAccessor.getInverted()
    assert (
        elevator._motor.configAccessor.getIdleMode() == SparkBaseConfig.IdleMode.kBrake
    )
    assert elevator._motor.configAccessor.getSmartCurrentLimit() == 30
    assert elevator._motor.configAccessor.encoder.getPositionConversionFactor() == 1
