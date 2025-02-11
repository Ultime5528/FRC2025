from _pytest.python_api import approx
from commands2 import Command

from commands.arm.extendarm import ExtendArm, arm_properties
from commands.arm.retractarm import RetractArm
from robot import Robot
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.tests import RobotTestController


def test_ports(robot: Robot):
    assert robot.hardware.arm._motor.getChannel() == 2


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
    printer.setPose(printer.right)
    printer.stop()

    sampling_time = arm_properties.delay * 0.5

    robot_controller.startTeleop()

    cmd = RetractArm(arm)
    assert not cmd.isScheduled()
    assert arm._motor.get() == approx(0.0, rel=0.1)

    cmd.schedule()

    robot_controller.wait(arm_properties.delay - sampling_time)

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
    printer.setPose(printer.right)
    printer.stop()

    sampling_time = arm_properties.delay * 0.5

    robot_controller.startTeleop()

    cmd = ExtendArm(arm)

    assert not cmd.isScheduled()
    assert arm._motor.get() == approx(0.0, rel=0.1)

    cmd.schedule()

    robot_controller.wait(arm_properties.delay - sampling_time)

    assert arm._motor.get() == approx(arm.speed, rel=0.1)
    assert elevator.movement_state == Elevator.MovementState.AvoidLowerZone
    assert printer.movement_state == Printer.MovementState.AvoidMiddleZone
    assert cmd.isScheduled()
    assert cmd.hasRequirement(arm)

    robot_controller.wait(sampling_time + 0.02)

    assert arm._motor.get() == 0.0


def testRetractFailBadElevatorPosition(
    robot_controller: RobotTestController, robot: Robot
):
    _testFail(
        robot_controller,
        robot,
        RetractArm(robot.hardware.arm),
        robot.hardware.elevator.height_lower_zone + 0.1,
        Elevator.MovementState.AvoidLowerZone,
        (robot.hardware.printer.right_zone + robot.hardware.printer.left_zone) * 0.5,
        Printer.MovementState.FreeToMove,
    )


def testRetractFailBadPrinterPosition(
    robot_controller: RobotTestController, robot: Robot
):
    _testFail(
        robot_controller,
        robot,
        RetractArm(robot.hardware.arm),
        robot.hardware.elevator.height_lower_zone - 0.1,
        Elevator.MovementState.AvoidLowerZone,
        robot.hardware.printer.right_zone,
        Printer.MovementState.FreeToMove,
    )

def testExtendFailBadElevatorPosition(
    robot_controller: RobotTestController, robot: Robot
):
    _testFail(
        robot_controller,
        robot,
        ExtendArm(robot.hardware.arm),
        robot.hardware.elevator.height_lower_zone + 0.1,
        Elevator.MovementState.AvoidLowerZone,
        (robot.hardware.printer.right_zone + robot.hardware.printer.left_zone) * 0.5,
        Printer.MovementState.FreeToMove,
    )


def testExtendFailBadPrinterPosition(
    robot_controller: RobotTestController, robot: Robot
):
    _testFail(
        robot_controller,
        robot,
        ExtendArm(robot.hardware.arm),
        robot.hardware.elevator.height_lower_zone - 0.1,
        Elevator.MovementState.AvoidLowerZone,
        robot.hardware.printer.right_zone,
        Printer.MovementState.FreeToMove,
    )

def _testFail(
    robot_controller: RobotTestController,
    robot: Robot,
    cmd: Command,
    elevator_height: float,
    elevator_movement_state: Elevator.MovementState,
    printer_pose: float,
    printer_movement_state: Printer.MovementState,
):

    arm = robot.hardware.arm
    elevator = robot.hardware.elevator
    printer = robot.hardware.printer

    arm.movement_state = Arm.MovementState.FreeToMove
    elevator.movement_state = Elevator.MovementState.FreeToMove
    printer.movement_state = Printer.MovementState.FreeToMove

    arm.state = Arm.State.Extended
    elevator.setHeight(elevator_height)
    elevator._has_reset = True
    elevator.stop()
    printer.setPose(printer_pose)
    printer.stop()

    sampling_time = arm_properties.delay * 0.5

    robot_controller.startTeleop()

    assert not cmd.isScheduled()
    assert arm._motor.get() == approx(0.0, rel=0.1)

    cmd.schedule()

    robot_controller.wait(arm_properties.delay - sampling_time)

    assert arm._motor.get() == approx(0.0, rel=0.1)
    assert not arm.state == Arm.State.Moving
    assert elevator.movement_state == elevator_movement_state
    assert printer.movement_state == printer_movement_state
    assert cmd.isScheduled()
    assert cmd.hasRequirement(arm)

    robot_controller.wait(sampling_time + 0.02)

    assert arm._motor.get() == approx(0.0, rel=0.1)
