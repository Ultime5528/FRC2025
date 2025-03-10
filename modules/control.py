from commands.alignwithreefside import AlignWithReefSide
from commands.arm.extendarm import ExtendArm
from commands.arm.retractarm import RetractArm
from commands.claw.drop import Drop
from commands.climber.moveclimber import (
    Climb,
    ReleaseClimber,
    ReadyClimberAndBalance,
)
from commands.climber.resetclimber import ResetClimber
from commands.dropprepareloading import DropPrepareLoading
from commands.elevator.moveelevator import MoveElevator
from commands.intake.dropalgae import DropAlgae
from commands.intake.grabalgae import GrabAlgae
from commands.intake.moveintake import MoveIntake
from commands.prepareloading import PrepareLoading
from commands.resetallbutclimber import ResetAllButClimber
from commands.vision.alignwithalgae import AlignWithAlgae
from modules.algaevision import AlgaeVisionModule
from modules.hardware import HardwareModule
from ultime.axistrigger import AxisTrigger
from ultime.module import Module


class ControlModule(Module):
    def __init__(
        self,
        hardware: HardwareModule,
        algae_vision: AlgaeVisionModule,
    ):
        super().__init__()

        """
        Pilot's buttons
        """
        hardware.controller.rightTrigger().whileTrue(
            AlignWithAlgae(hardware.drivetrain, algae_vision, hardware.controller)
        )

        hardware.controller.leftTrigger().whileTrue(
            AlignWithReefSide(hardware.drivetrain)
        )

        """
        Copilot's panel
        """
        # Elevator Levels
        hardware.panel_2.button(2).onTrue(Drop.atLevel2(hardware.claw))
        AxisTrigger(hardware.panel_1, 1, "up").onTrue(
            MoveElevator.toLevel1(hardware.elevator)
        )
        AxisTrigger(hardware.panel_1, 0, "up").onTrue(
            MoveElevator.toLevel2(hardware.elevator)
        )
        AxisTrigger(hardware.panel_1, 1, "down").onTrue(
            MoveElevator.toLevel3(hardware.elevator)
        )
        AxisTrigger(hardware.panel_1, 0, "down").onTrue(
            MoveElevator.toLevel4(hardware.elevator)
        )

        # Coral Drop and Load
        hardware.panel_1.button(1).onTrue(
            DropPrepareLoading.toLeft(
                hardware.printer,
                hardware.arm,
                hardware.elevator,
                hardware.drivetrain,
                hardware.claw,
                hardware.controller,
                False,
            )
        )
        AxisTrigger(hardware.panel_2, 1, "down").onTrue(
            DropPrepareLoading.toRight(
                hardware.printer,
                hardware.arm,
                hardware.elevator,
                hardware.drivetrain,
                hardware.claw,
                hardware.controller,
                False,
            )
        )
        AxisTrigger(hardware.panel_2, 0, "up").onTrue(
            PrepareLoading(hardware.elevator, hardware.arm, hardware.printer)
        )

        # Algae Manipulator
        AxisTrigger(hardware.panel_2, 1, "up").onTrue(GrabAlgae(hardware.intake))
        hardware.panel_2.button(3).onTrue(DropAlgae(hardware.intake))
        hardware.panel_2.button(1).onTrue(MoveIntake.toRetracted(hardware.intake))

        # Arm
        AxisTrigger(hardware.panel_2, 0, "down").onTrue(RetractArm(hardware.arm))
        hardware.panel_1.button(2).onTrue(ExtendArm(hardware.arm))

        # Climber
        hardware.panel_2.button(7).onTrue(ResetClimber(hardware.climber))
        hardware.panel_2.button(4).onTrue(
            ReadyClimberAndBalance(hardware.printer, hardware.climber)
        )
        hardware.panel_2.button(5).onTrue(Climb(hardware.climber))
        hardware.panel_2.button(6).onTrue(ReleaseClimber(hardware.climber))

        # Extra buttons
        hardware.panel_1.button(3).onTrue(
            ResetAllButClimber(
                hardware.elevator,
                hardware.printer,
                hardware.arm,
                hardware.intake,
            )
        )
