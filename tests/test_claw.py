from _pytest.python_api import approx
from commands2 import Command

from commands.claw.autodrop import AutoDrop
from commands.claw.drop import Drop, drop_properties
from commands.claw.loadcoral import LoadCoral
from commands.elevator.moveelevator import MoveElevator
from commands.elevator.resetelevator import ResetElevator
from robot import Robot
from subsystems.elevator import Elevator
from ultime.tests import RobotTestController


def test_ports(robot: Robot):
    assert robot.hardware.claw._motor_right.getChannel() == 0
    assert robot.hardware.claw._motor_left.getChannel() == 1
    assert robot.hardware.claw._sensor.getChannel() == 1


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


def testLoadCoral(
    robot_controller: RobotTestController,
    robot: Robot,
):
    robot_controller.startTeleop()
    claw = robot.hardware.claw

    claw._sensor.setSimUnpressed()

    assert not claw.hasCoralInLoader()

    claw._sensor.setSimPressed()
    assert claw.hasCoralInLoader()

    robot_controller.wait(0.1)

    cmd = LoadCoral(claw)

    assert robot.hardware.claw._motor_left.get() == approx(cmd.speed_left, rel=0.1)
    assert robot.hardware.claw._motor_right.get() == approx(cmd.speed_right, rel=0.1)

    claw._sensor.setSimUnpressed()
    assert not claw.hasCoralInLoader()

    robot_controller.wait(0.05 + cmd.delay)

    assert robot.hardware.claw._motor_left.get() == approx(0.0, rel=0.1)
    assert robot.hardware.claw._motor_right.get() == approx(0.0, rel=0.1)


def common_test_autodrop(
    robot_controller: RobotTestController,
    robot: Robot,
    CreateMoveElevator,
    elevator_state,
    speed_left,
    speed_right,
):

    robot_controller.startTeleop()

    ResetElevator(robot.hardware.elevator).schedule()
    robot_controller.wait(10)

    assert robot.hardware.elevator.hasReset()

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
