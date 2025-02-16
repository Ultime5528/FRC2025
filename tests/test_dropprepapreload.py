import pytest

from commands.arm.extendarm import ExtendArm
from commands.arm.retractarm import RetractArm
from commands.claw.autodrop import AutoDrop
from commands.dropprepareload import DropPrepareLoad
from commands.elevator.moveelevator import MoveElevator
from commands.elevator.resetelevator import ResetElevator
from commands.printer.moveprinter import MovePrinter
from commands.printer.resetright import ResetPrinterRight
from robot import Robot
from subsystems.arm import Arm
from subsystems.drivetrain import Drivetrain
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.tests import RobotTestController

@pytest.mark.specific
def testDropPrepareLoadLeftWithExtendedArmToLevel4(robot_controller: RobotTestController, robot: Robot):

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

    cmd_move_elevator = MoveElevator.toLevel4(elevator)
    cmd_move_elevator.schedule()
    robot_controller.wait(mega_delay)

    assert not cmd_move_elevator.isScheduled()

    cmd_reset_printer = ResetPrinterRight(printer)
    cmd_reset_printer.schedule()
    robot_controller.wait(mega_delay)

    assert not cmd_reset_printer.isScheduled()

    cmd_move_printer = MovePrinter.toLeft(printer)
    cmd_move_printer.schedule()
    robot_controller.wait(mega_delay)

    assert not cmd_move_printer.isScheduled()

    cmd_extend_arm = ExtendArm(arm)
    cmd_extend_arm.schedule()
    robot_controller.wait(mega_delay)

    assert not cmd_extend_arm.isScheduled()

    cmd = DropPrepareLoad.left(arm, claw, drivetrain, elevator, printer)

    assert not cmd.isScheduled()

    cmd.schedule()

    assert cmd.isScheduled()

    robot_controller.wait_until(lambda: not cmd.isScheduled(), 10.0)

    assert not cmd.isScheduled()
    assert arm.state == Arm.State.Extended
    assert printer.state == Printer.State.Unknown
    assert elevator.state == Elevator.State.Level3Algae
    assert claw._motor_right.get() == 0.0
    assert claw._motor_left.get() == 0.0
