from _pytest.python_api import approx

from commands.arm.extendarm import ExtendArm
from commands.arm.retractarm import RetractArm
from commands.elevator.moveelevator import MoveElevator
from commands.elevator.resetelevator import ResetElevator
from commands.printer.moveprinter import MovePrinter
from commands.printer.resetright import ResetPrinterRight
from robot import Robot
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.tests import RobotTestController


def test_ports(robot: Robot):
    assert robot.hardware.arm._motor.getChannel() == 3


def test_settings(robot: Robot):
    arm = robot.hardware.arm
    assert not arm._motor.getInverted()


def test_RetractArm(robot_controller: RobotTestController, robot: Robot):
    arm = robot.hardware.arm
    elevator = robot.hardware.elevator
    printer = robot.hardware.printer

    arm.movement_state = Arm.MovementState.FreeToMove
    elevator.movement_state = Elevator.MovementState.FreeToMove
    printer.movement_state = Printer.MovementState.FreeToMove

    elevator.setHeight(elevator.height_lower_zone + 0.1)
    elevator._has_reset = True
    elevator.stop()
    printer.setPosition(printer.right)
    printer.stop()

    cmd = RetractArm(arm)
    sampling_time = cmd.delay * 0.5

    robot_controller.startTeleop()

    assert not cmd.isScheduled()
    assert arm._motor.get() == approx(0.0, rel=0.1)

    cmd.schedule()

    robot_controller.wait(cmd.delay - sampling_time)

    assert cmd.isScheduled()
    assert cmd.hasRequirement(arm)
    assert arm._motor.get() == approx(-arm.speed, rel=0.1)

    robot_controller.wait(sampling_time + 0.02)

    assert arm._motor.get() == approx(0.0)


def test_ExtendArm(robot_controller: RobotTestController, robot: Robot):
    arm = robot.hardware.arm
    elevator = robot.hardware.elevator
    printer = robot.hardware.printer

    arm.movement_state = Arm.MovementState.FreeToMove
    elevator.movement_state = Elevator.MovementState.FreeToMove
    printer.movement_state = Printer.MovementState.FreeToMove

    elevator.setHeight(elevator.height_lower_zone + 0.1)
    elevator._has_reset = True
    elevator.stop()
    printer.setPosition(printer.right)
    printer.stop()

    cmd = ExtendArm(arm)
    sampling_time = cmd.delay * 0.5

    robot_controller.startTeleop()

    assert not cmd.isScheduled()
    assert arm._motor.get() == approx(0.0, rel=0.1)

    cmd.schedule()

    robot_controller.wait(cmd.delay - sampling_time)

    assert arm._motor.get() == approx(arm.speed, rel=0.1)
    assert elevator.movement_state == Elevator.MovementState.AvoidLowerZone
    assert printer.movement_state == Printer.MovementState.AvoidMiddleZone
    assert cmd.isScheduled()
    assert cmd.hasRequirement(arm)

    robot_controller.wait(sampling_time + 0.02)

    assert arm._motor.get() == approx(0.0, rel=0.1)


def testRetractFailBadElevatorPosition(
    robot_controller: RobotTestController, robot: Robot
):

    class TestParameters:

        Cmd = RetractArm

        initial_arm_state = Arm.State.Extended
        initial_elevator_state = Elevator.State.Level1
        initial_printer_state = Printer.State.Unknown

        initial_arm_movement_state = Arm.MovementState.FreeToMove
        initial_elevator_movement_state = Elevator.MovementState.FreeToMove
        initial_printer_movement_state = Printer.MovementState.FreeToMove

        initial_arm_speed = 0.0

        initial_move_elevator_cmd = MoveElevator.toLoading

        initial_printer_pose = (
            robot.hardware.printer.middle_zone_right
            + robot.hardware.printer.middle_zone_left
        ) * 0.5
        initial_printer_function = Printer.stop

        initial_move_printer_cmd = MovePrinter.toMiddle

        running_arm_speed = 0.0
        running_arm_state = Arm.State.Extended
        running_elevator_state = Elevator.State.Loading
        running_printer_state = Printer.State.Middle

        end_arm_speed = 0.0

    _genericTest(robot_controller, robot, TestParameters)


def _genericTest(robot_controller: RobotTestController, robot: Robot, parameters):

    mega_delay = 10.0

    arm = robot.hardware.arm
    elevator = robot.hardware.elevator
    printer = robot.hardware.printer

    arm.movement_state = parameters.initial_arm_movement_state
    elevator.movement_state = parameters.initial_elevator_movement_state
    printer.movement_state = parameters.initial_printer_movement_state

    arm.state = parameters.initial_arm_state
    elevator.state = parameters.initial_elevator_state
    printer.state = parameters.initial_printer_state

    robot_controller.startTeleop()

    cmd_reset_elevator = ResetElevator(elevator)
    cmd_reset_elevator.schedule()
    robot_controller.wait(mega_delay)

    assert not cmd_reset_elevator.isScheduled()

    cmd_move_elevator = parameters.initial_move_elevator_cmd(elevator)
    cmd_move_elevator.schedule()
    robot_controller.wait(mega_delay)

    assert not cmd_move_elevator.isScheduled()

    cmd_reset_printer = ResetPrinterRight(printer)
    cmd_reset_printer.schedule()
    robot_controller.wait(mega_delay)

    assert not cmd_reset_printer.isScheduled()

    cmd_move_printer = parameters.initial_move_printer_cmd(printer)
    cmd_move_printer.schedule()
    robot_controller.wait(mega_delay)

    assert not cmd_move_printer.isScheduled()

    cmd = parameters.Cmd(arm)
    sampling_time = cmd.delay * 0.5

    assert not cmd.isScheduled()
    assert arm._motor.get() == approx(parameters.initial_arm_speed, rel=0.1)

    cmd.schedule()

    robot_controller.wait(cmd.delay - sampling_time)

    assert arm._motor.get() == approx(parameters.running_arm_speed, rel=0.1)
    assert arm.state == parameters.running_arm_state
    assert elevator.state == parameters.running_elevator_state
    assert printer.state == parameters.running_printer_state
    assert cmd.isScheduled()
    assert cmd.hasRequirement(arm)

    robot_controller.wait(sampling_time + 0.02)

    assert arm._motor.get() == approx(parameters.end_arm_speed, rel=0.1)
