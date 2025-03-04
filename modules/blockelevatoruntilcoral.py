from modules.hardware import HardwareModule
from subsystems.elevator import Elevator
from ultime.module import Module


class BlockElevatorUntilCoral(Module):
    def __init__(self, hardware: HardwareModule):
        super().__init__()
        self.claw = hardware.claw
        self.elevator = hardware.elevator

    def robotPeriodic(self) -> None:
        if (
            self.elevator.loading_state != Elevator.LoadingState.DoNotMoveWhileLoading
            or self.claw.has_coral
        ):
            if (
                self.elevator.state == Elevator.State.Loading
                and not self.claw.has_coral
            ):
                self.elevator.loading_state = (
                    Elevator.LoadingState.DoNotMoveWhileLoading
                )
            else:
                self.elevator.loading_state = Elevator.LoadingState.FreeToMove
