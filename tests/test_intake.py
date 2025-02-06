from _pytest.python_api import approx

from commands.Intake.grabalgae import GrabAlgae
from robot import Robot
from ultime.switch import Switch
from ultime.tests import RobotTestController
from ultime.tests.utils import robot_controller


def test_ports(robot: Robot):
    intake = robot.hardware.intake

    assert intake.pivot_motor.getChannel() == 3
    assert intake.grab_motor.getChannel() == 4

    assert intake.pivot_encoder.getChannel() == 1
    assert intake.pivot_switch.getChannel() == 2
    assert intake.grab_switch.getChannel() == 3


def test_settings(robot: Robot):
    intake = robot.hardware.intake

    assert intake.pivot_switch.getType() == Switch.Type.NormallyOpen

    assert not intake.pivot_motor.getInverted()

    assert intake.grab_switch.getType() == Switch.Type.NormallyOpen

    assert not intake.grab_motor.getInverted()

def test_grab_algae(
        robotController: RobotTestController,
        robot: Robot,
        GrabAlgae
):
    robotController.startTeleop()

    robotController.wait(0.5)

    assert not robot.hardware.intake.grab_switch.isPressed()

    cmd = GrabAlgae(robot.hardware.intake)
    cmd.schedule()

    robotController.wait(0.5)

    assert not robot.hardware.intake.grab_switch.isPressed()
    assert robot.hardware.intake.grab_motor.get() == approx(0.3)

    robotController.wait(0.2)

    robot.hardware.intake.grab_switch.isPressed()

    robotController.wait(1.5)

    assert robot.hardware.intake.grab_motor.get() == approx(0.3)
    
    robotController.wait(5)

    assert robot.hardware.intake.grab_motor.get() == approx(0.0)