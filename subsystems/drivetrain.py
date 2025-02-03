from rev import SparkMax, SparkLowLevel
from wpiutil import SendableBuilder

from ultime.subsystem import Subsystem


class Drivetrain(Subsystem):
    def __init__(self):
        super().__init__()
        self.motor = SparkMax(1, SparkLowLevel.MotorType.kBrushless)

    def getCurrentDrawAmps(self):
        return 0.0

    def periodic(self) -> None:
        pass

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)
