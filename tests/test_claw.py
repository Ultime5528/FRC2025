from idlelib.undo import Command

from commands.claw.drop import Drop, drop_properties
from robot import Robot
from ultime.tests import RobotTestController


def test_ports(robot: Robot):
    assert robot.hardware.claw._motor_right.getChannel() == 0
    assert robot.hardware.claw._motor_left.getChannel() == 1


def testDropLevel1(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()

    sampling_time = drop_properties.delay * 0.5
    cmd = Drop.atLevel1(robot.hardware.claw)

    motor_left_started = robot.hardware.claw.isLeftRunning()
    motor_right_started = robot.hardware.claw.isRightRunning()
    no_motor_started = not motor_left_started and not motor_right_started
    assert no_motor_started
    assert not cmd.isScheduled()

    cmd.schedule()

    robot_controller.wait(drop_properties.delay - sampling_time)
    motor_left_started = robot.hardware.claw.isLeftRunning()
    motor_right_started = robot.hardware.claw.isRightRunning()
    two_motor_started = motor_left_started and motor_right_started
    no_motor_started = not motor_left_started and not motor_right_started
    assert not two_motor_started
    assert not no_motor_started
    assert cmd.isScheduled()

    robot_controller.wait(sampling_time + 0.02)
    motor_left_started = robot.hardware.claw.isLeftRunning()
    motor_right_started = robot.hardware.claw.isRightRunning()
    no_motor_started = not motor_left_started and not motor_right_started
    assert no_motor_started
    assert not cmd.isScheduled()


def testDropLevels234(robot_controller: RobotTestController, robot: Robot):
    _testDropLevelCommon(robot_controller, robot, Drop.atLevel2(robot.hardware.claw))
    _testDropLevelCommon(robot_controller, robot, Drop.atLevel3(robot.hardware.claw))
    _testDropLevelCommon(robot_controller, robot, Drop.atLevel4(robot.hardware.claw))


def _testDropLevelCommon(
    robot_controller: RobotTestController, robot: Robot, cmd: Command
):
    robot_controller.startTeleop()

    sampling_time = drop_properties.delay * 0.5

    motor_left_started = robot.hardware.claw.isLeftRunning()
    motor_right_started = robot.hardware.claw.isRightRunning()
    no_motor_started = not motor_left_started and not motor_right_started
    assert no_motor_started
    assert not cmd.isScheduled()

    cmd.schedule()

    robot_controller.wait(drop_properties.delay - sampling_time)
    motor_left_started = robot.hardware.claw.isLeftRunning()
    motor_right_started = robot.hardware.claw.isRightRunning()
    two_motor_started = motor_left_started and motor_right_started
    no_motor_started = not motor_left_started and not motor_right_started
    assert two_motor_started
    assert not no_motor_started
    assert cmd.isScheduled()

    robot_controller.wait(sampling_time + 0.02)
    motor_left_started = robot.hardware.claw.isLeftRunning()
    motor_right_started = robot.hardware.claw.isRightRunning()
    no_motor_started = not motor_left_started and not motor_right_started
    assert no_motor_started
    assert not cmd.isScheduled()
