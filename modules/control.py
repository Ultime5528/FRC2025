from ultime.module import Module
from modules.hardware import HardwareModule

class ControlModule(Module):
    def __init__(self, hardware: HardwareModule):
        super().__init__()
        self.hardware = hardware

    def robotInit(self) -> None:
        #Default subsystem commands

        #Setup Buttons

        pass
