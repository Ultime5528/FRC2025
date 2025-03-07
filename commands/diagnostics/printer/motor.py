from commands2 import SequentialCommandGroup, FunctionalCommand
from commands2.cmd import parallel, runOnce
from wpilib import RobotController, DataLogManager, PowerDistribution

import ports
from commands.printer.moveprinter import MovePrinter
from commands.printer.resetprinter import ResetPrinterRight
from subsystems.printer import Printer
from ultime.autoproperty import autoproperty
from ultime.command import ignore_requirements, WaitCommand
from ultime.proxy import proxy


@ignore_requirements(["printer"])
class DiagnoseMotor(SequentialCommandGroup):
    voltage_change_threshold = autoproperty(0.5)

    def __init__(self, printer: Printer, pdp: PowerDistribution):
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
        self.pdp = pdp

    def before_moving(self):
        if self.pdp.getCurrent(ports.PDP.printer_motor) > 0.1:
            DataLogManager.log(
                f"Printer diagnostics: Motor current measured too high. {self.pdp.getCurrent(ports.PDP.printer_motor)}"
            )
            self.printer.alert_motor_hi.set(True)

    def during_moving(self):
        if self.pdp.getCurrent(ports.PDP.printer_motor) < 0.1:
            DataLogManager.log(
                f"Printer diagnostics: Motor current measured too low. {self.pdp.getCurrent(ports.PDP.printer_motor)}"
            )
            self.printer.alert_motor_lo.set(True)

    def after_move(self):
        if self.pdp.getCurrent(ports.PDP.printer_motor) > 0.1:
            DataLogManager.log(
                f"Printer diagnostics: Motor current measured too low. {self.pdp.getCurrent(ports.PDP.printer_motor)}"
            )
            self.printer.alert_motor_hi.set(True)
