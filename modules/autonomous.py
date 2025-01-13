from sys import modules


class AutonomousModule(modules):
    def __init__(self):
        super().__init__()


    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def autonomousExit(self):
        pass