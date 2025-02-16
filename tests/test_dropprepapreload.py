from commands.printer.resetright import ResetPrinterRight

from commands.arm.extendarm import ExtendArm
from commands.arm.retractarm import RetractArm
from commands.dropprepareload import DropPrepareLoad
from commands.elevator.moveelevator import MoveElevator
from commands.elevator.resetelevator import ResetElevator
from commands.printer.moveprinter import MovePrinter
from robot import Robot
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.tests import RobotTestController


def commun_test_drop_prepareLoad(
    robot_controller: RobotTestController,
    robot: Robot,
    side: str,
    extended: bool,
    elevator_starting_level: int,
):

    mega_delay = 10.0

    arm = robot.hardware.arm
    claw = robot.hardware.claw
    drivetrain = robot.hardware.drivetrain
    elevator = robot.hardware.elevator
    printer = robot.hardware.printer

    robot_controller.startTeleop()

    cmd_retract_arm = RetractArm(arm)
    cmd_retract_arm.schedule()
    robot_controller.wait(mega_delay)

    assert not cmd_retract_arm.isScheduled()

    cmd_reset_elevator = ResetElevator(elevator)
    cmd_reset_elevator.schedule()
    robot_controller.wait(mega_delay)

    assert not cmd_reset_elevator.isScheduled()

    if elevator_starting_level == 1:
        cmd_move_elevator = MoveElevator.toLevel1(elevator)
    elif elevator_starting_level == 2:
        cmd_move_elevator = MoveElevator.toLevel2(elevator)
    elif elevator_starting_level == 3:
        cmd_move_elevator = MoveElevator.toLevel3(elevator)
    else:
        cmd_move_elevator = MoveElevator.toLevel4(elevator)

    cmd_move_elevator.schedule()
    robot_controller.wait(mega_delay)

    assert not cmd_move_elevator.isScheduled()

    cmd_reset_printer = ResetPrinterRight(printer)
    cmd_reset_printer.schedule()
    robot_controller.wait(mega_delay)

    assert not cmd_reset_printer.isScheduled()
    ###all reset done

    if side == "Left":
        cmd_move_printer = MovePrinter.toLeft(printer)
    elif side == "Right":
        cmd_move_printer = MovePrinter.toRight(printer)
    else:
        raise RuntimeError

    cmd_move_printer.schedule()
    robot_controller.wait(mega_delay)

    assert not cmd_move_printer.isScheduled()

    if extended:
        cmd_extend_arm = ExtendArm(arm)
    else:
        cmd_extend_arm = RetractArm(arm)
    cmd_extend_arm.schedule()
    robot_controller.wait(mega_delay)

    assert not cmd_extend_arm.isScheduled()

    cmd = DropPrepareLoad.left(arm, claw, drivetrain, elevator, printer)

    assert not cmd.isScheduled()

    cmd.schedule()

    assert cmd.isScheduled()

    robot_controller.wait_until(lambda: not cmd.isScheduled(), 10.0)

    assert not cmd.isScheduled()

    if extended:
        assert arm.state == Arm.State.Extended
    else:
        assert arm.state == Arm.State.Retracted

    assert printer.state == Printer.State.Unknown

    if elevator_starting_level == 1:
        assert elevator.state == Elevator.State.Level1
    elif elevator_starting_level == 2:
        assert elevator.state == Elevator.State.Level2
    elif elevator_starting_level == 3 and extended:
        assert elevator.state == Elevator.State.Level2Algae
    elif elevator_starting_level == 3 and not extended:
        assert elevator.state == Elevator.State.Level3
    elif elevator_starting_level == 4 and extended:
        assert elevator.state == Elevator.State.Level3Algae
    elif elevator_starting_level == 4 and not extended:
        assert elevator.state == Elevator.State.Level4
    assert claw._motor_right.get() == 0.0
    assert claw._motor_left.get() == 0.0


def test_left_extended_4(robot_controller: RobotTestController, robot: Robot):
    list_level = [1, 2, 3, 4]
    list_side = ["Left", "Right"]
    list_extend = [True, False]

    for level in list_level:
        for side in list_side:
            for extended in list_extend:
                commun_test_drop_prepareLoad(
                    robot_controller, robot, side, extended, level
                )
