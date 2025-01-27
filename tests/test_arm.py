from _pytest.python_api import approx

from commands.arm.retractarm import RetractArm
from robot import Robot
from ultime.tests import RobotTestController


def testPorts(robot: Robot):
    arm = robot.hardware.arm
    assert arm.arm_motor.getChannel() == 0

def testSettings(robot: Robot):
    arm = robot.hardware.arm

    assert not arm.arm_motor.getInverted()

def testRetractArm(robot_controller: RobotTestController, robot: Robot):
    arm = robot.hardware.arm

    robot_controller.startTeleop()

    cmd = RetractArm(arm)
    cmd.schedule()

    robot_controller.wait(0.1)

    assert arm.arm_motor.get() == approx(arm.speed)
    assert cmd.isScheduled()

    robot_controller.wait(5)

    assert arm.arm_motor.get() == 0