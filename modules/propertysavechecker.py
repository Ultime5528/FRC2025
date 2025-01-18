import wpilib
from ntcore import NetworkTableInstance
from wpilib import DriverStation, Timer, RobotBase

from properties import loop_delay, entry_name_check_time, entry_name_check_mirror
from ultime.module import Module
from ultime.autoproperty import mode, PropertyMode


class PropertySaveCheckerModule(Module):
    def __init__(self):
        super().__init__()
        inst = NetworkTableInstance.getDefault()
        self.entry_check_time = inst.getEntry(entry_name_check_time)
        self.entry_check_mirror = inst.getEntry(entry_name_check_mirror)
        self.timer_check = Timer()


    def robotPeriodic(self) -> None:
        # TODO change condition check in constructor to log condition
        # i.e. disabling property save check, simulation currently
        # or PropertyMode is Local
        if not RobotBase.isSimulation() and mode != PropertyMode.Local:
            # TODO add wpilib.Alert in module (add Modules to Diagnostics ?)
            if DriverStation.isFMSAttached():
                if self.timer_check.advanceIfElapsed(10.0):
                    wpilib.reportWarning(
                        f"FMS is connected, but PropertyMode is not Local: {mode}"
                    )

            elif DriverStation.isDSAttached():
                self.timer_check.start()
                current_time = wpilib.getTime()
                self.entry_check_time.setDouble(current_time)
                if self.timer_check.advanceIfElapsed(loop_delay):
                    mirror_time = self.entry_check_mirror.getDouble(0.0)
                    if current_time - mirror_time < 5.0:
                        print("Save loop running")
                    else:
                        raise RuntimeError(
                            f"Save loop is not running ({current_time=:.2f}, {mirror_time=:.2f})"
                        )
