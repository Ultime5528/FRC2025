from ultime.alert import AlertType, Alert


class AlertCreator:
    def __init__(self):
        super().__init__()
        self._registered_alerts = []
        self.running_test = self.createAlert("Diagnosing component...", AlertType.Info)

    def createAlert(self, text: str, alert_type: AlertType) -> Alert:
        alert = Alert(text, alert_type, self.getName() + "/Alerts")
        self._registered_alerts.append(alert)
        return alert

    def clearAlerts(self) -> None:
        for alert in self._registered_alerts:
            alert.set(False)

    def getName(self) -> str:
        return self.__class__.__name__
