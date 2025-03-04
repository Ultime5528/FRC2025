from typing import Callable

from commands2 import FunctionalCommand


class RunOnce(FunctionalCommand):
    def __init__(self, to_run: Callable):
        super().__init__(to_run, lambda: None, lambda interrupted: None, lambda: True)
