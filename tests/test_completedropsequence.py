from commands.completedropsequence import CompleteDropSequence
from robot import Robot
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.tests import RobotTestController


def test_completedropsequence(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()
    elevator = robot.hardware.elevator
    printer = robot.hardware.printer
    arm = robot.hardware.arm
    drivetrain = robot.hardware.drivetrain
    claw = robot.hardware.claw

    elevator.state = Elevator.State.Level3
    arm.state = Arm.State.Extended

    cmd = CompleteDropSequence.toLeft(printer, arm, elevator, drivetrain, claw)
    cmd.schedule()

    robot_controller.wait(1.0)

    robot_controller.wait_until(lambda: not cmd.isScheduled(), 10.0)

    assert elevator.state == Elevator.State.Loading
    assert printer.state == Printer.State.Loading
    assert arm.state == arm.State.Retracted
