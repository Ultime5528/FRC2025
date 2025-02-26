from commands.resetallbutclimber import ResetAllButClimber
from commands.vision.alignwithalgae import AlignWithAlgae
from modules.algaevision import AlgaeVisionModule
from commands.completedropsequence import CompleteDropSequence
from commands.arm.extendarm import ExtendArm
from commands.arm.retractarm import RetractArm
from commands.climber.moveclimber import ReadyClimber, Climb, ReleaseClimber
from commands.climber.resetclimber import ResetClimber
from commands.elevator.moveelevator import MoveElevator
from commands.intake.dropalgae import DropAlgae
from commands.intake.grabalgae import GrabAlgae
from commands.intake.moveintake import MoveIntake
from commands.prepareloading import PrepareLoading
from commands.resetall import ResetAll
from modules.hardware import HardwareModule
from ultime.axistrigger import AxisTrigger
from ultime.module import Module


class ControlModule(Module):
    def __init__(self, hardware: HardwareModule, vision_algae: AlgaeVisionModule):
        super().__init__()
        self.hardware = hardware
        self.algae_vision = vision_algae

        self.setupButtons()
        # self.hardware.controller.button(1).onTrue(Command())

    def setupButtons(self):
        """
        Bind commands to buttons on controllers and joysticks
        """
        # Example code for xbox_controller
        # self.hardware.controller.leftTrigger().whileTrue(
        #     AlignedPickUp(self.drivetrain, self.intake, self.vision_pick_up)
        # )
        self.hardware.controller.rightTrigger().whileTrue(
            AlignWithAlgae(
                self.hardware.drivetrain, self.algae_vision, self.hardware.controller
            )
        )

        # Pilot buttons

        # Copilot's panel
        # Elevator Levels
        AxisTrigger(self.hardware.panel_1, 1, "up").onTrue(
            MoveElevator.toLevel1(self.hardware.elevator)
        )
        AxisTrigger(self.hardware.panel_1, 0, "up").onTrue(
            MoveElevator.toLevel2(self.hardware.elevator)
        )
        AxisTrigger(self.hardware.panel_1, 1, "down").onTrue(
            MoveElevator.toLevel3(self.hardware.elevator)
        )
        AxisTrigger(self.hardware.panel_1, 0, "down").onTrue(
            MoveElevator.toLevel4(self.hardware.elevator)
        )

        # Coral Drop and Load
        self.hardware.panel_1.button(1).onTrue(
            CompleteDropSequence.toLeft(
                self.hardware.printer,
                self.hardware.arm,
                self.hardware.elevator,
                self.hardware.drivetrain,
                self.hardware.claw,
            )
        )
        AxisTrigger(self.hardware.panel_2, 1, "down").onTrue(
            CompleteDropSequence.toRight(
                self.hardware.printer,
                self.hardware.arm,
                self.hardware.elevator,
                self.hardware.drivetrain,
                self.hardware.claw,
            )
        )
        AxisTrigger(self.hardware.panel_2, 0, "up").onTrue(
            PrepareLoading(
                self.hardware.elevator, self.hardware.arm, self.hardware.printer
            )
        )

        # Algae Manipulator
        AxisTrigger(self.hardware.panel_2, 1, "up").onTrue(
            GrabAlgae(self.hardware.intake)
        )
        self.hardware.panel_2.button(3).onTrue(DropAlgae(self.hardware.intake))
        self.hardware.panel_2.button(1).onTrue(
            MoveIntake.toRetracted(self.hardware.intake)
        )

        # Arm
        AxisTrigger(self.hardware.panel_2, 0, "down").onTrue(
            RetractArm(self.hardware.arm)
        )
        self.hardware.panel_1.button(2).onTrue(ExtendArm(self.hardware.arm))

        # Climber
        self.hardware.panel_2.button(7).onTrue(ResetClimber(self.hardware.climber))
        self.hardware.panel_2.button(4).onTrue(ReadyClimber(self.hardware.climber))
        self.hardware.panel_2.button(5).onTrue(Climb(self.hardware.climber))
        self.hardware.panel_2.button(6).onTrue(ReleaseClimber(self.hardware.climber))

        # Extra buttons
        self.hardware.panel_1.button(3).onTrue(
            ResetAllButClimber(
                self.hardware.elevator,
                self.hardware.printer,
                self.hardware.arm,
                self.hardware.intake,
            )
        )
        # self.hardware.panel_2.button(1).onTrue()
