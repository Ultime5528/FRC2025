from _pytest.python_api import approx
from rev import SparkBase, SparkBaseConfig

from commands.climber.moveclimber import ReadyClimber, ReleaseClimber, Climb
from commands.climber.resetclimber import ResetClimber
from robot import Robot
from subsystems.climber import Climber
from ultime.switch import Switch
from ultime.tests import RobotTestController


def test_ports(robot: Robot):
    climber = robot.hardware.climber

    assert climber._motor.getDeviceId() == 9
    assert climber._switch.getChannel() == 9


def test_settings(robot: Robot):
    climber = robot.hardware.climber

    assert climber._switch.getType() == Switch.Type.NormallyClosed

    assert not climber._motor.getInverted()
    assert climber._motor.getMotorType() == SparkBase.MotorType.kBrushless
    assert not climber._motor.configAccessor.getInverted()
    assert (
        climber._motor.configAccessor.getIdleMode() == SparkBaseConfig.IdleMode.kBrake
    )
    assert climber._motor.configAccessor.getSmartCurrentLimit() == 30


def test_climber_ready(robot_controller: RobotTestController, robot: Robot):
    climber = robot.hardware.climber
    robot_controller.startTeleop()

    cmd = ReadyClimber(climber)
    cmd.schedule()

    robot_controller.wait(0.5)

    assert climber._motor.get() > 0.0

    robot_controller.wait_until(lambda: climber.state == Climber.State.Ready, 4.0)

    assert climber.getPosition() == approx(45.0, abs=1.0)
    assert climber.state == Climber.State.Ready
    assert climber._motor.get() == 0.0


def test_climber_climbed(robot_controller: RobotTestController, robot: Robot):
    climber = robot.hardware.climber
    robot_controller.startTeleop()

    cmd = Climb(climber)
    cmd.schedule()

    robot_controller.wait(0.5)

    assert climber._motor.get() > 0.0

    robot_controller.wait(20)

    cmd.isScheduled()
    assert climber._switch.isPressed()
    assert climber.state == climber.State.Climbed
    assert climber._motor.get() == 0.0


def test_climber_initial(robot_controller: RobotTestController, robot: Robot):
    climber = robot.hardware.climber
    robot_controller.startTeleop()

    cmd = Climb(climber)
    cmd.schedule()

    robot_controller.wait(20)

    assert climber.state == climber.State.Climbed

    cmd = ReleaseClimber(climber)
    cmd.schedule()

    robot_controller.wait(0.5)

    assert climber._motor.get() < 0.0

    robot_controller.wait(20)

    assert climber._motor.get() == approx(0.0, abs=0.1)
    assert climber.isInitial()


def testResetClimber(robot_controller: RobotTestController, robot: Robot):
    climber = robot.hardware.climber
    robot_controller.startTeleop()

    cmd = ResetClimber(climber)

    assert not cmd.isScheduled()
    assert not climber.isClimbed()
    assert not climber._switch.isPressed()
    assert climber._motor.get() == 0.0
    assert climber.state == climber.State.Unknown

    cmd.schedule()

    assert cmd.isScheduled()
    assert not climber.isClimbed()
    assert not climber._switch.isPressed()
    assert climber._motor.get() == 0.0
    assert (
        climber.state == climber.State.Unknown or climber.state == climber.State.Moving
    )

    robot_controller.wait(0.02)

    assert cmd.isScheduled()
    assert not climber.isClimbed()
    assert not climber._switch.isPressed()
    assert climber._motor.get() > 0.0
    assert climber.state == climber.State.Moving

    robot_controller.wait_until(lambda: climber._switch.isPressed(), 10.0)

    assert cmd.isScheduled()
    assert climber.isClimbed()
    assert climber._switch.isPressed()
    assert climber._motor.get() <= 0.0
    assert (
        climber.state == climber.State.Climbed or climber.state == climber.State.Moving
    )

    robot_controller.wait_until(lambda: not cmd.isScheduled(), 10.0)

    assert not cmd.isScheduled()
    assert not climber.isClimbed()
    assert not climber._switch.isPressed()
    assert climber._motor.get() == 0.0
    assert climber.state == climber.State.Initial
