from hal import AllianceStationID
from wpilib.simulation import DriverStationSim

from commands.alignwithreefside import AlignWithReefSide
from commands.drivetrain.driverelative import DriveRelative
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


def test_drive_relative(robot_controller: RobotTestController, robot: Robot):
    drivetrain = robot.hardware.drivetrain

    robot_controller.startTeleop()

    # Move left
    left_cmd = DriveRelative.left(drivetrain)
    left_cmd.schedule()
    robot_controller.wait_until(lambda: drivetrain.getPose().Y() >= 1, 5.0)

    # Move right
    right_cmd = DriveRelative.right(drivetrain)
    right_cmd.schedule()
    robot_controller.wait_until(lambda: drivetrain.getPose().Y() <= 0, 5.0)

    # Move forwards
    left_cmd = DriveRelative.forwards(drivetrain)
    left_cmd.schedule()
    robot_controller.wait_until(lambda: drivetrain.getPose().X() >= 1, 5.0)

    # Move backwards
    right_cmd = DriveRelative.backwards(drivetrain)
    right_cmd.schedule()
    robot_controller.wait_until(lambda: drivetrain.getPose().X() <= 0, 5.0)


def test_AlignWithReefSide_not_crash(
    robot_controller: RobotTestController, robot: Robot
):
    DriverStationSim.setAllianceStationId(AllianceStationID.kRed1)
    robot_controller.startTeleop()
    robot_controller.run_command(AlignWithReefSide(robot.hardware.drivetrain), 10.0)
