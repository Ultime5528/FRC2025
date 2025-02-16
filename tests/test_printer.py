from _pytest.python_api import approx
from wpilib.simulation import stepTiming

from commands.arm.retractarm import RetractArm
from commands.printer.moveprinter import MovePrinter, move_printer_properties
from commands.printer.resetright import ResetPrinterRight
from robot import Robot
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.switch import Switch
from ultime.tests import RobotTestController


def test_ports(robot: Robot):
    printer = robot.hardware.printer

    assert printer._motor.getChannel() == 2
    assert printer._switch_left.getChannel() == 2
    assert printer._switch_right.getChannel() == 3


def test_settings(robot: Robot):

    printer = robot.hardware.printer

    assert printer._motor.getInverted()
    assert printer._switch_left.getType() == Switch.Type.NormallyClosed
    assert printer._switch_right.getType() == Switch.Type.NormallyClosed


def test_reset_right(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()

    arm = robot.hardware.arm
    elevator = robot.hardware.elevator
    printer = robot.hardware.printer

    arm.movement_state = Arm.MovementState.FreeToMove
    elevator.movement_state = Elevator.MovementState.FreeToMove
    printer.movement_state = Printer.MovementState.FreeToMove

    arm.state = Arm.State.Retracted

    printer._sim_encoder.setDistance(0.5)

    # Enable robot and schedule command
    robot_controller.wait(0.5)
    cmd = ResetPrinterRight(printer)
    cmd.schedule()

    robot_controller.wait(0.01)

    counter = 0
    while not printer._switch_right.isPressed() and counter < 1000:
        assert printer._motor.get() < 0.0
        stepTiming(0.01)
        counter += 1

    assert counter < 1000, "isPressed takes too long to happen"
    assert printer._switch_right.isPressed()

    counter = 0
    while printer._switch_right.isPressed() and counter < 1000:
        assert printer._motor.get() > 0.0
        stepTiming(0.01)
        counter += 1

    assert counter < 1000, "not isPressed takes too long to happen"
    assert not printer._switch_right.isPressed()

    robot_controller.wait(1.0)

    assert printer._motor.get() == approx(0.0)
    assert printer.getPosition() == approx(0.0, abs=1.0)

    assert not cmd.isScheduled()


def common_test_movePrinter_from_switch_right(
    robotController: RobotTestController,
    robot: Robot,
    MovePrinterCommand,
    wantedHeight,
):
    robotController.startTeleop()
    # Set hasReset to true
    robot.hardware.printer._has_reset = True
    # Set encoder to the minimum value so switch_down is pressed
    robot.hardware.printer.setPosition(-0.05)
    robot.hardware.printer._sim_position = -0.05
    # Enable robot and schedule command
    robotController.wait(0.5)
    assert robot.hardware.printer.isRight()

    cmd = RetractArm(robot.hardware.arm)
    cmd.schedule()

    robotController.wait(10)

    cmd = MovePrinterCommand(robot.hardware.printer)
    cmd.schedule()

    robotController.wait(0.05)

    assert robot.hardware.printer._motor.get() > 0.0

    robotController.wait(10)

    assert not robot.hardware.printer._switch_right.isPressed()

    robotController.wait(20)

    assert robot.hardware.printer._motor.get() == approx(0.0)
    assert robot.hardware.printer.getPosition() == approx(wantedHeight, abs=0.05)


def test_movePrinter_toLeft(robot_controller: RobotTestController, robot: Robot):
    common_test_movePrinter_from_switch_right(
        robot_controller,
        robot,
        MovePrinter.toLeft,
        move_printer_properties.position_left,
    )


def test_moveElevator_toMiddle(robot_controller: RobotTestController, robot: Robot):
    common_test_movePrinter_from_switch_right(
        robot_controller,
        robot,
        MovePrinter.toMiddle,
        move_printer_properties.position_middle,
    )


def test_movePrinter_toLoading(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()

    cmd = RetractArm(robot.hardware.arm)
    cmd.schedule()
    # Set hasReset to true
    robot.hardware.printer._has_reset = True
    # Set printer in the middle
    cmd = MovePrinter.toMiddle(robot.hardware.printer)
    cmd.schedule()
    # Enable robot and schedule command
    robot_controller.wait(10)

    assert robot.hardware.printer.state == robot.hardware.printer.State.Middle

    cmd = MovePrinter.toLoading(robot.hardware.printer)
    cmd.schedule()

    robot_controller.wait(0.05)

    assert robot.hardware.printer._motor.get() < 0.0

    robot_controller.wait(10)

    assert not robot.hardware.printer._switch_right.isPressed()

    robot_controller.wait(20)

    assert robot.hardware.printer._motor.get() == approx(0.0)
    assert robot.hardware.printer.getPosition() == approx(0.05, rel=0.005)


def test_movePrinter_toRight(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()

    cmd = RetractArm(robot.hardware.arm)
    cmd.schedule()
    # Set hasReset to true
    robot.hardware.printer._has_reset = True
    # Set printer in the middle
    cmd = MovePrinter.toMiddle(robot.hardware.printer)
    cmd.schedule()
    # Enable robot and schedule command
    robot_controller.wait(10)

    assert robot.hardware.printer.state == robot.hardware.printer.State.Middle

    cmd = MovePrinter.toRight(robot.hardware.printer)
    cmd.schedule()

    robot_controller.wait(0.05)

    assert robot.hardware.printer._motor.get() < 0.0

    robot_controller.wait(10)

    assert not robot.hardware.printer._switch_right.isPressed()

    robot_controller.wait(20)

    assert robot.hardware.printer._motor.get() == approx(0.0)
    assert robot.hardware.printer.getPosition() == approx(0.0, abs=0.005)


def test_move_printer_leftUntilReef(
    robot_controller: RobotTestController, robot: Robot
):
    robot_controller.startTeleop()

    cmd = RetractArm(robot.hardware.arm)
    cmd.schedule()

    robot_controller.wait(10)

    robot.hardware.printer._has_reset = True

    robot_controller.wait(10)

    cmd = ResetPrinterRight(robot.hardware.printer)
    cmd.schedule()

    robot_controller.wait(10)

    cmd = MovePrinter.toLeft(robot.hardware.printer)
    cmd.schedule()

    robot_controller.wait(10)

    assert robot.hardware.printer.state == robot.hardware.printer.State.Left

    cmd = MovePrinter.leftUntilReef(robot.hardware.printer)
    cmd.schedule()

    robot_controller.wait(0.5)

    count = 0
    while robot.hardware.printer._motor.get() < 0 and count < 1000:
        robot_controller.wait(0.01)
        count += 1

    robot_controller.wait(0.01)

    robot.hardware.printer.photocell.setSimPressed()

    robot_controller.wait(1)

    assert robot.hardware.printer._motor.get() == approx(0.0)


def test_move_printer_rightUntilReef(
    robot_controller: RobotTestController, robot: Robot
):
    robot_controller.startTeleop()

    cmd = RetractArm(robot.hardware.arm)
    cmd.schedule()

    robot_controller.wait(10)

    assert not cmd.isScheduled()

    robot.hardware.printer._has_reset = True

    cmd = MovePrinter.toRight(robot.hardware.printer)
    cmd.schedule()

    robot_controller.wait(10)

    assert robot.hardware.printer.state == robot.hardware.printer.State.Right

    cmd = MovePrinter.rightUntilReef(robot.hardware.printer)
    cmd.schedule()

    robot_controller.wait(0.5)

    count = 0
    while robot.hardware.printer._motor.get() > 0 and count < 1000:
        robot_controller.wait(0.01)
        count += 1

    robot_controller.wait(0.01)

    robot.hardware.printer.photocell.setSimPressed()

    robot_controller.wait(1)

    assert robot.hardware.printer._motor.get() == approx(0.0)
