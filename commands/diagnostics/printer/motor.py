from commands2 import SequentialCommandGroup, FunctionalCommand
from commands2.cmd import parallel, runOnce
from wpilib import RobotController, DataLogManager

from commands.printer.moveprinter import MovePrinter
from commands.printer.resetprinter import ResetPrinterRight
from subsystems.printer import Printer
from ultime.autoproperty import autoproperty
from ultime.command import ignore_requirements, WaitCommand
from ultime.proxy import proxy


@ignore_requirements(["printer"])
class DiagnoseMotor(SequentialCommandGroup):
    voltage_change_threshold = autoproperty(0.5)

    def __init__(self, printer: Printer):
        super().__init__(
            WaitCommand(0.1),
            runOnce(proxy(self.before_moving)),
            parallel(
                MovePrinter.toLeft(printer),
                FunctionalCommand(
                    lambda: None,
                    proxy(self.during_moving),
                    lambda _: None,
                    lambda: printer.isLeft(),
                ),
            ),
            WaitCommand(0.1),
            runOnce(proxy(self.after_move)),
            ResetPrinterRight(printer),
        )
        self.printer = printer
        self.voltage_before = None
        self.voltage_during = None
        self.voltage_after = None

    def before_moving(self):
        self.voltage_before = RobotController.getBatteryVoltage()

    def during_moving(self):
        self.voltage_during = RobotController.getBatteryVoltage()

    def after_move(self):
        self.voltage_after = RobotController.getBatteryVoltage()

        voltage_delta_before = self.voltage_before - self.voltage_during
        voltage_delta_after = self.voltage_after - self.voltage_during
        DataLogManager.log(
            "Printer diagnostics: motor voltage delta before: "
            + str(voltage_delta_before)
        )
        DataLogManager.log(
            "Printer diagnostics: motor voltage delta after: "
            + str(voltage_delta_after)
        )
        if (
            voltage_delta_after < self.voltage_change_threshold
            or voltage_delta_before < self.voltage_change_threshold
        ):
            self.printer.alert_motor.set(True)
