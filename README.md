# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2025/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                             |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|--------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| commands/\_\_init\_\_.py         |        0 |        0 |        0 |        0 |    100% |           |
| modules/\_\_init\_\_.py          |        0 |        0 |        0 |        0 |    100% |           |
| modules/hardware.py              |        8 |        0 |        0 |        0 |    100% |           |
| ports.py                         |       17 |       17 |        0 |        0 |      0% |      1-35 |
| properties.py                    |       93 |       93 |       16 |        0 |      0% |     1-179 |
| robot.py                         |       45 |        3 |        4 |        2 |     90% |25->exit, 31->exit, 62, 65, 68 |
| subsystems/\_\_init\_\_.py       |        0 |        0 |        0 |        0 |    100% |           |
| subsystems/drivetrain.py         |        9 |        1 |        0 |        0 |     89% |        14 |
| tests/\_\_init\_\_.py            |        0 |        0 |        0 |        0 |    100% |           |
| tests/test\_common.py            |        1 |        0 |        0 |        0 |    100% |           |
| tests/test\_drivetrain.py        |        0 |        0 |        0 |        0 |    100% |           |
| ultime/\_\_init\_\_.py           |        0 |        0 |        0 |        0 |    100% |           |
| ultime/affinecontroller.py       |       77 |       77 |        2 |        0 |      0% |     1-122 |
| ultime/autoproperty.py           |       58 |       35 |       20 |        0 |     29% |33-35, 39, 50-102 |
| ultime/axistrigger.py            |        8 |        8 |        2 |        0 |      0% |      1-16 |
| ultime/command.py                |        7 |        7 |        0 |        0 |      0% |      1-11 |
| ultime/coroutinecommand.py       |       27 |       27 |        6 |        0 |      0% |      1-41 |
| ultime/gyro.py                   |      122 |      122 |       10 |        0 |      0% |     1-181 |
| ultime/immutable.py              |        6 |        6 |        0 |        0 |      0% |       1-8 |
| ultime/linearinterpolator.py     |       25 |       25 |        6 |        0 |      0% |      1-36 |
| ultime/module.py                 |       66 |        8 |       20 |        2 |     86% |51, 54, 57, 71, 96-97, 103-104 |
| ultime/subsystem.py              |       23 |       17 |        4 |        0 |     22% | 10, 13-34 |
| ultime/switch.py                 |       66 |        8 |       42 |        7 |     86% |29->exit, 41, 53, 57, 67, 71, 81, 84, 87 |
| ultime/tests/\_\_init\_\_.py     |        5 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_commands.py   |       75 |       46 |       54 |        3 |     25% |21-27, 32, 37-40, 47-107 |
| ultime/tests/test\_properties.py |        3 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_subsystems.py |       17 |        0 |        8 |        0 |    100% |           |
| ultime/tests/test\_switch.py     |       33 |        0 |        0 |        0 |    100% |           |
| ultime/tests/utils.py            |       17 |        4 |        6 |        2 |     74% |15, 21-22, 24 |
| ultime/trapezoidalmotion.py      |      104 |      104 |       42 |        0 |      0% |     1-203 |
|                        **TOTAL** |  **912** |  **608** |  **242** |   **16** | **32%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/Ultime5528/FRC2025/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2025/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Ultime5528/FRC2025/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2025/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2FUltime5528%2FFRC2025%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2025/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.