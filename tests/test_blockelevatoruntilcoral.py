from _pytest.python_api import approx

from commands.elevator.moveelevator import MoveElevator
from commands.prepareloading import PrepareLoading
from commands.printer.moveprinter import MovePrinter
from commands.resetallbutclimber import ResetAllButClimber
from robot import Robot
from subsystems.elevator import Elevator
from ultime.tests import RobotTestController


def test_block_elevator_until_coral(
    robot_controller: RobotTestController, robot: Robot
):
    printer = robot.hardware.printer
    arm = robot.hardware.arm
    elevator = robot.hardware.elevator
    claw = robot.hardware.claw
    intake = robot.hardware.intake

    robot_controller.startTeleop()

    robot_controller.run_command(
        ResetAllButClimber(elevator, printer, arm, intake), 10.0
    )

    robot_controller.run_command(
        MoveElevator.toLoading(elevator), 10.0
    )

    robot_controller.run_command(
        MovePrinter.toLoading(printer), 10.0
    )

    assert not claw.has_coral

    claw._sensor.setSimPressed()
    robot_controller.wait_one_frame()

    assert robot.loading_detection.isLoading()
    robot_controller.wait_one_frame()

    assert elevator.loading_state == Elevator.LoadingState.DoNotMoveWhileLoading

    cmd_move_elevator_to_level4 = MoveElevator.toLevel4(elevator)
    cmd_move_elevator_to_level4.schedule()
    robot_controller.wait_one_frame()
    assert elevator._motor.get() == approx(elevator.speed_maintain)

    claw._sensor.setSimUnpressed()
    robot_controller.wait_one_frame()

    assert claw.has_coral
    robot_controller.wait_one_frame()

    assert elevator._motor.get() > 0.0
    robot_controller.wait_until(
        lambda: not cmd_move_elevator_to_level4.isScheduled(), 10.0
    )

    cmd_prepare_loading = PrepareLoading(elevator, arm, printer)
    cmd_prepare_loading.schedule()
    robot_controller.wait_until(lambda: not cmd_prepare_loading.isScheduled(), 10.0)
    claw.has_coral = False

    robot_controller.wait_one_frame()
    assert elevator.state == Elevator.State.Loading
    assert elevator._motor.get() == approx(0.0)

    claw.has_coral = True
    cmd_move_elevator_to_level4.schedule()
    robot_controller.wait_one_frame()
    assert elevator._motor.get() > 0.0

    robot_controller.wait_until(
        lambda: not cmd_move_elevator_to_level4.isScheduled(), 10.0
    )
    assert elevator.state == Elevator.State.Level4
    assert elevator._motor.get() == approx(0.0)
