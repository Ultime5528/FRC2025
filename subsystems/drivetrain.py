from wpiutil import SendableBuilder

from ultime.subsystem import Subsystem


class Drivetrain(Subsystem):
    def __init__(self):
        super().__init__()

    def periodic(self) -> None:
        pass

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)
