from robot import Robot


def test_setupCommands_not_crash(robot: Robot):
    robot.dashboard.setupCommands(robot.hardware)
