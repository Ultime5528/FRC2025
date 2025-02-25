import os

from wpilib import DataLogManager, DriverStation

import ports
from ultime.module import Module
from ultime.timethis import print_stats_every


class LoggingModule(Module):
    def __init__(self):
        super().__init__()

        can_id_aliases = dict()

        for attr, value in ports.CAN.__dict__.items():
            if not attr.startswith("__"):
                assert isinstance(value, int)
                can_id_aliases[value] = attr

        print("Logging with CAN ID aliases:", can_id_aliases)

        if os.environ.get("CI"):
            print("Testing in CI: URCL is disabled")
        else:
            print("Not in CI: URCL is enabled")

            # urcl.URCL.start(can_id_aliases)

        DataLogManager.start()
        DriverStation.startDataLog(DataLogManager.getLog())

    def robotPeriodic(self) -> None:
        print_stats_every(5.0, "ns")
