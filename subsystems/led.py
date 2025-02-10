from wpilib import AddressableLED

import ports
from ultime.autoproperty import autoproperty
from ultime.subsystem import Subsystem


class LEDController(Subsystem):
    led_number = autoproperty(190)

    def __init__(self):
        super().__init__()
        self.led_strip = AddressableLED(ports.DIO.led_strip)
        self.buffer = [AddressableLED.LEDData() for _ in range(self.led_number)]


    def getCurrentDrawAmps(self) -> float:
        pass
