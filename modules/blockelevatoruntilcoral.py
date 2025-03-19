from modules.loadingdetection import LoadingDetectionModule
from subsystems.elevator import Elevator
from ultime.module import Module


class BlockElevatorUntilCoralModule(Module):
    def __init__(self, loading_detection: LoadingDetectionModule, elevator: Elevator):
        super().__init__()
        self.loading_detection = loading_detection
        self.elevator = elevator

    def robotPeriodic(self) -> None:
        if self.loading_detection.isLoading():
            self.elevator.loading_state = Elevator.LoadingState.DoNotMoveWhileLoading
        else:
            self.elevator.loading_state = Elevator.LoadingState.FreeToMove
