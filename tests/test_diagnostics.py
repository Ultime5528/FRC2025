import pytest

from robot import Robot
from ultime.tests import RobotTestController


def test_runs_in_test_mode(robot_controller: RobotTestController, robot: Robot):
    diagnose_command = robot.diagnostics._run_all_command
    assert not diagnose_command.isScheduled()

    # Trigger all alerts
    robot.hardware.claw._sensor.setSimPressed()
    robot_controller.startTest()
    assert diagnose_command.isScheduled()

    robot_controller.wait_until(lambda: not diagnose_command.isScheduled(), 30.0)
