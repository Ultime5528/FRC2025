from commands.dropprepareloading import DropPrepareLoading
from commands.resetautonomous import ResetAutonomous
from robot import Robot
from subsystems.arm import Arm
from subsystems.climber import Climber
from subsystems.elevator import Elevator
from subsystems.intake import Intake
from subsystems.printer import Printer
from ultime.tests import RobotTestController


def test_resetautonomous(robot_controller: RobotTestController, robot: Robot):
    elevator = robot.hardware.elevator
    printer = robot.hardware.printer
    arm = robot.hardware.arm
    drivetrain = robot.hardware.drivetrain
    claw = robot.hardware.claw
    intake = robot.hardware.intake
    climber = robot.hardware.climber
    controller = robot.hardware.controller

    # Testing if autonomousInit commands schedule properly
    robot_controller.startAutonomous()
    robot_controller.wait_until(
        lambda: not robot.autonomous.reset_intake_command.isScheduled(), 10.0
    )
    robot_controller.wait_until(
        lambda: not robot.autonomous.reset_climber_command.isScheduled(), 10.0
    )

    assert intake.state == Intake.State.Retracted
    assert climber.state == Climber.State.Initial

    # ResetAutonomous Test
    robot_controller.startTeleop()

    reset_cmd = ResetAutonomous(elevator, printer, arm)
    reset_cmd.schedule()

    robot_controller.wait_until(lambda: not reset_cmd.isScheduled(), 10.0)

    assert elevator.state == Elevator.State.Reset
    assert elevator.movement_state == Elevator.MovementState.FreeToMove
    assert printer.state == Printer.State.Reset
    assert printer.movement_state == Printer.MovementState.FreeToMove
    assert arm.state == Arm.State.Retracted
    assert arm.movement_state == Arm.MovementState.DoNotMove

    # Make sure that the reset didn't disturb the normal functioning of the robot
    elevator.state = Elevator.State.Level3
    arm.state = Arm.State.Extended

    cmd = DropPrepareLoading.toLeft(
        printer, arm, elevator, drivetrain, claw, controller
    )
    cmd.schedule()

    robot_controller.wait(1.0)

    robot_controller.wait_until(lambda: not cmd.isScheduled(), 10.0)

    assert elevator.state == Elevator.State.Loading
    assert printer.state == Printer.State.Loading
    assert arm.state == arm.State.Retracted
