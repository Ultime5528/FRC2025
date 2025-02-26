from _pytest.python_api import approx

from commands.arm.extendarm import ExtendArm
from commands.arm.retractarm import RetractArm
from commands.elevator.moveelevator import MoveElevator
from commands.printer.moveprinter import MovePrinter
from commands.resetall import ResetAll
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

    assert not cmd.isScheduled()
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

    assert not cmd.isScheduled()
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

        running_arm_speed = lambda arm: 0.0
        running_elevator_cmd = None
        running_printer_cmd = None
        running_arm_state = Arm.State.Extended

        def running_arm_moving_condition(arm: Arm) -> bool:
            return True

        running_elevator_state = Elevator.State.Loading

        def running_printer_state(printer: Printer):
            return printer.state == Printer.State.Middle

        end_arm_speed = 0.0
        end_arm_state = Arm.State.Extended

    _genericTest(robot_controller, robot, TestParameters)


def testRetractFailBadPrinterPosition(
    robot_controller: RobotTestController, robot: Robot
):

    class TestParameters:

        Cmd = RetractArm

        initial_arm_state = Arm.State.Extended
        initial_elevator_state = Elevator.State.Level1
        initial_printer_state = Printer.State.Middle

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

        running_arm_speed = lambda arm: 0.0
        running_elevator_cmd = None
        running_printer_cmd = None
        running_arm_state = Arm.State.Extended

        def running_arm_moving_condition(arm: Arm) -> bool:
            return True

        running_elevator_state = Elevator.State.Loading

        def running_printer_state(printer: Printer):
            return printer.state == Printer.State.Middle

        end_arm_speed = 0.0
        end_arm_state = Arm.State.Extended

    _genericTest(robot_controller, robot, TestParameters)


def testRetractSucessGoodElevatorPosition(
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

        running_arm_speed = lambda arm: -arm.speed
        running_elevator_cmd = None
        running_printer_cmd = MovePrinter.toLeft
        running_arm_state = Arm.State.Moving

        def running_arm_moving_condition(arm: Arm) -> bool:
            return arm.movement_state == Arm.MovementState.FreeToMove

        running_elevator_state = Elevator.State.Loading

        def running_printer_state(printer: Printer):
            return (
                printer.state == Printer.State.Moving
                or printer.state == Printer.State.Left
            )

        end_arm_speed = 0.0
        end_arm_state = Arm.State.Retracted

    _genericTest(robot_controller, robot, TestParameters)


def testRetractSucessGoodPrinterPosition(
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

        initial_printer_pose = robot.hardware.printer.middle_zone_right
        initial_printer_function = Printer.stop

        initial_move_printer_cmd = MovePrinter.toRight

        running_arm_speed = lambda arm: -arm.speed
        running_elevator_cmd = MoveElevator.toLevel4
        running_printer_cmd = MovePrinter.toRight
        running_arm_state = Arm.State.Moving

        def running_arm_moving_condition(arm: Arm) -> bool:
            return arm.movement_state == Arm.MovementState.FreeToMove

        running_elevator_state = Elevator.State.Moving

        def running_printer_state(printer: Printer):
            return printer.state == Printer.State.Right

        end_arm_speed = 0.0
        end_arm_state = Arm.State.Retracted

    _genericTest(robot_controller, robot, TestParameters)


def _genericTest(robot_controller: RobotTestController, robot: Robot, parameters):

    mega_delay = 10.0

    arm = robot.hardware.arm
    elevator = robot.hardware.elevator
    printer = robot.hardware.printer

    robot_controller.startTeleop()

    reset_all_cmd = ResetAll(
        elevator, printer, arm, robot.hardware.intake, robot.hardware.climber
    )
    reset_all_cmd.schedule()
    robot_controller.wait_until(lambda: not reset_all_cmd.isScheduled(), 30.0)

    if parameters.initial_arm_state == Arm.State.Extended:
        clear_elevator_cmd = MoveElevator.toLevel1(elevator)
        clear_elevator_cmd.schedule()
        robot_controller.wait_until(lambda: not clear_elevator_cmd.isScheduled(), 10.0)

        extend_arm_cmd = ExtendArm(arm)
        extend_arm_cmd.schedule()
        robot_controller.wait_until(lambda: not extend_arm_cmd.isScheduled(), 10.0)

    # cmd_reset_elevator = ResetElevator(elevator)
    # cmd_reset_elevator.schedule()
    # robot_controller.wait_until(lambda: not cmd_reset_elevator.isScheduled(), mega_delay)
    #
    # cmd_move_elevator = parameters.initial_move_elevator_cmd(elevator)
    # cmd_move_elevator.schedule()
    # robot_controller.wait_until(lambda: not cmd_move_elevator.isScheduled(), mega_delay)
    #
    # cmd_reset_printer = ResetPrinterRight(printer)
    # cmd_reset_printer.schedule()
    # robot_controller.wait_until(lambda: not cmd_reset_printer.isScheduled(), mega_delay)

    cmd_move_printer = parameters.initial_move_printer_cmd(printer)
    cmd_move_printer.schedule()
    robot_controller.wait_until(lambda: not cmd_move_printer.isScheduled(), mega_delay)

    cmd = parameters.Cmd(arm)
    sampling_time = cmd.delay * 0.5

    assert not cmd.isScheduled()
    assert arm._motor.get() == approx(parameters.initial_arm_speed, rel=0.1)

    if parameters.running_printer_cmd != None:
        running_printer_cmd = parameters.running_printer_cmd(printer)
        running_printer_cmd.schedule()

    if parameters.running_elevator_cmd != None:
        running_elevator_cmd = parameters.running_elevator_cmd(elevator)
        running_elevator_cmd.schedule()

    cmd.schedule()

    robot_controller.wait_until(
        lambda: parameters.running_arm_moving_condition(arm), mega_delay
    )

    robot_controller.wait(0.1)
    # robot_controller.wait(cmd.delay - sampling_time)

    assert arm._motor.get() == approx(parameters.running_arm_speed(arm), rel=0.1)
    assert arm.state == parameters.running_arm_state
    assert parameters.running_printer_state(printer)
    assert cmd.isScheduled()
    assert cmd.hasRequirement(arm)

    robot_controller.wait(mega_delay)

    assert arm._motor.get() == approx(parameters.end_arm_speed, rel=0.1)
    assert arm.state == parameters.end_arm_state
