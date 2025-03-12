from hal import AllianceStationID
from wpilib.simulation import DriverStationSim

from commands.alignwithreefside import AlignWithReefSide
from commands.drivetrain.movehorizontal import MoveHorizontal
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


def test_movehorizontal(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()
    robot_controller.wait(0.5)

    # Move left
    left_cmd = MoveHorizontal.left(robot.hardware.drivetrain)
    left_cmd.schedule()
    robot_controller.wait(1.0)
    assert robot.hardware.drivetrain.getPose().Y() >= 1

    # Move right
    right_cmd = MoveHorizontal.right(robot.hardware.drivetrain)
    right_cmd.schedule()
    robot_controller.wait(2.0)
    assert robot.hardware.drivetrain.getPose().Y() <= 0


def test_AlignWithReefSide_not_crash(
    robot_controller: RobotTestController, robot: Robot
):
    DriverStationSim.setAllianceStationId(AllianceStationID.kRed1)
    robot_controller.startTeleop()
    robot_controller.run_command(AlignWithReefSide(robot.hardware.drivetrain), 10.0)
