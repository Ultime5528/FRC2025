from _pytest.python_api import approx
from wpilib.simulation import stepTiming

from commands.printer.resetright import ResetPrinterRight
from robot import Robot
from ultime.switch import Switch
from ultime.tests import RobotTestController


def test_ports(robot: Robot):
    printer = robot.hardware.printer

    assert printer._motor.getChannel() == 1
    assert printer._switch_left.getChannel() == 2
    assert printer._switch_right.getChannel() == 1


def test_settings(robot: Robot):
    printer = robot.hardware.printer

    assert not printer._motor.getInverted()
    assert printer._switch_left.getType() == Switch.Type.NormallyClosed
    assert printer._switch_right.getType() == Switch.Type.NormallyClosed

def test_reset_right(robot_controller: RobotTestController, robot: Robot):
    robot_controller.startTeleop()

    printer = robot.hardware.printer
    printer._sim_encoder.setDistance(0.5)

    # Enable robot and schedule command
    robot_controller.wait(0.5)
    cmd = ResetPrinterRight(printer)
    cmd.schedule()

    robot_controller.wait(0.5)

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
    assert printer._motor.get() == approx(0.0)
    assert printer.getPose() == approx(0.0, abs=1.0)

    assert not cmd.isScheduled()
