import pytest
from _pytest.python_api import approx

from commands.arm.extendarm import ExtendArm
from commands.arm.retractarm import RetractArm
from subsystems.arm import Arm
from robot import Robot
from ultime.tests import RobotTestController


def testPorts(robot: Robot):
    assert robot.hardware.arm._motor.getChannel() == 0

def testSettings(robot: Robot):
    arm = robot.hardware.arm
    assert not arm._motor.getInverted()


def testRetractArm(robot_controller: RobotTestController, robot: Robot):
    arm = robot.hardware.arm

    robot_controller.startTeleop()

    cmd = RetractArm(arm)
    cmd.schedule()

    robot_controller.wait(0.1)

    assert cmd.isScheduled()
    assert arm._motor.get() == approx(arm.speed, rel=0.1)

    robot_controller.wait(cmd.delay + 0.1)

    assert arm._motor.get() == approx(0.0)


def testExtendArm(robot_controller: RobotTestController, robot: Robot):
    arm = robot.hardware.arm
    robot_controller.startTeleop()

    cmd = ExtendArm(arm)
    cmd.schedule()

    robot_controller.wait(0.1)

    assert arm._motor.get() == approx(arm.speed * -1, rel=0.1)
    assert cmd.isScheduled()

    robot_controller.wait(cmd.delay + 0.1)

    assert arm._motor.get() == approx(0.0)
