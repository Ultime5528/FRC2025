import math
import weakref
from typing import Union, Tuple, List, Callable

import numpy as np
import wpilib
from wpilib import AddressableLED, DriverStation, SmartDashboard, getTime, LEDPattern, Color
from wpiutil import SendableBuilder

import ports
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem


def interpolate(t, color1, color2):
    assert 0 <= t <= 1
    return ((1 - t) * color1 + t * color2).astype(int)


def numpy_interpolation(t: np.ndarray, color1: np.ndarray, color2: np.ndarray):
    assert 0 <= t.min() and t.max() <= 1
    return ((1 - t)[:, np.newaxis] * color1 + t[:, np.newaxis] * color2).astype(int)


_Color = Union[np.ndarray, Tuple[int, int, int], List[int]]


class LEDController(Subsystem):
    green_rgb = np.array([0, 255, 0])
    red_rgb = np.array([255, 0, 0])
    blue_rgb = np.array([0, 0, 255])
    black = np.array([0, 0, 0])
    white = np.array([255, 255, 255])

    led_number = autoproperty(250.0)

    brightness_value = autoproperty(20.0)

    def __init__(self, hardware):
        super().__init__()
        self.led_strip = AddressableLED(ports.PWM.led_strip)
        self.buffer = [AddressableLED.LEDData() for _ in range(int(self.led_number))]
        self.led_strip.setLength(len(self.buffer))
        self.led_strip.setData(self.buffer)
        self.led_strip.start()

        self.claw = hardware.claw
        self.elevator = hardware.elevator
        self.printer = hardware.printer

        self.time = 0
        self.has_seen_coral = False
        self.timer = wpilib.Timer()
        self.timer.reset()

        self.hardware = weakref.proxy(hardware)

    @property
    def brightness(self) -> float:
        return max(min(100, self.brightness_value), 0) / 100

    def getAllianceColor(self):
        alliance = DriverStation.getAlliance()
        if alliance == DriverStation.Alliance.kBlue:  # blue team
            color = Color.kBlue
        elif alliance == DriverStation.Alliance.kRed:  # red team
            color = Color.kRed
        else:
            color = Color.kBlack
        return color

    def e_stopped(self):
        self.e_stopped_pattern = LEDPattern.solid(Color.kRed)
        self.e_stopped_pattern = self.e_stopped_pattern.blink(1.0)

        self.e_stopped_pattern.applyTo(self.buffer)

    def modeAuto(self):
        color = self.getAllianceColor()
        mode_auto_pattern = LEDPattern.gradient(LEDPattern.GradientType.kDiscontinuous, [Color.kBlack, color])
        mode_auto_pattern = mode_auto_pattern.scrollAtRelativeSpeed(3.0)
        mode_auto_pattern.applyTo(self.buffer)


    def modeTeleop(self):
        color = self.getAllianceColor()
        mode_teleop_pattern = LEDPattern.solid(color)
        white_pattern = LEDPattern.solid(Color.kWhite)
        white_pattern_mask = LEDPattern.steps([(0, Color.kWhite), (0.5, Color.kBlack)]).scrollAtRelativeSpeed(2.0)
        white_pattern = white_pattern.mask(white_pattern_mask)
        mode_teleop_pattern = white_pattern.overlayOn(mode_teleop_pattern)

        mode_teleop_pattern.applyTo(self.buffer)

    def modeEndgame(self):
        mode_end_game_pattern = LEDPattern.steps([(0, Color.kRed), (0.5, Color.kBlue)]).scrollAtRelativeSpeed(1.0)

        mode_end_game_pattern.applyTo(self.buffer)

    def modeConnected(self):
        color = self.getAllianceColor()
        mode_connected_pattern = LEDPattern.solid(color)
        mode_connected_pattern = mode_connected_pattern.breathe(2.0)

        mode_connected_pattern.applyTo(self.buffer)

    def modeNotConnected(self):
        mode_not_connected_pattern = LEDPattern.steps([(0, Color.kRed), (0.5, Color.kBlue)])
        mode_not_connected_pattern.breathe(2.0)

        mode_not_connected_pattern.applyTo(self.buffer)

    def rainbow(self):
        rainbow_pattern = LEDPattern.rainbow(255, 128)

        rainbow_pattern.applyTo(self.buffer)

    def periodic(self) -> None:
        start_time = getTime()
        self.time += 1

        if DriverStation.isEStopped():
            self.e_stopped()
        elif DriverStation.isAutonomousEnabled():  # auto
            self.modeAuto()
        elif DriverStation.isTeleopEnabled():  # teleop
            if DriverStation.getMatchTime() > 15:
                self.modeTeleop()
            elif DriverStation.getMatchTime() == -1.0:
                self.rainbow()
            else:
                self.modeEndgame()
        elif DriverStation.isDSAttached():
            self.modeConnected()  # connected to driver station
        else:  # not connected to driver station
            self.modeNotConnected()

        self.led_strip.setData(self.buffer)
        SmartDashboard.putNumber("led_time", getTime() - start_time)

    def getCurrentDrawAmps(self) -> float:
        return 0.0

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)
        builder.addIntegerProperty("time", lambda: self.time, lambda _: None)
