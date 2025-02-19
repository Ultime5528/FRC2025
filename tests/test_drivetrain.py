from commands.drivetrain.resetgyro import ResetGyro
from robot import Robot
from ultime.tests import RobotTestController


def test_ResetGyro(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()
    robot_controller.wait(0.5)
    cmd = ResetGyro(robot.hardware.drivetrain)
    cmd.schedule()
    robot_controller.wait(0.5)
    assert not cmd.isScheduled()
