from commands.arm.retractarm import RetractArm
from robot import Robot


def testPorts(robot: Robot):
    arm = robot.hardware.arm
    assert arm.arm_motor.getChannel() == 0

def testSettings(robot: Robot):
    arm = robot.hardware.arm

    assert not arm.arm_motor.getInverted()

def testRetractArm(control, robot: Robot):
    arm = robot.hardware.arm

    with control.run_robot:
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = RetractArm(arm)
        assert arm.arm_motor.get() == 0.3
