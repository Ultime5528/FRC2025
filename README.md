# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2025/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                    |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|---------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| commands/\_\_init\_\_.py                |        0 |        0 |        0 |        0 |    100% |           |
| commands/claw/drop.py                   |       53 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/\_\_init\_\_.py    |        0 |        0 |        0 |        0 |    100% |           |
| commands/elevator/\_\_init\_\_.py       |        0 |        0 |        0 |        0 |    100% |           |
| commands/elevator/maintainelevator.py   |       16 |        0 |        2 |        0 |    100% |           |
| commands/elevator/manualmoveelevator.py |       28 |        1 |        0 |        0 |     96% |        32 |
| commands/elevator/moveelevator.py       |       63 |        2 |        4 |        2 |     94% |    92, 97 |
| commands/elevator/resetelevator.py      |       21 |        0 |        2 |        0 |    100% |           |
| modules/\_\_init\_\_.py                 |        0 |        0 |        0 |        0 |    100% |           |
| modules/autonomous.py                   |       18 |        2 |        4 |        2 |     82% |    30, 34 |
| modules/batterysim.py                   |       11 |        2 |        0 |        0 |     82% |     14-15 |
| modules/control.py                      |        6 |        0 |        0 |        0 |    100% |           |
| modules/dashboard.py                    |       47 |        2 |       12 |        3 |     92% |56, 60->63, 68 |
| modules/diagnostics.py                  |       40 |        8 |        4 |        1 |     75% |31-34, 37-38, 42, 52 |
| modules/hardware.py                     |       16 |        0 |        0 |        0 |    100% |           |
| modules/propertysavechecker.py          |       35 |       17 |       16 |        2 |     39% |22-26, 31-47 |
| ports.py                                |       19 |        0 |        0 |        0 |    100% |           |
| properties.py                           |       93 |       75 |       16 |        1 |     17% |19-27, 37-59, 63-79, 83-96, 100-142, 146-180 |
| robot.py                                |       23 |        0 |        0 |        0 |    100% |           |
| subsystems/\_\_init\_\_.py              |        0 |        0 |        0 |        0 |    100% |           |
| subsystems/claw.py                      |       15 |        0 |        0 |        0 |    100% |           |
| subsystems/drivetrain.py                |       13 |        1 |        0 |        0 |     92% |        13 |
| subsystems/elevator.py                  |      110 |        6 |       12 |        2 |     93% |57->exit, 101, 118, 130, 139, 142, 145 |
| tests/\_\_init\_\_.py                   |        0 |        0 |        0 |        0 |    100% |           |
| tests/conftest.py                       |        1 |        0 |        0 |        0 |    100% |           |
| tests/test\_claw.py                     |       71 |        0 |        0 |        0 |    100% |           |
| tests/test\_common.py                   |        1 |        0 |        0 |        0 |    100% |           |
| tests/test\_drivetrain.py               |        0 |        0 |        0 |        0 |    100% |           |
| tests/test\_elevator.py                 |      118 |        0 |        4 |        0 |    100% |           |
| ultime/\_\_init\_\_.py                  |        0 |        0 |        0 |        0 |    100% |           |
| ultime/affinecontroller.py              |       77 |       77 |        2 |        0 |      0% |     1-122 |
| ultime/alert.py                         |       74 |        6 |       12 |        3 |     90% |42, 70, 83, 87, 98, 101, 106->105 |
| ultime/autoproperty.py                  |       58 |       31 |       20 |        2 |     37% |35, 39, 53-102 |
| ultime/axistrigger.py                   |        8 |        8 |        2 |        0 |      0% |      1-16 |
| ultime/command.py                       |        7 |        4 |        0 |        0 |     43% |      7-11 |
| ultime/coroutinecommand.py              |       27 |       27 |        6 |        0 |      0% |      1-41 |
| ultime/gyro.py                          |      122 |      122 |       10 |        0 |      0% |     1-181 |
| ultime/immutable.py                     |        6 |        2 |        0 |        0 |     67% |      3, 8 |
| ultime/linearinterpolator.py            |       25 |       25 |        6 |        0 |      0% |      1-36 |
| ultime/module.py                        |       78 |       10 |       16 |        1 |     88% |15, 21, 24, 27, 45, 51, 63, 66, 69, 97 |
| ultime/modulerobot.py                   |       43 |        3 |        4 |        2 |     89% |18->exit, 24->exit, 55, 58, 61 |
| ultime/subsystem.py                     |       27 |        3 |        4 |        0 |     90% |11, 15, 37 |
| ultime/switch.py                        |       66 |        6 |       42 |        7 |     88% |29->exit, 41, 53, 57, 67, 71, 81 |
| ultime/tests/\_\_init\_\_.py            |        7 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_alert.py             |       41 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_commands.py          |       74 |       11 |       54 |        5 |     81% |59->51, 61-64, 71-82, 98->95, 106 |
| ultime/tests/test\_modules.py           |       41 |        1 |        0 |        0 |     98% |        17 |
| ultime/tests/test\_properties.py        |        3 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_subsystems.py        |       17 |        0 |        8 |        0 |    100% |           |
| ultime/tests/test\_switch.py            |       33 |        0 |        0 |        0 |    100% |           |
| ultime/tests/utils.py                   |       50 |       10 |        8 |        0 |     83% |25-26, 37-40, 49-52 |
| ultime/trapezoidalmotion.py             |      104 |       33 |       42 |       11 |     59% |20, 22, 40-44, 59->exit, 73-91, 110-111, 136->exit, 161, 168, 176, 188, 194, 199-200, 203 |
|                               **TOTAL** | **1806** |  **495** |  **312** |   **44** | **70%** |           |


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