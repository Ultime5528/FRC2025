from commands.arm.extendarm import ExtendArm
from commands.dropprepareloading import DropPrepareLoading
from commands.elevator.moveelevator import MoveElevator, move_elevator_properties
from commands.printer.moveprinter import MovePrinter
from commands.resetall import ResetAll
from robot import Robot
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.tests import RobotTestController


def commun_test_drop_prepare_load(
    robot_controller: RobotTestController,
    robot: Robot,
    side: str,
    extended: bool,
    elevator_starting_level: int,
):

    arm = robot.hardware.arm
    claw = robot.hardware.claw
    climber = robot.hardware.climber
    drivetrain = robot.hardware.drivetrain
    elevator = robot.hardware.elevator
    intake = robot.hardware.intake
    printer = robot.hardware.printer

    robot_controller.startTeleop()

    cmd_reset_all = ResetAll(elevator, printer, arm, intake, climber)
    cmd_reset_all.schedule()
    robot_controller.wait_until(lambda: not cmd_reset_all.isScheduled(), 10.0)

    assert move_elevator_properties.position_level2 > elevator.height_lower_zone
    cmd_move_elevator_for_arm = MoveElevator.toLevel2(elevator)
    cmd_move_elevator_for_arm.schedule()
    robot_controller.wait_until(
        lambda: not cmd_move_elevator_for_arm.isScheduled(), 10.0
    )

    if extended:
        cmd_extend_arm = ExtendArm(arm)
        cmd_extend_arm.schedule()
        robot_controller.wait_until(lambda: not cmd_extend_arm.isScheduled(), 10.0)

    if elevator_starting_level == 1:
        cmd_move_elevator = MoveElevator.toLevel1(elevator)
    elif elevator_starting_level == 2:
        cmd_move_elevator = MoveElevator.toLevel2(elevator)
    elif elevator_starting_level == 3:
        cmd_move_elevator = MoveElevator.toLevel3(elevator)
    else:
        cmd_move_elevator = MoveElevator.toLevel4(elevator)

    cmd_move_elevator.schedule()
    robot_controller.wait_until(lambda: not cmd_move_elevator.isScheduled(), 10.0)

    if side == "Left":
        cmd_move_printer = MovePrinter.toLeft(printer)
    elif side == "Right":
        cmd_move_printer = MovePrinter.toRight(printer)
    else:
        raise RuntimeError
    cmd_move_printer.schedule()
    robot_controller.wait_until(lambda: not cmd_move_printer.isScheduled(), 10.0)

    cmd_drop_prepare_loading = DropPrepareLoading.left(
        arm, claw, drivetrain, elevator, printer
    )

    assert not cmd_drop_prepare_loading.isScheduled()

    cmd_drop_prepare_loading.schedule()

    assert cmd_drop_prepare_loading.isScheduled()

    robot_controller.wait_until(
        lambda: not cmd_drop_prepare_loading.isScheduled(), 10.0
    )

    assert arm.state == Arm.State.Retracted
    assert printer.state == Printer.State.Loading
    assert elevator.state == Elevator.State.Loading
    assert claw._motor_right.get() == 0.0
    assert claw._motor_left.get() == 0.0


def test_left_extended_4(robot_controller: RobotTestController, robot: Robot):
    list_level = [2, 3, 4]
    list_side = ["Left", "Right"]
    extended = True
    for level in list_level:
        for side in list_side:
            commun_test_drop_prepare_load(
                robot_controller, robot, side, extended, level
            )

    list_level = [1, 2, 3, 4]
    list_side = ["Left", "Right"]
    extended = False
    for level in list_level:
        for side in list_side:
            commun_test_drop_prepare_load(
                robot_controller, robot, side, extended, level
            )
