from abc import abstractmethod

import commands2
from wpiutil import SendableBuilder

from ultime.alert import AlertType, Alert


class Subsystem(commands2.Subsystem):
    def __init__(self):
        super().__init__()
        self._registered_alerts = []
        self._alert_running_test = self.createAlert(
            "Subsystem is running test...", AlertType.Info
        )

    def setIsRunningTest(self, is_running: bool) -> None:
        self._alert_running_test.set(is_running)

    def isRunningTest(self) -> bool:
        return self._alert_running_test.get()

    def createAlert(self, text: str, alert_type: AlertType) -> Alert:
        alert = Alert(text, alert_type, self.getName() + "/Alerts")
        self._registered_alerts.append(alert)
        return alert

    def clearAlerts(self) -> None:
        for alert in self._registered_alerts:
            alert.set(False)

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
