from ntcore import NetworkTableInstance

from ultime.alert import AlertType, Alert
from ultime.tests import RobotTestController


def test_alert(robot_controller: RobotTestController):
    topic = (
        NetworkTableInstance.getDefault()
        .getStringArrayTopic("/SmartDashboard/Alerts/errors")
        .subscribe(["default"])
    )
    alert = Alert("Test", AlertType.Error)

    robot_controller.wait(0.1)

    assert topic.get() == []

    alert.set(True)
    robot_controller.wait(0.1)

    assert topic.get() == ["Test"]

    alert.setText("Test2")
    robot_controller.wait(0.1)

    assert topic.get() == ["Test2"]

    alert.set(False)
    robot_controller.wait(0.1)

    assert topic.get() == []

    alert.setText("Test3")
    robot_controller.wait(0.1)

    assert topic.get() == []

    alert.set(True)
    robot_controller.wait(0.1)

    assert topic.get() == ["Test3"]


def test_alert_weakrefset_empty():
    assert len(Alert._groups) == 0
