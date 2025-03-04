from _pytest.python_api import approx

from commands.elevator.moveelevator import MoveElevator
from commands.prepareloading import PrepareLoading
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
    drivetrain = robot.hardware.drivetrain
    claw = robot.hardware.claw
    intake = robot.hardware.intake

    robot_controller.startTeleop()

    cmd_reset_all_but_climber = ResetAllButClimber(elevator, printer, arm, intake)
    cmd_reset_all_but_climber.schedule()
    robot_controller.wait_until(
        lambda: not cmd_reset_all_but_climber.isScheduled(), 10.0
    )

    cmd_move_elevator_to_loading = MoveElevator.toLoading(elevator)
    cmd_move_elevator_to_loading.schedule()
    robot_controller.wait_until(
        lambda: not cmd_move_elevator_to_loading.isScheduled(), 10.0
    )

    assert not claw.has_coral
    robot_controller.wait(0.02)

    cmd_move_elevator_to_level4 = MoveElevator.toLevel4(elevator)
    cmd_move_elevator_to_level4.schedule()
    robot_controller.wait(0.02)
    assert elevator._motor.get() == approx(elevator.speed_maintain)

    claw.has_coral = True
    robot_controller.wait(0.02)
    assert elevator._motor.get() > 0.0
    robot_controller.wait_until(
        lambda: not cmd_move_elevator_to_level4.isScheduled(), 10.0
    )

    cmd_prepare_loading = PrepareLoading(elevator, arm, printer)
    cmd_prepare_loading.schedule()
    robot_controller.wait_until(lambda: not cmd_prepare_loading.isScheduled(), 10.0)
    claw.has_coral = False

    robot_controller.wait(0.02)
    assert elevator.state == Elevator.State.Loading
    assert elevator._motor.get() == approx(0.0)

    claw.has_coral = True
    cmd_move_elevator_to_level4.schedule()
    robot_controller.wait(0.02)
    assert elevator._motor.get() > 0.0

    robot_controller.wait_until(
        lambda: not cmd_move_elevator_to_level4.isScheduled(), 10.0
    )
    assert elevator.state == Elevator.State.Level4
    assert elevator._motor.get() == approx(0.0)
