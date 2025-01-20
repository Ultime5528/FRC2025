from modules.hardware import HardwareModule
from ultime.module import Module


class ControlModule(Module):
    def __init__(self, hardware: HardwareModule):
        super().__init__()
        self.hardware = hardware

        # self.hardware.controller.button(1).onTrue(Command())
