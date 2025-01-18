import wpilib

from ultime.alert import AlertType, Alert


def test_a():
    assert len(Alert._groups) == 0
    alert = Alert("Test", AlertType.Error)


def test_b():
    assert len(Alert._groups) == 0
    alert = Alert("Test", AlertType.Error)
