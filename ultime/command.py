from typing import Type

from commands2 import Command


def ignore_requirements(reqs: list[str]):
    def _ignore(actual_cls: Type[Command]) -> Type[Command]:
        setattr(actual_cls, "__ignore_reqs", reqs)
        return actual_cls

    return _ignore
