from _pytest.python_api import approx

from commands.arm.extendarm import ExtendArm
from commands.arm.retractarm import RetractArm
from commands.elevator.moveelevator import MoveElevator
from commands.elevator.resetelevator import ResetElevator
from commands.printer.moveprinter import MovePrinter
from commands.printer.resetprinter import ResetPrinterRight
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

def testRetractFailBadPrinterPosition(
    robot_controller: RobotTestController, robot: Robot
):
    list_commands_arm = [RetractArm, ExtendArm]
    list_initial_arm_state = [Arm.State.Extended, Arm.State.Retracted]
    list_initial_elevator_state = [Elevator.State.Loading, Elevator.State.Level1, Elevator.State.Level2, Elevator.State.Level3, Elevator.State.Level4]
    list_initial_printer_state = [Printer.State.Left, Printer.State.MiddleLeft, Printer.State.MiddleRight, Printer.State.Right]

    list_initial_elevator_cmd = [MoveElevator.toLoading, MoveElevator.toLevel1, MoveElevator.toLevel2, MoveElevator.toLevel3, MoveElevator.toLevel4]
    list_initial_printer_cmd = [MovePrinter.toLeft, MovePrinter.toMiddleLeft, MovePrinter.toMiddle, MovePrinter.toMiddleRight, MovePrinter.toRight, MovePrinter.toLoading]

    list_initial_move_printer_cmd = [MovePrinter.toLeft, MovePrinter.toMiddleLeft, MovePrinter.toMiddle, MovePrinter.toMiddleRight, MovePrinter.toRight, MovePrinter.toLoading]

    list_running_elevator_cmd = [None, MoveElevator.toLoading, MoveElevator.toLevel1, MoveElevator.toLevel2, MoveElevator.toLevel3, MoveElevator.toLevel4]
    list_running_printer_cmd = [None, MovePrinter.toLeft, MovePrinter.toMiddleLeft, MovePrinter.toMiddle, MovePrinter.toMiddleRight, MovePrinter.toRight, MovePrinter.toLoading]

    for _command_arm in list_commands_arm:
        for _initial_arm_state in list_initial_arm_state:
            for _initial_elevator_state in list_initial_elevator_state:
                for _initial_printer_state in list_initial_printer_state:
                    for _initial_elevator_cmd in list_initial_elevator_cmd:
                        for _initial_printer_cmd in list_initial_printer_cmd:
                            for _initial_move_printer_cmd in list_initial_move_printer_cmd:
                                for _running_elevator_cmd in list_running_elevator_cmd:
                                    for _running_printer_cmd in list_running_printer_cmd:
                                        class TestParameters:
                                            Cmd = _command_arm

                                            initial_arm_state = _initial_arm_state
                                            initial_elevator_state = _initial_elevator_state
                                            initial_printer_state = _initial_printer_state

                                            initial_arm_movement_state = Arm.MovementState.FreeToMove
                                            initial_elevator_movement_state = Elevator.MovementState.FreeToMove
                                            initial_printer_movement_state = Printer.MovementState.FreeToMove

                                            initial_arm_speed = 0.0  ####

                                            initial_move_elevator_cmd = _initial_elevator_cmd

                                            initial_printer_pose = (
                                                                           robot.hardware.printer.middle_zone_right  ######
                                                                           + robot.hardware.printer.middle_zone_left
                                                                   ) * 0.5
                                            initial_printer_function = Printer.stop

                                            initial_move_printer_cmd = _initial_move_printer_cmd

                                            running_elevator_cmd = _running_elevator_cmd
                                            running_printer_cmd = _running_printer_cmd

                                            #running_arm_speed = 0
                                            running_arm_state = None
                                            if (initial_move_printer_cmd == MovePrinter.toMiddle and running_printer_cmd == None) or (initial_move_elevator_cmd == MoveElevator.toLoading and running_elevator_cmd == None and Cmd != RetractArm):
                                                running_arm_speed = lambda arm: 0.0
                                                if initial_arm_state == Arm.State.Extended:
                                                    running_arm_state = Arm.State.Extended
                                                    end_arm_state = Arm.State.Extended
                                                else:
                                                    running_arm_state = Arm.State.Retracted
                                                    end_arm_state = Arm.State.Retracted
                                            else:
                                                if Cmd == RetractArm:
                                                    running_arm_speed = lambda arm: -arm.speed
                                                    running_arm_state = Arm.State.Moving
                                                    end_arm_state = Arm.State.Retracted
                                                else:
                                                    running_arm_speed = lambda arm: arm.speed
                                                    running_arm_state = Arm.State.Moving
                                                    end_arm_state = Arm.State.Extended

                                            def running_arm_moving_condition(arm: Arm) -> bool:
                                                return True

                                            def running_elevator_state(elevator: Elevator):
                                                if _running_elevator_cmd != _initial_elevator_cmd and _running_elevator_cmd is not None:
                                                    if _running_elevator_cmd == MoveElevator.toLoading:
                                                        return elevator.state == Elevator.State.Loading or elevator.state == Elevator.State.Moving
                                                    elif _running_elevator_cmd == MoveElevator.toLevel1:
                                                        return  elevator.state == Elevator.State.Level1 or elevator.state == Elevator.State.Moving
                                                    elif _running_elevator_cmd == MoveElevator.toLevel2:
                                                        return  elevator.state == Elevator.State.Level2 or elevator.state == Elevator.State.Moving
                                                    elif _running_elevator_cmd == MoveElevator.toLevel3:
                                                        return  elevator.state == Elevator.State.Level3 or elevator.state == Elevator.State.Moving
                                                    elif _running_elevator_cmd == MoveElevator.toLevel4:
                                                        return  elevator.state == Elevator.State.Level4 or elevator.state == Elevator.State.Moving
                                                else:
                                                    if _initial_elevator_cmd == MoveElevator.toLoading:
                                                        return  elevator.state == Elevator.State.Loading
                                                    elif _initial_elevator_cmd == MoveElevator.toLevel1:
                                                        return  elevator.state == Elevator.State.Level1
                                                    elif _initial_elevator_cmd == MoveElevator.toLevel2:
                                                        return  elevator.state == Elevator.State.Level2
                                                    elif _initial_elevator_cmd == MoveElevator.toLevel3:
                                                        return  elevator.state == Elevator.State.Level3
                                                    elif _initial_elevator_cmd == MoveElevator.toLevel4:
                                                        return  elevator.state == Elevator.State.Level4

                                            def running_printer_state(printer: Printer):
                                                if _initial_printer_cmd != _running_printer_cmd and _running_printer_cmd is not None:
                                                    if _running_printer_cmd == MovePrinter.toLeft:
                                                        return (printer.state == Printer.State.Moving or printer.state == Printer.State.Left)
                                                    elif _running_printer_cmd == MovePrinter.toMiddleLeft:
                                                        return (printer.state == Printer.State.Moving or printer.state == Printer.State.MiddleLeft)
                                                    elif _running_printer_cmd == MovePrinter.toMiddle:
                                                        return (printer.state == Printer.State.Moving or printer.state == Printer.State.Middle)
                                                    elif _running_printer_cmd == MovePrinter.toMiddleRight:
                                                        return (printer.state == Printer.State.Moving or printer.state == Printer.State.MiddleRight)
                                                    elif _running_printer_cmd == MovePrinter.toRight:
                                                        return (printer.state == Printer.State.Moving or printer.state == Printer.State.Right)
                                                    elif _running_printer_cmd == MovePrinter.toLoading:
                                                        return (printer.state == Printer.State.Moving or printer.state == Printer.State.Loading)
                                                else:
                                                    if _initial_printer_cmd == MovePrinter.toLeft:
                                                        return printer.state == Printer.State.Left
                                                    elif _initial_printer_cmd == MovePrinter.toMiddleLeft:
                                                        return printer.state == Printer.State.MiddleLeft
                                                    elif _initial_printer_cmd == MovePrinter.toMiddle:
                                                        return printer.state == Printer.State.Middle
                                                    elif _initial_printer_cmd == MovePrinter.toMiddleRight:
                                                        return printer.state == Printer.State.MiddleRight
                                                    elif _initial_printer_cmd == MovePrinter.toRight:
                                                        return printer.state == Printer.State.Right
                                                    elif _initial_printer_cmd == MovePrinter.toLoading:
                                                        return printer.state == Printer.State.Loading

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

    print(parameters.Cmd)
    print(parameters.initial_move_printer_cmd)
    print(parameters.running_printer_cmd)
    print(parameters.initial_move_elevator_cmd)
    print(parameters.running_elevator_cmd)

    robot_controller.startTeleop()

    if arm.state != arm.State.Extended:
        cmd_reset_elevator = ResetElevator(elevator)
        cmd_reset_elevator.schedule()
        robot_controller.wait(mega_delay)

        assert not cmd_reset_elevator.isScheduled()
    else:
        elevator._has_reset = True

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

    robot_controller.wait(cmd.delay - sampling_time)

    assert arm._motor.get() == approx(parameters.running_arm_speed(arm), abs=0.1)
    assert arm.state == parameters.running_arm_state
    assert parameters.running_elevator_state(elevator)
    assert parameters.running_printer_state(printer)
    assert cmd.isScheduled()
    assert cmd.hasRequirement(arm)

    robot_controller.wait(sampling_time + 0.02)

    assert arm._motor.get() == approx(parameters.end_arm_speed, rel=0.1)
    assert arm.state == parameters.end_arm_state
    print("Passed")
