from _pytest.python_api import approx
from commands2.cmd import runOnce

from commands.Intake.grabalgae import _GrabAlgae
from robot import Robot
from ultime.switch import Switch
from ultime.tests import RobotTestController
from ultime.tests.utils import robot_controller


def test_ports(robot: Robot):
    intake = robot.hardware.intake

    assert intake._grab_motor.getChannel() == 4
    assert intake._pivot_motor.getChannel() == 5

    assert intake._pivot_switch.getChannel() == 8
    assert intake._grab_switch.getChannel() == 9

def test_settings(robot: Robot):
    intake = robot.hardware.intake

    assert intake._pivot_switch.getType() == Switch.Type.NormallyOpen

    assert not intake._pivot_motor.getInverted()

    assert intake._grab_switch.getType() == Switch.Type.NormallyOpen

    assert not intake._grab_motor.getInverted()


def test_grab_algae(robotController: RobotTestController, robot: Robot, GrabAlgae):
    # setting up shortcuts
    def wait(time):
        robotController.wait(time)

    intake = robot.hardware.intake

    # actual test
    robotController.startTeleop()
    wait(0.5)

    cmd = GrabAlgae(robot.hardware.intake)
    cmd.schedule()

    intake._has_reset = True
    intake._sim_encoder.setDistance(0)
    intake._grab_switch.setSimUnpressed()

    wait(1)

    assert intake._grab_motor.get() == approx(0.0)
    assert intake._pivot_motor.get() > 0.0

    intake._sim_encoder.setDistance(51)

    wait(0.3)

    assert intake._grab_motor.get() == approx(0.3)
    assert intake._pivot_motor == 0.0

    intake._grab_switch.setSimPressed()

    wait(1.5)

    assert intake._grab_motor.get() == approx(0.3)

    wait
