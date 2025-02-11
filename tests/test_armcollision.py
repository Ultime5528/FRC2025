from robot import Robot
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.tests import RobotTestController


def test_RetractArm(robot_controller: RobotTestController, robot: Robot):

    arm = robot.hardware.arm
    elevator = robot.hardware.elevator
    printer = robot.hardware.printer

    arm.movement_state = Arm.MovementState.FreeToMove
    elevator.movement_state = Elevator.MovementState.FreeToMove
    printer.movement_state = Printer.MovementState.FreeToMove
