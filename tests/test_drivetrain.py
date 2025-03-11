from hal import AllianceStationID
from wpilib.simulation import DriverStationSim

from commands.alignwithreefside import AlignWithReefSide
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


def test_AlignWithReefSide_not_crash(
    robot_controller: RobotTestController, robot: Robot
):
    DriverStationSim.setAllianceStationId(AllianceStationID.kRed1)
    robot_controller.startTeleop()
    robot_controller.run_command(AlignWithReefSide(robot.hardware.drivetrain), 10.0)
