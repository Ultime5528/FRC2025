import inspect
from functools import wraps

from wpiutil import Sendable


class Module(Sendable):
    def __init__(self):
        super().__init__()

    def robotPeriodic(self) -> None:
        pass

    def simulationInit(self) -> None:
        pass

    def simulationPeriodic(self) -> None:
        pass

    def disabledInit(self) -> None:
        pass

    def disabledPeriodic(self) -> None:
        pass

    def disabledExit(self) -> None:
        pass

    def autonomousInit(self) -> None:
        pass

    def autonomousPeriodic(self) -> None:
        pass

    def autonomousExit(self) -> None:
        pass

    def teleopInit(self) -> None:
        pass

    def teleopPeriodic(self) -> None:
        pass

    def teleopExit(self) -> None:
        pass

    def testInit(self) -> None:
        pass

    def testPeriodic(self) -> None:
        pass

    def testExit(self) -> None:
        pass

    def driverStationConnected(self) -> None:
        pass


class ModuleList(Module):
    def __init__(self, *modules: Module):
        super().__init__()
        self.modules = modules
        self._setup()

    def addModules(self, *modules):
        self.modules = self.modules + modules
        self._setup()

    def _setup(self):
        for module in self.modules:
            if not isinstance(module, Module):
                raise TypeError(
                    "Every module must be an instance of a Module subclass :", module
                )

        self._methods: dict[str, list[callable]] = {
            name: []
            for name, attr in Module.__dict__.items()
            if inspect.isfunction(attr)
        }

        for name, methods in self._methods.items():
            for module in self.modules:
                module_method = getattr(module, name)
                declaring_classes = []
                for cls in inspect.getmro(module_method.__self__.__class__):
                    if module_method.__name__ in cls.__dict__:
                        declaring_classes.append(cls)

                if len(declaring_classes) > 1:
                    methods.append(module_method)

            if len(methods) > 0:

                @wraps(getattr(self, name))
                def call(_):
                    for method in methods:
                        method()

                setattr(self, name, call)
