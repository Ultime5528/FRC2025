from _pytest.python_api import approx

from commands.arm.extendarm import ExtendArm, arm_properties
from commands.arm.retractarm import RetractArm
from robot import Robot
from ultime.tests import RobotTestController


def test_ports(robot: Robot):
    assert robot.hardware.arm._motor.getChannel() == 0


def test_settings(robot: Robot):
    arm = robot.hardware.arm
    assert not arm._motor.getInverted()


def test_RetractArm(robot_controller: RobotTestController, robot: Robot):
    arm = robot.hardware.arm

    robot_controller.startTeleop()

    sampling_time = arm_properties.delay * 0.5

    cmd = RetractArm(arm)

    assert not cmd.isScheduled()
    assert arm._motor.get() == approx(0, rel=0.1)

    cmd.schedule()

    robot_controller.wait(arm_properties.delay - sampling_time)

    assert cmd.isScheduled()
    assert arm._motor.get() == approx(-arm.speed, rel=0.1)

    robot_controller.wait(sampling_time + 0.02)

    assert arm._motor.get() == approx(0.0)


def test_ExtendArm(robot_controller: RobotTestController, robot: Robot):
    arm = robot.hardware.arm
    robot_controller.startTeleop()

    sampling_time = arm_properties.delay * 0.5

    cmd = ExtendArm(arm)

    assert not cmd.isScheduled()
    assert arm._motor.get() == approx(0, rel=0.1)

    cmd.schedule()

    robot_controller.wait(arm_properties.delay - sampling_time)

    assert arm._motor.get() == approx(arm.speed, rel=0.1)
    assert cmd.isScheduled()

    robot_controller.wait(sampling_time + 0.02)

    assert arm._motor.get() == 0.0
