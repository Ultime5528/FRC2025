import os


def test_auto_level_4():

    path = "deploy/pathplanner/autos"
    for filename in os.listdir(path):
        if filename.endswith(".auto"):
            with open(os.path.join(path, filename)) as file:
                content = file.read()
                assert not "MoveElevator.toLevel1" in content, filename
                assert not "MoveElevator.toLevel2" in content, filename
                assert not "MoveElevator.toLevel3" in content, filename
                assert "MoveElevator.toLevel4" in content, filename
