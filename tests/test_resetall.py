from commands.resetall import ResetAll
from commands.resetallbutclimber import ResetAllButClimber
from robot import Robot
from ultime.tests import RobotTestController


def test_reset_all(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()
    elevator = robot.hardware.elevator
    printer = robot.hardware.printer
    arm = robot.hardware.arm
    intake = robot.hardware.intake
    climber = robot.hardware.climber

    cmd = ResetAll(elevator, printer, arm, intake, climber)
    cmd.schedule()

    robot_controller.wait_until(lambda: not cmd.isScheduled(), 10.0)

    assert elevator.hasReset()
    assert printer.hasReset()
    assert arm.state == arm.State.Retracted
    assert intake.hasReset()
    assert climber._has_reset


def test_reset_all_but_climber(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()
    elevator = robot.hardware.elevator
    printer = robot.hardware.printer
    arm = robot.hardware.arm
    intake = robot.hardware.intake

    cmd = ResetAllButClimber(elevator, printer, arm, intake)
    cmd.schedule()

    robot_controller.wait_until(lambda: not cmd.isScheduled(), 10.0)

    assert printer.hasReset()
    assert arm.state == arm.State.Retracted
    assert intake.hasReset()
    assert elevator.hasReset()
