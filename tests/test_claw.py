from _pytest.python_api import approx
from commands2 import Command

from commands.claw.autodrop import AutoDrop
from commands.claw.drop import Drop, drop_properties
from commands.claw.loadcoral import load_coral_properties
from commands.elevator.moveelevator import MoveElevator
from commands.prepareloading import PrepareLoading
from commands.printer.moveprinter import MovePrinter
from commands.resetall import ResetAll
from robot import Robot
from subsystems.elevator import Elevator
from ultime.tests import RobotTestController


def test_ports(robot: Robot):
    assert robot.hardware.claw._motor_right.getChannel() == 1
    assert robot.hardware.claw._motor_left.getChannel() == 0
    assert robot.hardware.claw._sensor.getChannel() == 5


def testDropLevel1(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()

    sampling_time = drop_properties.delay * 0.5
    cmd = Drop.atLevel1(robot.hardware.claw)

    motor_left_started = not robot.hardware.claw._motor_left.getVoltage() == approx(0.0)
    motor_right_started = not robot.hardware.claw._motor_right.getVoltage() == approx(
        0.0
    )
    no_motor_started = not motor_left_started and not motor_right_started
    assert no_motor_started
    assert robot.hardware.claw._motor_left.get() == approx(0.0)
    assert robot.hardware.claw._motor_right.get() == approx(0.0)
    assert not cmd.isScheduled()

    cmd.schedule()

    robot_controller.wait(drop_properties.delay - sampling_time)
    motor_left_started = not robot.hardware.claw._motor_left.getVoltage() == approx(0.0)
    motor_right_started = not robot.hardware.claw._motor_right.getVoltage() == approx(
        0.0
    )
    two_motor_started = motor_left_started and motor_right_started
    no_motor_started = not motor_left_started and not motor_right_started
    assert not two_motor_started
    assert not no_motor_started
    assert robot.hardware.claw._motor_left.get() == approx(
        drop_properties.speed_level_1_left, rel=0.1
    )
    assert robot.hardware.claw._motor_right.get() == approx(
        drop_properties.speed_level_1_right, rel=0.1
    )
    assert cmd.isScheduled()

    robot_controller.wait(sampling_time + 0.02)
    motor_left_started = not robot.hardware.claw._motor_left.getVoltage() == approx(0.0)
    motor_right_started = not robot.hardware.claw._motor_right.getVoltage() == approx(
        0.0
    )
    no_motor_started = not motor_left_started and not motor_right_started
    assert no_motor_started
    assert robot.hardware.claw._motor_left.get() == approx(0.0, rel=0.1)
    assert robot.hardware.claw._motor_right.get() == approx(0.0, rel=0.1)
    assert not cmd.isScheduled()


def testDropLevels234(robot_controller: RobotTestController, robot: Robot):
    _testDropLevelCommon(
        robot_controller,
        robot,
        Drop.atLevel2(robot.hardware.claw),
        drop_properties.speed_level_2_left,
        drop_properties.speed_level_2_right,
    )
    _testDropLevelCommon(
        robot_controller,
        robot,
        Drop.atLevel3(robot.hardware.claw),
        drop_properties.speed_level_3_left,
        drop_properties.speed_level_3_right,
    )
    _testDropLevelCommon(
        robot_controller,
        robot,
        Drop.atLevel4(robot.hardware.claw),
        drop_properties.speed_level_4_left,
        drop_properties.speed_level_4_right,
    )


def _testDropLevelCommon(
    robot_controller: RobotTestController,
    robot: Robot,
    cmd: Command,
    speed_left: float,
    speed_right: float,
):
    robot_controller.startTeleop()

    sampling_time = drop_properties.delay * 0.5

    motor_left_started = not robot.hardware.claw._motor_left.getVoltage() == approx(0.0)
    motor_right_started = not robot.hardware.claw._motor_right.getVoltage() == approx(
        0.0
    )
    no_motor_started = not motor_left_started and not motor_right_started
    assert no_motor_started
    assert robot.hardware.claw._motor_left.get() == approx(0.0, rel=0.1)
    assert robot.hardware.claw._motor_right.get() == approx(0.0, rel=0.1)
    assert not cmd.isScheduled()

    cmd.schedule()

    robot_controller.wait(drop_properties.delay - sampling_time)
    motor_left_started = not robot.hardware.claw._motor_left.getVoltage() == approx(0.0)
    motor_right_started = not robot.hardware.claw._motor_right.getVoltage() == approx(
        0.0
    )
    two_motor_started = motor_left_started and motor_right_started
    no_motor_started = not motor_left_started and not motor_right_started
    assert two_motor_started
    assert not no_motor_started
    assert robot.hardware.claw._motor_left.get() == approx(speed_left, rel=0.1)
    assert robot.hardware.claw._motor_right.get() == approx(speed_right, rel=0.1)
    assert cmd.isScheduled()

    robot_controller.wait(sampling_time + 0.02)
    motor_left_started = not robot.hardware.claw._motor_left.getVoltage() == approx(0.0)
    motor_right_started = not robot.hardware.claw._motor_right.getVoltage() == approx(
        0.0
    )
    no_motor_started = not motor_left_started and not motor_right_started
    assert no_motor_started
    assert robot.hardware.claw._motor_left.get() == approx(0.0, rel=0.1)
    assert robot.hardware.claw._motor_right.get() == approx(0.0, rel=0.1)
    assert not cmd.isScheduled()


def common_test_autodrop(
    robot_controller: RobotTestController,
    robot: Robot,
    CreateMoveElevator,
    elevator_state,
    speed_left,
    speed_right,
):

    robot_controller.startTeleop()

    reset_all = ResetAll(
        robot.hardware.elevator,
        robot.hardware.printer,
        robot.hardware.arm,
        robot.hardware.intake,
        robot.hardware.climber,
    )
    reset_all.schedule()
    robot_controller.wait_until(lambda: not reset_all.schedule(), 30.0)

    CreateMoveElevator(robot.hardware.elevator).schedule()
    robot_controller.wait(10)

    assert robot.hardware.elevator.state == elevator_state

    AutoDrop(robot.hardware.claw, robot.hardware.elevator).schedule()

    robot_controller.wait(0.05)

    assert robot.hardware.claw._motor_left.get() == approx(speed_left, abs=0.05)
    assert robot.hardware.claw._motor_right.get() == approx(speed_right, abs=0.05)


def test_AutoDrop_Level1(robot_controller, robot):
    common_test_autodrop(
        robot_controller,
        robot,
        MoveElevator.toLevel1,
        Elevator.State.Level1,
        drop_properties.speed_level_1_left,
        drop_properties.speed_level_1_right,
    )


def test_AutoDrop_Level2(robot_controller, robot):
    common_test_autodrop(
        robot_controller,
        robot,
        MoveElevator.toLevel2,
        Elevator.State.Level2,
        drop_properties.speed_level_2_left,
        drop_properties.speed_level_2_right,
    )


def test_AutoDrop_Level3(robot_controller, robot):
    common_test_autodrop(
        robot_controller,
        robot,
        MoveElevator.toLevel3,
        Elevator.State.Level3,
        drop_properties.speed_level_3_left,
        drop_properties.speed_level_3_right,
    )


def test_AutoDrop_Level4(robot_controller, robot):
    common_test_autodrop(
        robot_controller,
        robot,
        MoveElevator.toLevel4,
        Elevator.State.Level4,
        drop_properties.speed_level_4_left,
        drop_properties.speed_level_4_right,
    )


def test_LoadingDetection(robot_controller: RobotTestController, robot: Robot):
    arm = robot.hardware.arm
    claw = robot.hardware.claw
    climber = robot.hardware.climber
    elevator = robot.hardware.elevator
    intake = robot.hardware.intake
    printer = robot.hardware.printer

    robot_controller.startTeleop()

    cmd = ResetAll(elevator, printer, arm, intake, climber)
    cmd.schedule()
    robot_controller.wait_until(lambda: not cmd.isScheduled(), 10.0)

    cmd = MoveElevator.toLevel4(elevator)
    cmd.schedule()
    robot_controller.wait_until(lambda: not cmd.isScheduled(), 10.0)

    cmd = MovePrinter.toMiddleRight(printer)
    cmd.schedule()
    robot_controller.wait_until(lambda: not cmd.isScheduled(), 10.0)

    # Test that even if the sensors sees something, it won't consider having a coral if it is not at loading
    claw._sensor.setSimPressed()
    assert not claw._load_command.isScheduled()
    assert not claw.is_at_loading
    assert claw._motor_right.get() == approx(0.0, rel=0.1)
    assert claw._motor_left.get() == approx(0.0, rel=0.1)
    assert not claw.has_coral

    # Going to loading
    cmd_prepare_loading = PrepareLoading(elevator, arm, printer)
    cmd_prepare_loading.schedule()

    # Not at loading yet, so even if sensor sees something, it won't consider having a coral if it is not at loading
    robot_controller.wait(0.02)
    assert cmd_prepare_loading.isScheduled()
    assert not claw._load_command.isScheduled()
    assert not claw.is_at_loading
    assert claw._motor_right.get() == approx(0.0, rel=0.1)
    assert claw._motor_left.get() == approx(0.0, rel=0.1)
    assert not claw.has_coral

    # We are going to loading, and at some point the sensor doesn't detect anything
    robot_controller.wait(0.02)
    claw._sensor.setSimUnpressed()
    assert cmd_prepare_loading.isScheduled()
    assert not claw._load_command.isScheduled()
    assert not claw.is_at_loading
    assert claw._motor_right.get() == approx(0.0, rel=0.1)
    assert claw._motor_left.get() == approx(0.0, rel=0.1)
    assert not claw.has_coral

    # We are now at loading and the coral is not in the robot yet
    robot_controller.wait_until(lambda: not cmd_prepare_loading.isScheduled(), 10.0)
    assert not cmd_prepare_loading.isScheduled()
    assert (
        not claw.is_at_loading
    )  # The LoadingDetection Module has not been run yet, so we are still not at loading
    assert claw._motor_right.get() == approx(0.0, rel=0.1)
    assert claw._motor_left.get() == approx(0.0, rel=0.1)
    assert not claw.has_coral

    # We are now at loading and a coral is put in the robot
    # The sensor detects it
    robot_controller.wait(0.02)
    claw._sensor.setSimPressed()
    assert not cmd_prepare_loading.isScheduled()
    assert not claw._load_command.isScheduled()
    assert claw.is_at_loading
    assert claw._motor_right.get() == approx(0.0, rel=0.1)
    assert claw._motor_left.get() == approx(0.0, rel=0.1)
    assert not claw.has_coral

    # We are at loading and the sensor stops seeing the coral after the wheels have moved the coral forward
    robot_controller.wait(0.02)
    claw._sensor.setSimUnpressed()
    assert not cmd_prepare_loading.isScheduled()
    assert claw._load_command.isScheduled()
    assert claw.is_at_loading
    assert claw._motor_right.get() == approx(load_coral_properties.speed_right, rel=0.1)
    assert claw._motor_left.get() == approx(load_coral_properties.speed_left, rel=0.1)
    assert not claw.has_coral

    # The motors are stopped
    robot_controller.wait(load_coral_properties.delay + 5.0)
    assert not cmd_prepare_loading.isScheduled()
    assert not claw._load_command.isScheduled()
    assert not claw.is_at_loading
    assert claw._motor_right.get() == approx(0.0, rel=0.1)
    assert claw._motor_left.get() == approx(0.0, rel=0.1)
    assert claw.has_coral
    assert printer.state == printer.State.MiddleRight
