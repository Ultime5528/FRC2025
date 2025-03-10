import pytest
import os


@pytest.mark.specific
def test_auonome_level_4():

    path = "deploy/pathplanner/autos"
    for filename in os.listdir(path):
        if filename.endswith(".auto"):
            with open(os.path.join(path, filename)) as file:
                assert not '.toLevel1' in file.read()
                assert not '.toLevel2' in file.read()
                assert not '.toLevel3' in file.read()
                assert '.toLevel4' in file.read()
