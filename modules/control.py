import robot
from commands.vision.alignwithalgae import AlignWithAlgae
from modules.algaevision import AlgaeVisionModule
from modules.hardware import HardwareModule
from robot import Robot
from ultime.module import Module


class ControlModule(Module):
    def __init__(self, hardware: HardwareModule, vision_algae: AlgaeVisionModule):
        super().__init__()
        self.hardware = hardware
        self.algae_vision = vision_algae

        self.hardware.controller.rightTrigger().whileTrue(AlignWithAlgae(hardware.drivetrain, self.algae_vision, hardware.controller))
        # self.hardware.controller.button(1).onTrue(Command())
