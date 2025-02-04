from commands2 import SelectCommand

from commands.claw.drop import Drop
from subsystems.claw import Claw
from subsystems.elevator import Elevator
from ultime.command import ignore_requirements


@ignore_requirements(["claw", "elevator"])
class AutoDrop(SelectCommand):
    def __init__(self, claw: Claw, elevator: Elevator):
        super().__init__(
            {
                Elevator.State.Level1: Drop.atLevel1(claw),
                Elevator.State.Level2: Drop.atLevel2(claw),
                Elevator.State.Level3: Drop.atLevel3(claw),
                Elevator.State.Level4: Drop.atLevel4(claw),
            },
            lambda: elevator.state
        )