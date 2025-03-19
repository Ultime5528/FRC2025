from _pytest.python_api import approx
from rev import SparkBase, SparkBaseConfig

from commands.arm.retractarm import RetractArm
from commands.elevator.manualmoveelevator import ManualMoveElevator
from commands.elevator.moveelevator import MoveElevator, move_elevator_properties
from commands.elevator.resetelevator import ResetElevator
from commands.resetallbutclimber import ResetAllButClimber
from robot import Robot
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.switch import Switch
from ultime.tests import RobotTestController
from ultime.tests.utils import robot_controller


def test_ports(robot: Robot):
    elevator = robot.hardware.elevator

    assert elevator._motor.getDeviceId() == 10
    assert elevator._switch.getChannel() == 6


def test_settings(robot: Robot):
    elevator = robot.hardware.elevator

    assert elevator._switch.getType() == Switch.Type.NormallyClosed

    assert not elevator._motor.getInverted()
    assert elevator._motor.getMotorType() == SparkBase.MotorType.kBrushless
    assert not elevator._motor.configAccessor.getInverted()
    assert (
        elevator._motor.configAccessor.getIdleMode() == SparkBaseConfig.IdleMode.kBrake
    )
    assert elevator._motor.configAccessor.getSmartCurrentLimit() == 30


def test_maintain(robot_controller: RobotTestController, robot: Robot):
    arm = robot.hardware.arm
    elevator = robot.hardware.elevator
    intake = robot.hardware.intake
    printer = robot.hardware.printer

    arm.movement_state = Arm.MovementState.FreeToMove
    elevator.movement_state = Elevator.MovementState.FreeToMove
    printer.movement_state = Printer.MovementState.FreeToMove

    robot_controller.startTeleop()

    cmd = ResetAllButClimber(elevator, printer, arm, intake)
    cmd.schedule()
    robot_controller.wait_until(lambda: not cmd.isScheduled(), 10.0)
    assert elevator.state == Elevator.State.Reset
    assert not elevator.hasReset()

    robot_controller.wait(0.02)
    assert elevator.state == Elevator.State.Reset
    assert elevator.hasReset()

    cmd = MoveElevator.toLevel1(elevator)
    cmd.schedule()
    robot_controller.wait_until(lambda: not cmd.isScheduled(), 10.0)
    assert elevator._motor.get() == approx(0.0)

    robot_controller.wait(0.02)
    assert elevator._motor.get() == approx(elevator.speed_maintain)

    cmd = ResetElevator(elevator)
    cmd.schedule()
    robot_controller.wait_until(lambda: not cmd.isScheduled(), 10.0)
    assert elevator._motor.get() == 0.0


def common_test_moveElevator_from_switch_down(
    robotController: RobotTestController,
    robot: Robot,
    MoveElevatorCommand,
    wantedHeight,
):
    arm = robot.hardware.arm
    elevator = robot.hardware.elevator
    printer = robot.hardware.printer

    robotController.startTeleop()

    robotController.run_command(
        ResetAllButClimber(elevator, printer, arm, robot.hardware.intake), 10.0
    )

    cmd = MoveElevatorCommand(elevator)
    cmd.schedule()

    robotController.wait(0.02)

    assert elevator.state == Elevator.State.Moving

    robotController.run_command(cmd, 10.0)
    robotController.wait(0.1)

    assert not elevator.state == Elevator.State.Moving
    if wantedHeight >= elevator.height_maintain:
        assert elevator._motor.get() == approx(
            elevator.speed_maintain
        )  # speed_maintain
    else:
        assert elevator._motor.get() == 0.0
    assert elevator.getHeight() == approx(wantedHeight, abs=0.05)


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


def test_moveElevator_toLevel2Algae(
    robot_controller: RobotTestController, robot: Robot
):
    common_test_moveElevator_from_switch_down(
        robot_controller,
        robot,
        MoveElevator.toLevel2Algae,
        move_elevator_properties.position_level2_algae,
    )


