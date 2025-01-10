import commands2
import wpilib
from wpiutil import SendableBuilder


class Subsystem(commands2.Subsystem):
    def createAlert(self, text: str, alert_type: wpilib.Alert.AlertType) -> wpilib.Alert:
        return wpilib.Alert(self.getName() + "/Alerts", text, alert_type)

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
