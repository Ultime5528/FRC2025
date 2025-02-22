from modules.hardware import HardwareModule
from ultime.module import Module


class ControlModule(Module):
    def __init__(self, hardware: HardwareModule):
        super().__init__()
        self.hardware = hardware

        self.setupButtons()

    def setupButtons(self):
        def setupButtons(self):
            """
            Bind commands to buttons on controllers and joysticks
            """
            # Example code for xbox_controller
            # self.hardware.controller.leftTrigger().whileTrue(
            #     AlignedPickUp(self.drivetrain, self.intake, self.vision_pick_up)
            # )

            # Copilot's panel
            AxisTrigger(self.panel_1, 1, "down").whileTrue(ExtendClimber(self.climber_left))
            AxisTrigger(self.panel_1, 1, "up").whileTrue(RetractClimber(self.climber_left))
            self.panel_1.button(3).onTrue(PickUp(self.intake))
            self.panel_1.button(2).onTrue(Drop(self.intake))
            self.panel_1.button(1).onTrue(MovePivot.toSpeakerClose(self.pivot))

            AxisTrigger(self.panel_2, 1, "down").whileTrue(
                ExtendClimber(self.climber_right)
            )
            AxisTrigger(self.panel_2, 1, "up").whileTrue(RetractClimber(self.climber_right))
            self.panel_2.button(2).onTrue(
                PrepareAndShootAndMovePivotLoading(self.shooter, self.pivot, self.intake)
            )
            self.panel_2.button(5).onTrue(
                ShootAndMovePivotLoading(self.shooter, self.intake, self.pivot)
            )
            self.panel_2.button(1).onTrue(MovePivot.toAmp(self.pivot))
            self.panel_2.button(4).onTrue(ResetPivotDown(self.pivot))
