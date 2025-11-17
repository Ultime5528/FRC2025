from dataclasses import dataclass


@dataclass
class PoseFrame:
    questPose3d: object
    dataTimestamp: float
    appTimestamp: float
    frameCount: int
