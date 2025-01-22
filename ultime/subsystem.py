from abc import abstractmethod

import commands2
from wpiutil import SendableBuilder

from ultime.alert import AlertType, Alert


class Subsystem(commands2.Subsystem):
    def createAlert(self, text: str, alert_type: AlertType) -> Alert:
        return Alert(text, alert_type, self.getName() + "/Alerts")

    @abstractmethod
    def getCurrentDrawAmps(self) -> float:
        raise NotImplementedError(
            f"Subsystem {self.getName()} does not implement getCurrentDrawAmps"
        )

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def currentCommandName():
            cmd = self.getCurrentCommand()
            if cmd:
                return cmd.getName()
            else:
                return "None"

        def defaultCommandName():
            cmd = self.getDefaultCommand()
            if cmd:
                return cmd.getName()
            else:
                return "None"

        def noop(_):
            pass

        builder.setSmartDashboardType("List")
        builder.addStringProperty("Current command", currentCommandName, noop)
        builder.addStringProperty("Default command", defaultCommandName, noop)
