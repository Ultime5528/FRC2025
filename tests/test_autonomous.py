from _pytest.python_api import approx
from commands2 import Command
from pathplannerlib.auto import AutoBuilder, PathPlannerAuto
from pathplannerlib.config import RobotConfig
from pathplannerlib.path import PathPlannerPath

from commands.claw.drop import Drop, drop_properties
from robot import Robot
from ultime.tests import RobotTestController


def testSimpleAutonomous(robot_controller: RobotTestController, robot: Robot):
    auto_test = AutoBuilder.buildAuto("AutoTest")
    auto_path = PathPlannerPath.fromPathFile("AutoTestPath")
    auto_traj = auto_path.getIdealTrajectory(RobotConfig.fromGUISettings())

    robot.autonomous.auto_chooser.setDefaultOption("AutoTest", auto_test)

    robot_controller.startAutonomous()
    robot_controller.wait(0.02)
    assert auto_test.isScheduled()
    robot_controller.wait(0.02)

    assert robot.hardware.drivetrain.getPose() == auto_path.getStartingHolonomicPose()
    robot_controller.wait(auto_traj.getEndState().timeSeconds + 2)

    assert robot.hardware.arm._motor.get() == approx(robot.hardware.arm.speed, rel=0.1)

    robot_controller.wait(2.0)

    assert robot.hardware.arm._motor.get() == approx(0.0)
