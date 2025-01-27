from _pytest.python_api import approx
from rev import SparkBase, SparkBaseConfig
from wpilib.simulation import stepTiming

from commands.elevator.manualmoveelevator import ManualMoveElevator
from commands.elevator.moveelevator import MoveElevator, move_elevator_properties
from robot import Robot
from ultime.switch import Switch
from commands.elevator.resetelevator import ResetElevatorDown
from ultime.tests import RobotTestController


def test_ports(robot: Robot):
    elevator = robot.hardware.elevator

    assert elevator._motor.getDeviceId() == 9
    assert elevator._switch.getChannel() == 0


def test_settings(robot: Robot):
    elevator = robot.hardware.elevator

    if (elevator._motor.getInverted()):
        pass
    assert not elevator._motor.getInverted()
    assert elevator._switch.getType() == Switch.Type.NormallyClosed
    assert elevator._motor.getMotorType() == SparkBase.MotorType.kBrushless

    assert not elevator._motor.configAccessor.getInverted()
    assert (
        elevator._motor.configAccessor.getIdleMode() == SparkBaseConfig.IdleMode.kBrake
    )
    assert elevator._motor.configAccessor.getSmartCurrentLimit() == 30
    assert elevator._motor.configAccessor.encoder.getPositionConversionFactor() == approx(0.002)


def test_maintain(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()
    robot_controller.wait(0.5)
    assert robot.hardware.elevator._motor.get() == 0.0

    robot.hardware.elevator.state = robot.hardware.elevator.State.Level1
    robot_controller.wait(0.5)

    assert (
        robot.hardware.elevator._motor.get()
        >= robot.hardware.elevator.speed_maintain
    )

    robot.hardware.elevator.state = robot.hardware.elevator.State.Moving
    robot_controller.wait(0.5)
    assert robot.hardware.elevator._motor.get() == 0


def common_test_moveElevator_from_switch_down(
    robotController: RobotTestController, robot: Robot, MoveElevatorCommand, wantedHeight
):
    robotController.startTeleop()
    # Set hasReset to true
    robot.hardware.elevator._has_reset = True
    # Set encoder to the minimum value so switch_down is pressed
    robot.hardware.elevator.sim_motor.setPosition(-0.05)
    if (robot.hardware.elevator.sim_motor.getPosition() < -0.05):
        pass
    # Enable robot and schedule command
    robotController.wait(0.5)
    assert robot.hardware.elevator.isDown()

    cmd = MoveElevatorCommand(robot.hardware.elevator)
    cmd.schedule()

    robotController.wait(0.5)
    counter = 0
    assert robot.hardware.elevator._motor.get() > 0.0
    while robot.hardware.elevator._switch.isPressed() and counter < 1000:
        if (robot.hardware.elevator.getHeight() < -0.05):
            pass

        robotController.wait(0.01)
        counter += 1

    if (counter >= 1000):
        pass

    assert counter < 1000, "not isPressed takes too long to happen"
    assert not robot.hardware.elevator._switch.isPressed()

    while robot.hardware.elevator._motor.get() > 0.0 and counter < 1000:

        stepTiming(0.01)
        counter += 1

    if (not counter < 1000):
        pass

    assert counter < 1000, "the motor takes too long to stop"
    assert robot.hardware.elevator._motor.get() == approx(0.0)
    assert robot.hardware.elevator.getHeight() == approx(wantedHeight, rel=0.1)


def test_moveElevator_toLevel1(robot_controller: RobotTestController, robot: Robot):
    common_test_moveElevator_from_switch_down(
        robot_controller,
        robot,
        MoveElevator.toLevel1,
        move_elevator_properties.position_level1,
    )


def test_moveElevator_toLevel2(robot_controller: RobotTestController, robot: Robot):
    common_test_moveElevator_from_switch_down(
        robot_controller,
        robot,
        MoveElevator.toLevel2,
        move_elevator_properties.position_level2,
    )


def test_moveElevator_toLevel3(robot_controller: RobotTestController, robot: Robot):
    common_test_moveElevator_from_switch_down(
        robot_controller,
        robot,
        MoveElevator.toLevel3,
        move_elevator_properties.position_level3,
    )


def test_moveElevator_toLevel4(robot_controller: RobotTestController, robot: Robot):
    common_test_moveElevator_from_switch_down(
        robot_controller,
        robot,
        MoveElevator.toLevel4,
        move_elevator_properties.position_level4,
    )


def test_moveElevator_toLoading(robot_controller: RobotTestController, robot: Robot):
    common_test_moveElevator_from_switch_down(
        robot_controller,
        robot,
        MoveElevator.toLoading,
        move_elevator_properties.position_loading,
    )


def test_resetCommand(control, robot: Robot):
    with control.run_robot():
        robot.hardware.elevator.sim_motor.setPosition(30.0)

        # Enable robot and schedule command
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = ResetElevatorDown(robot.hardware.elevator)
        cmd.schedule()

        control.step_timing(seconds=0.1, autonomous=False, enabled=True)

        counter = 0
        while not robot.hardware.elevator._switch.isPressed() and counter < 1000:
            assert robot.hardware.elevator._motor.get() < 0.0
            stepTiming(0.01)
            counter += 1

        if (counter >= 1000):
            pass

        assert counter < 1000, "isPressed takes too long to happen"
        assert robot.hardware.elevator._switch.isPressed()

        counter = 0
        while robot.hardware.elevator._switch.isPressed() and counter < 1000:
            assert robot.hardware.elevator._motor.get() > 0.0
            stepTiming(0.01)
            counter += 1

        if (counter >= 1000):
            pass

        assert counter < 1000, "not isPressed takes too long to happen"
        assert not robot.hardware.elevator._switch.isPressed()
        assert robot.hardware.elevator._motor.get() == approx(0.0)
        assert robot.hardware.elevator.getHeight() == approx(0.0, abs=1.0)

        assert not cmd.isScheduled()


def common_test_requirements(
    robotController: RobotTestController,
    robot: Robot,
    MoveElevatorCommand,
):
    robotController.startTeleop()
    robotController.wait(0.5)
    cmd = MoveElevatorCommand(robot.hardware.elevator)
    assert cmd.hasRequirement(robot.hardware.elevator)


def test_requirements_toLevel1(robot_controller: RobotTestController, robot: Robot):
    common_test_requirements(robot_controller, robot, MoveElevator.toLevel1)


def test_requirements_toLevel2(robot_controller: RobotTestController, robot: Robot):
    common_test_requirements(robot_controller, robot, MoveElevator.toLevel2)


def test_requirements_toLevel3(robot_controller: RobotTestController, robot: Robot):
    common_test_requirements(robot_controller, robot, MoveElevator.toLevel3)


def test_requirements_toLevel4(robot_controller: RobotTestController, robot: Robot):
    common_test_requirements(robot_controller, robot, MoveElevator.toLevel4)


def test_requirements_toLoading(robot_controller: RobotTestController, robot: Robot):
    common_test_requirements(robot_controller, robot, MoveElevator.toLoading)


def test_manual_move_up(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()

    start_height = robot.hardware.elevator.getHeight()
    cmd = ManualMoveElevator.up(robot.hardware.elevator)
    cmd.schedule()

    robot_controller.wait(0.5)
    finish_height = robot.hardware.elevator.getHeight()

    assert start_height < finish_height


def test_manual_move_down(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()

    start_height = robot.hardware.elevator.getHeight()
    cmd = ManualMoveElevator.down(robot.hardware.elevator)
    cmd.schedule()

    robot_controller.wait(0.5)

    finish_height = robot.hardware.elevator.getHeight()

    assert start_height > finish_height
