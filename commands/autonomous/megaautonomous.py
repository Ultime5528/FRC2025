from commands2 import SequentialCommandGroup
from commands2.cmd import parallel, sequence, either, waitSeconds
from pathplannerlib.path import PathPlannerPath

from commands.claw.loadcoral import LoadCoral
from commands.claw.retractcoral import RetractCoral
from commands.claw.waituntilcoral import WaitUntilCoral
from commands.dropautonomous import DropAutonomous
from commands.elevator.moveelevator import MoveElevator
from commands.prepareloading import PrepareLoading
from commands.resetautonomous import ResetAutonomous
from modules.hardware import HardwareModule
from ultime.followpath import FollowPath


class MegaAutonomous(SequentialCommandGroup):
    @classmethod
    def left(cls, hardware: HardwareModule):
        cmd = MegaAutonomous(hardware, True)
        cmd.setName(MegaAutonomous.__name__ + ".left")
        return cmd

    @classmethod
    def right(cls, hardware: HardwareModule):
        cmd = MegaAutonomous(hardware, False)
        cmd.setName(MegaAutonomous.__name__ + ".right")
        return cmd

    def __init__(self, hardware: HardwareModule, is_left_side: bool):
        super().__init__()

        el = hardware.elevator
        pr = hardware.printer
        arm = hardware.arm
        claw = hardware.claw
        driv = hardware.drivetrain

        def Follow(path: str):
            return FollowPath(
                PathPlannerPath.fromPathFile(path),
                driv,
            )

        def Drop():
            return DropAutonomous(
                hardware.printer,
                hardware.arm,
                hardware.elevator,
                driv,
                hardware.claw,
                "none",
                True,
            )

        self.addCommands(
            parallel(
                sequence(
                    ResetAutonomous(el, pr, arm),
                    parallel(
                        MoveElevator.toLevel4(el),
                        RetractCoral.retract(claw),
                    ),
                ),
                either(
                    Follow("Straight Align #20 Left"),
                    Follow("Straight Align #22 Right"),
                    lambda: is_left_side,
                ),
            ),
            Drop(),
            #coral 2
            parallel(
                either(
                    Follow("Go to Coral Station after reef #20 Left"),
                    Follow("Go to Coral Station after reef #22 Right"),
                    lambda: is_left_side,
                ),
                PrepareLoading(el, arm, pr),
            ),
            WaitUntilCoral(claw),
            parallel(
                sequence(
                    LoadCoral(claw, pr),
                    RetractCoral.retract(claw),
                ),
                sequence(
                    parallel(
                        either(
                            Follow("Go to tag #19 after loading Left"),
                            Follow("Go to tag #17 after loading Right"),
                            lambda: is_left_side,
                        ),
                        sequence(
                            waitSeconds(0.3),
                            MoveElevator.toLevel4(el),
                        )
                    ),
                )
            ),
            Drop(),
            #Coral 3
            parallel(
                either(
                    Follow("Go to Coral Station after reef #20 Left"),
                    Follow("Go to Coral Station after reef #22 Right"),
                    lambda: is_left_side,
                ),
                PrepareLoading(el, arm, pr),
            ),
            WaitUntilCoral(claw),
            parallel(
                sequence(
                    LoadCoral(claw, pr),
                    RetractCoral.retract(claw),
                ),
                sequence(
                    parallel(
                        either(
                            # TODO new paths with left offset
                            Follow("Go to tag #19 after loading Left"),
                            Follow("Go to tag #17 after loading Right"),
                            lambda: is_left_side,
                        ),
                        sequence(
                            waitSeconds(0.3),
                            MoveElevator.toLevel4(el),
                        )
                    ),
                )
            ),
        )
