from _pytest.python_api import approx
from commands2 import Command
from pathplannerlib.auto import AutoBuilder, PathPlannerAuto
from pathplannerlib.config import RobotConfig
from pathplannerlib.path import PathPlannerPath

from commands.claw.drop import Drop, drop_properties
from robot import Robot
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.tests import RobotTestController


def testSimpleAutonomous(robot_controller: RobotTestController, robot: Robot):
    auto_test = AutoBuilder.buildAuto("AutoTest")
    auto_path = PathPlannerPath.fromPathFile("AutoTestPath")
    auto_traj = auto_path.getIdealTrajectory(RobotConfig.fromGUISettings())

    robot.autonomous.auto_chooser.setDefaultOption("AutoTest", auto_test)


    arm = robot.hardware.arm
    elevator = robot.hardware.elevator
    printer = robot.hardware.printer

    arm.movement_state = Arm.MovementState.FreeToMove
    elevator.movement_state = Elevator.MovementState.FreeToMove
    printer.movement_state = Printer.MovementState.FreeToMove

    elevator.setHeight(elevator.height_lower_zone + 0.1)
    elevator._has_reset = True
    elevator.stop()
    printer.setPosition(printer.right)
    printer.stop()


    robot_controller.startAutonomous()
    robot_controller.wait(0.02)
    assert auto_test.isScheduled()
    robot_controller.wait(0.02)

    assert arm._motor.get() == approx(0.0, rel=0.1)

    assert robot.hardware.drivetrain.getPose() == auto_path.getStartingHolonomicPose()
    robot_controller.wait_until(lambda: robot.hardware.drivetrain.getPose().X() == approx(auto_traj.getEndState().pose.X(), rel=0.3), 5)
    robot_controller.wait_until(lambda: robot.hardware.drivetrain.getPose().Y() == approx(auto_traj.getEndState().pose.Y(), rel=0.3), 5)
    robot_controller.wait_until(lambda: robot.hardware.drivetrain.getPose().rotation().degrees() == approx(auto_traj.getEndState().pose.rotation().degrees(), abs=0.3), 6)


    robot_controller.wait_until(lambda: arm._motor.get() == approx(-arm.speed, rel=0.1), 5)

    robot_controller.wait_until(lambda: arm._motor.get() == approx(0), 3)
