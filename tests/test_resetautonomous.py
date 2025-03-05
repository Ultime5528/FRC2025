from commands.dropprepareloading import DropPrepareLoading
from commands.resetautonomous import ResetAutonomous
from robot import Robot
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.tests import RobotTestController


def test_resetautonomous(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()
    elevator = robot.hardware.elevator
    printer = robot.hardware.printer
    arm = robot.hardware.arm
    drivetrain = robot.hardware.drivetrain
    claw = robot.hardware.claw

    reset_cmd = ResetAutonomous(
        elevator, printer, arm, robot.hardware.intake, robot.hardware.climber
    )
    reset_cmd.schedule()

    robot_controller.wait_until(lambda: not reset_cmd.isScheduled(), 10.0)

    assert elevator.state == Elevator.State.Reset
    assert elevator.movement_state == Elevator.MovementState.FreeToMove
    assert printer.state == Printer.State.Reset
    assert arm.state == Arm.State.Retracted
    assert arm.movement_state == Arm.MovementState.DoNotMove
    assert robot.hardware.intake.state == robot.hardware.intake.State.Retracted
    assert robot.hardware.climber.state == robot.hardware.climber.State.Initial

    elevator.state = Elevator.State.Level3
    arm.state = Arm.State.Extended

    cmd = DropPrepareLoading.toLeft(printer, arm, elevator, drivetrain, claw)
    cmd.schedule()

    robot_controller.wait(1.0)

    robot_controller.wait_until(lambda: not cmd.isScheduled(), 10.0)

    assert elevator.state == Elevator.State.Loading
    assert printer.state == Printer.State.Loading
    assert arm.state == arm.State.Retracted
