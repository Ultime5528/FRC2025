from subsystems.arm import Arm
from subsystems.elevator import Elevator
from subsystems.printer import Printer
from ultime.module import Module


class ArmCollision(Module):
    def __init__(self, arm: Arm, printer: Printer, elevator: Elevator):
        super().__init__()

        self.arm = arm
        self.printer = printer
        self.elevator = elevator

    def autonomousInit(self) -> None:
        pass

    def autonomousPeriodic(self) -> None:
        pass

    def autonomousExit(self) -> None:
        pass

    def teleopInit(self) -> None:
        pass

    def teleopPeriodic(self) -> None:
        self.arm.movement_state = Arm.MovementState.FreeToMove
        self.elevator.movement_state = Elevator.MovementState.FreeToMove
        self.printer.movement_state = Printer.MovementState.FreeToMove

        if self.arm.state == Arm.State.Retracted and self.elevator.isInLowerZone():
            self.arm.movement_state = Arm.MovementState.DoNotExtend

        elif self.arm.state != Arm.State.Retracted:
            # Impossible to have elevator in lower zone?
            self.elevator.movement_state = Elevator.MovementState.AvoidLowerZone

        if self.arm.isInMovement():
            # What if the printer is already in the middle zone?
            self.printer.movement_state = Printer.MovementState.AvoidMiddleZone

    def teleopExit(self) -> None:
        pass
