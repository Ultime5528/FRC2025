from _pytest.python_api import approx

from commands.claw.drop import Drop
from robot import Robot
from ultime.tests import RobotTestController


def test_ports(robot: Robot):
    assert robot.hardware.claw._motor_right.getChannel() == 0
    assert robot.hardware.claw._motor_left.getChannel() == 1

def testDropLevel1(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()

    cmd = Drop.atLevel1(robot.hardware.claw)
    cmd.schedule()

    robot_controller.wait(0.1)
    assert robot.hardware.claw._motor_left.get() == approx(cmd.get_speed_left(), rel=0.1)
    assert robot.hardware.claw._motor_left.get() == approx(cmd.get_speed_left(), rel=0.1)
    assert robot.hardware.claw._motor_right.get() == approx(cmd.get_speed_right(), rel=0.1)
    assert (cmd.get_speed_left() == 0.0 or cmd.get_speed_right() == 0.0) and not (cmd.get_speed_left() == 0.0 and cmd.get_speed_right == 0.0)

    robot_controller.wait(cmd.delay - 0.4)
    assert robot.hardware.claw._motor_left.get() == approx(cmd.get_speed_left(), rel=0.1)
    assert robot.hardware.claw._motor_right.get() == approx(cmd.get_speed_right(), rel=0.1)
    assert (cmd.get_speed_left() == 0.0 or cmd.get_speed_right() == 0.0) and not (cmd.get_speed_left() == 0.0 and cmd.get_speed_right == 0.0)

    robot_controller.wait(0.8)
    assert cmd.get_speed_left() == 0.0 and cmd.get_speed_right() == 0.0
    assert not cmd.isScheduled()