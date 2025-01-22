# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2025/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                             |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|--------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| commands/\_\_init\_\_.py         |        0 |        0 |        0 |        0 |    100% |           |
| modules/\_\_init\_\_.py          |        0 |        0 |        0 |        0 |    100% |           |
| modules/autonomous.py            |       18 |        2 |        4 |        2 |     82% |    30, 34 |
| modules/batterysim.py            |       11 |        0 |        0 |        0 |    100% |           |
| modules/control.py               |        6 |        0 |        0 |        0 |    100% |           |
| modules/hardware.py              |       10 |        0 |        0 |        0 |    100% |           |
| modules/propertysavechecker.py   |       35 |       17 |       16 |        2 |     39% |22-26, 31-47 |
| ports.py                         |       17 |       17 |        0 |        0 |      0% |      1-35 |
| properties.py                    |       93 |       75 |       16 |        1 |     17% |19-27, 37-59, 63-79, 83-96, 100-142, 146-180 |
| robot.py                         |       18 |        0 |        0 |        0 |    100% |           |
| subsystems/\_\_init\_\_.py       |        0 |        0 |        0 |        0 |    100% |           |
| subsystems/drivetrain.py         |       11 |        1 |        0 |        0 |     91% |        17 |
| tests/\_\_init\_\_.py            |        0 |        0 |        0 |        0 |    100% |           |
| tests/conftest.py                |        1 |        0 |        0 |        0 |    100% |           |
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
| ultime/module.py                 |       70 |        8 |       18 |        1 |     90% |12, 18, 30, 36, 48, 51, 54, 82 |
| ultime/modulerobot.py            |       41 |        3 |        4 |        2 |     89% |12->exit, 21->exit, 52, 55, 58 |
| ultime/subsystem.py              |       27 |       18 |        4 |        0 |     29% |12, 16, 21-42 |
| ultime/switch.py                 |       66 |        8 |       42 |        7 |     86% |29->exit, 41, 53, 57, 67, 71, 81, 84, 87 |
| ultime/tests/\_\_init\_\_.py     |        6 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_commands.py   |       74 |       46 |       54 |        3 |     24% |20-26, 31, 36-39, 46-106 |
| ultime/tests/test\_modules.py    |       32 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_properties.py |        3 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_subsystems.py |       17 |        0 |        8 |        0 |    100% |           |
| ultime/tests/test\_switch.py     |       33 |        0 |        0 |        0 |    100% |           |
| ultime/tests/utils.py            |       47 |       10 |        8 |        2 |     78% |19, 25-26, 28, 37-39, 47-49 |
| ultime/trapezoidalmotion.py      |      104 |      104 |       42 |        0 |      0% |     1-203 |
|                        **TOTAL** | **1071** |  **616** |  **262** |   **20** | **40%** |           |


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