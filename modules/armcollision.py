from modules.hardware import HardwareModule
from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.module import Module


class ArmCollision(Module):
    def __init__(self, hardwareModule: HardwareModule):
        super().__init__()

        self.arm = hardwareModule.arm
        self.printer = hardwareModule.printer
        self.elevator = hardwareModule.elevator

    def robotPeriodic(self) -> None:
        self.arm.movement_state = Arm.MovementState.FreeToMove
        self.elevator.movement_state = Elevator.MovementState.FreeToMove
        self.printer.movement_state = Printer.MovementState.FreeToMove

        if self.elevator.isInLowerZone() and self.arm.state == Arm.State.Retracted:
            self.arm.movement_state = Arm.MovementState.DoNotExtendOrRetract

        if self.printer.isInMiddleZone() and not self.arm.state == Arm.State.Moving:
            self.arm.movement_state = Arm.MovementState.DoNotExtendOrRetract

        if self.arm.state == Arm.State.Unknown:
            self.elevator.movement_state = Elevator.MovementState.AvoidLowerZone
            self.printer.movement_state = Printer.MovementState.AvoidMiddleZone

        if self.arm.state != Arm.State.Retracted:
            # Impossible to have elevator in lower zone?
            self.elevator.movement_state = Elevator.MovementState.AvoidLowerZone

        if self.arm.state == Arm.State.Moving:
            # What if the printer is already in the middle zone?
            self.printer.movement_state = Printer.MovementState.AvoidMiddleZone
