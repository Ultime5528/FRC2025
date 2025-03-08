from commands.claw.loadcoral import LoadCoral
from modules.hardware import HardwareModule
from ultime.module import Module
from ultime.timethis import tt


class LoadingDetectionModule(Module):
    def __init__(self, hardware: HardwareModule):
        super().__init__()
        self.claw = hardware.claw
        self.elevator = hardware.elevator
        self.printer = hardware.printer
        self._load_command = LoadCoral(self.claw)
        self._is_at_loading = False

    def teleopPeriodic(self) -> None:
        self._is_at_loading = (
            self.printer.state == self.printer.State.Loading
            and self.elevator.state == self.elevator.State.Loading
        )

        if self.claw.seesObject() and not self.claw.has_coral and self._is_at_loading:
            self._load_command.schedule()

    def isLoading(self):
        return self._load_command.isScheduled()

    def initSendable(self, builder):
        super().initSendable(builder)

        def noop(_):
            pass

        builder.addBooleanProperty(
            "is_at_loading", tt(lambda: self._is_at_loading), noop
        )
        builder.addBooleanProperty("is_loading", tt(self.isLoading), noop)
