from commands2 import Command

from commands.claw.loadcoral import LoadCoral
from command.claw.drop import Drop
from subsystems.claw import Claw
from ultime.alert import AlertType


class DiagnoseClaw(Command):
    def __init__(self, claw: Claw):
        super().__init__()
        self.addRequirements(claw)
        self.claw = claw

        self._to_loading_command = LoadCoral(claw)
        self._load_command = LoadCoral(claw)
        self._drop_command_level4 = Drop.atLevel4(claw)

        self.tried_loading_flag = False
        self.tried_dropping_flag = False
      
        self._alert_is_at_loading = self.claw.createAlert("Claw is not at loading. Make sure to also move elevator to loading", AlertType.Error)
        self._alert_has_coral = self.claw.createAlert("Claw didn't return the correct value after loading. Is there a coral in the loader? Execution will halt until a coral is placed", AlertType.Warning)
        self._alert_load_failed = self.claw.createAlert("Claw didn't succeed loading. Check sensor", AlertType.Error)
        self._alert_drop_failed = self.claw.createAlert("Claw did not drop coral. Check motors", AlertType.Error)

    def initialize(self):
        self.tried_loading_flag = False
        self.tried_dropping_flag = False
      
        self._alert_is_at_loading.set(False)
        self._alert_has_coral.set(False)
        self._alert_load_failed.set(False)
        self._alert_drop_failed.set(False)

    def execute(self):
        if not self.claw.seesObject() and not self.tried_loading_flag and not self.tried_dropping_flag:
            # There is no coral  
            self._alert_has_coral.set(True)
        elif not self.claw.has_coral and not self._load_command.isScheduled() and not self._drop_command_level4.isScheduled() and not self.tried_loading_flag:
          # Tries to load coral in loader  
          self._load_command.schedule()
          self.tried_loading_flag = True
        elif self.tried_loading_flag and not self._load_command.isScheduled() and not self._drop_command_level4.isScheduled() and not self.claw.has_coral:
          # Tried to load coral but didn't succeed 
          self._alert_load_failed.set(True)
        
        elif not self.tried_dropping_flag and not self._load_command.isScheduled() and not self._drop_command_level4.isScheduled() and self.claw.has_coral:
          # LoadCoral succeeded
          self._drop_command_level4.schedule()
          self.tried_dropping_flag = True

        elif self.tried_dropping_flag and not self._load_command.isScheduled() and not self._drop_command_level4.isScheduled() and self.claw.has_coral:
          # DropCoral failed
          self._alert_drop_failed.set(True)
        
        
          
          

    def isFinished(self) -> bool:
        return False
