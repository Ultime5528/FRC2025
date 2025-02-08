from _pytest.python_api import approx
from commands2.cmd import runOnce

from commands.intake.dropalgae import DropAlgae
from commands.intake.grabalgae import _GrabAlgae, GrabAlgae
from commands.intake.moveintake import MoveIntake
from commands.intake.resetintake import ResetIntake
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


def test_grab_algae(robot_controller: RobotTestController, robot: Robot):
    # setting up shortcuts
    def wait(time):
        robot_controller.wait(time)

    intake = robot.hardware.intake

    # actual test
    robot_controller.startTeleop()
    wait(0.5)

    intake._has_reset = True
    intake._sim_encoder.setDistance(0)
    intake._grab_switch.setSimUnpressed()

    cmd = GrabAlgae(robot.hardware.intake)
    cmd.schedule()

    wait(1)

    assert intake._grab_motor.get() == approx(0.0)
    assert intake._pivot_motor.get() > 0.0

    intake._sim_encoder.setDistance(1)

    wait(0.3)

    assert intake._grab_motor.get() == approx(0.3, rel=0.1)
    assert intake._pivot_motor.get() == 0.0

    intake._grab_switch.setSimPressed()

    wait(0.5)

    assert intake._grab_motor.get() == approx(0.3, rel=0.1)

    wait(5)

    assert intake._grab_motor.get() == 0.0


def test_drop_algae(robot_controller: RobotTestController, robot: Robot):
    # setting up shortcuts
    def wait(time):
        robot_controller.wait(time)

    intake = robot.hardware.intake

    # actual test
    robot_controller.startTeleop()
    intake._grab_switch.setSimPressed()
    intake._sim_encoder.setDistance(50)
    intake._has_reset = True

    wait(0.5)

    cmd = DropAlgae(intake)
    cmd.schedule()

    wait(0.5)

    assert intake._grab_motor.get() == approx(-0.3, rel=0.1)
    assert intake._pivot_motor.get() == 0.0

    intake._grab_switch.setSimUnpressed()

    wait(1.5)

    assert intake._grab_motor.get() == approx(-0.3, rel=0.1)

    wait(3)

    assert intake._grab_motor.get() == 0.0
    assert intake._pivot_motor.get() < 0.0

    intake._sim_encoder.setDistance(0.0)

    wait(1)

    assert intake._pivot_motor.get() == 0.0


def test_reset_intake(robot_controller: RobotTestController, robot: Robot):
    # setting up shortcuts
    def wait(time):
        robot_controller.wait(time)

    intake = robot.hardware.intake

    # actual test
    robot_controller.startTeleop()
    assert not intake._has_reset

    wait(0.5)

    intake._pivot_switch.setSimUnpressed()

    cmd = ResetIntake(intake)
    cmd.schedule()

    wait(5)

    assert intake.hasReset()
    assert intake.getPivotPosition() == approx(0, abs=0.2)