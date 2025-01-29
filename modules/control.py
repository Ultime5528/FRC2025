from commands.arm.extendarm import ExtendArm
from commands.arm.retractarm import RetractArm
from modules.hardware import HardwareModule
from ultime.module import Module


class ControlModule(Module):
    def __init__(self, hardware: HardwareModule):
        super().__init__()
        self.hardware = hardware

        # self.hardware.controller.button(1).onTrue(Command())
        self.hardware.controller.button(1).onTrue(RetractArm(hardware.arm))
        self.hardware.controller.button(2).onTrue(ExtendArm(hardware.arm))