def test_moveElevator_toLevel3(robot_controller: RobotTestController, robot: Robot):
    common_test_moveElevator_from_switch_down(
        robot_controller,
        robot,
        MoveElevator.toLevel3,
        move_elevator_properties.position_level3,
    )


def test_moveElevator_toLevel3Algae(
    robot_controller: RobotTestController, robot: Robot
):
    common_test_moveElevator_from_switch_down(
        robot_controller,
        robot,
        MoveElevator.toLevel3Algae,
        move_elevator_properties.position_level3_algae,
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


def test_resetCommand(robot_controller: RobotTestController, robot: Robot):
    arm = robot.hardware.arm
    elevator = robot.hardware.elevator

    robot_controller.startTeleop()

    # Retract Arm so the elevator is free to move
    cmd = RetractArm(arm)
    cmd.schedule()
    robot_controller.wait_until(lambda: not cmd.isScheduled(), 5.0)

    cmd = ResetElevator(elevator)
    cmd.schedule()
    robot_controller.wait(0.02)

    assert elevator._motor.get() < 0.0

    robot_controller.wait_until(lambda: elevator.isDown(), 5.0, delta=0.02)

    assert elevator._switch.isPressed()
    assert elevator._motor.get() > 0.0

    robot_controller.wait_until(lambda: not elevator.isDown(), 5.0, delta=0.02)

    assert not elevator._switch.isPressed()

    robot_controller.wait(0.05)

    assert not cmd.isScheduled()
    assert elevator._motor.get() == approx(0.0)
    assert elevator.getHeight() == approx(0.0, abs=0.02)


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


def test_requirements_toLevel2Algae(
    robot_controller: RobotTestController, robot: Robot
):
    common_test_requirements(robot_controller, robot, MoveElevator.toLevel2Algae)


def test_requirements_toLevel3(robot_controller: RobotTestController, robot: Robot):
    common_test_requirements(robot_controller, robot, MoveElevator.toLevel3)


def test_requirements_toLevel3Algae(
    robot_controller: RobotTestController, robot: Robot
):
    common_test_requirements(robot_controller, robot, MoveElevator.toLevel3Algae)


def test_requirements_toLevel4(robot_controller: RobotTestController, robot: Robot):
    common_test_requirements(robot_controller, robot, MoveElevator.toLevel4)


def test_requirements_toLoading(robot_controller: RobotTestController, robot: Robot):
    common_test_requirements(robot_controller, robot, MoveElevator.toLoading)


def test_manual_move_up(robot_controller: RobotTestController, robot: Robot):

    arm = robot.hardware.arm
    elevator = robot.hardware.elevator
    printer = robot.hardware.printer

    arm.movement_state = Arm.MovementState.FreeToMove
    elevator.movement_state = Elevator.MovementState.FreeToMove
    printer.movement_state = Printer.MovementState.FreeToMove

    arm.state = Arm.State.Retracted

    robot_controller.startTeleop()

    start_height = elevator.getHeight()
    cmd = ManualMoveElevator.up(robot.hardware.elevator)
    cmd.schedule()

    robot_controller.wait(0.5)
    finish_height = elevator.getHeight()

    assert start_height < finish_height


def test_manual_move_down(robot_controller: RobotTestController, robot: Robot):

    arm = robot.hardware.arm
    elevator = robot.hardware.elevator
    printer = robot.hardware.printer

    arm.movement_state = Arm.MovementState.FreeToMove
    elevator.movement_state = Elevator.MovementState.FreeToMove
    printer.movement_state = Printer.MovementState.FreeToMove

    arm.state = Arm.State.Retracted

    robot_controller.startTeleop()

    start_height = elevator.getHeight()
    cmd = ManualMoveElevator.down(robot.hardware.elevator)
    cmd.schedule()

    robot_controller.wait(0.5)

    finish_height = elevator.getHeight()

    assert start_height > finish_height

    elevator._switch.setSimPressed()

    robot_controller.wait(0.5)

    assert elevator.getMotorInput() == 0.0
