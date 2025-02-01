import os

from urcl import URCL
from wpilib import DataLogManager, DriverStation

import ports
from ultime.module import Module


class LoggingModule(Module):
    def __init__(self):
        super().__init__()

        can_id_aliases = dict()

        for attr, value in ports.CAN.__dict__.items():
            if not attr.startswith("__"):
                assert isinstance(value, int)
                can_id_aliases[value] = attr

        print("Logging with CAN ID aliases:", can_id_aliases)

        if os.environ.get("GITHUB_ACTIONS"):
            print("Testing in CI: Logging is disabled")
        else:
            print("Not in CI: Logging is enabled")
            URCL.start(can_id_aliases)
            DataLogManager.start()
            DriverStation.startDataLog(DataLogManager.getLog())
