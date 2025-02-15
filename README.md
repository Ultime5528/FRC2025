# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2025/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                    |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|---------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| commands/\_\_init\_\_.py                |        0 |        0 |        0 |        0 |    100% |           |
| commands/arm/\_\_init\_\_.py            |        0 |        0 |        0 |        0 |    100% |           |
| commands/arm/extendarm.py               |       22 |        1 |        2 |        1 |     92% |        30 |
| commands/arm/retractarm.py              |       22 |        1 |        2 |        1 |     92% |        30 |
| commands/claw/\_\_init\_\_.py           |        0 |        0 |        0 |        0 |    100% |           |
| commands/claw/autodrop.py               |        9 |        0 |        0 |        0 |    100% |           |
| commands/claw/drop.py                   |       54 |        0 |        0 |        0 |    100% |           |
| commands/claw/loadcoral.py              |       28 |        0 |        2 |        0 |    100% |           |
| commands/climber/\_\_init\_\_.py        |        0 |        0 |        0 |        0 |    100% |           |
| commands/climber/moveclimber.py         |       45 |        3 |        2 |        1 |     91% |20, 24, 29 |
| commands/diagnostics/\_\_init\_\_.py    |        0 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/\_\_init\_\_.py     |        0 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/drive.py            |       56 |       12 |       12 |        4 |     71% |18, 22-25, 68-70, 79-80, 83-85 |
| commands/drivetrain/resetgyro.py        |       17 |        1 |        2 |        1 |     89% |        18 |
| commands/drivetrain/resetpose.py        |       13 |        6 |        0 |        0 |     54% |9-12, 15, 18 |
| commands/elevator/\_\_init\_\_.py       |        0 |        0 |        0 |        0 |    100% |           |
| commands/elevator/maintainelevator.py   |       16 |        0 |        2 |        0 |    100% |           |
| commands/elevator/manualmoveelevator.py |       28 |        1 |        0 |        0 |     96% |        32 |
| commands/elevator/moveelevator.py       |       83 |        2 |        4 |        2 |     95% |  129, 134 |
| commands/elevator/resetelevator.py      |       24 |        1 |        4 |        1 |     93% |        29 |
| commands/intake/\_\_init\_\_.py         |        0 |        0 |        0 |        0 |    100% |           |
| commands/intake/dropalgae.py            |       27 |        0 |        2 |        0 |    100% |           |
| commands/intake/grabalgae.py            |       29 |        0 |        2 |        0 |    100% |           |
| commands/intake/moveintake.py           |       45 |        2 |        4 |        2 |     92% |    63, 66 |
| commands/intake/resetintake.py          |       21 |        9 |        2 |        0 |     52% |14-15, 18-24, 27, 30-31 |
| commands/printer/\_\_init\_\_.py        |        0 |        0 |        0 |        0 |    100% |           |
| commands/printer/manualmoveprinter.py   |       31 |        0 |        4 |        1 |     97% |  31->exit |
| commands/printer/moveprinter.py         |       91 |        2 |        4 |        2 |     96% |  122, 127 |
| commands/printer/resetright.py          |       21 |        0 |        2 |        0 |    100% |           |
| conftest.py                             |        1 |        0 |        0 |        0 |    100% |           |
| modules/\_\_init\_\_.py                 |        0 |        0 |        0 |        0 |    100% |           |
| modules/armcollision.py                 |       26 |        0 |       10 |        0 |    100% |           |
| modules/autonomous.py                   |       18 |        2 |        4 |        2 |     82% |    30, 34 |
| modules/batterysim.py                   |       11 |        2 |        0 |        0 |     82% |     14-15 |
| modules/control.py                      |        6 |        0 |        0 |        0 |    100% |           |
| modules/dashboard.py                    |       90 |        2 |       12 |        3 |     95% |115, 119->122, 127 |
| modules/diagnostics.py                  |       40 |        8 |        4 |        1 |     75% |31-34, 37-38, 42, 52 |
| modules/hardware.py                     |       29 |        0 |        0 |        0 |    100% |           |
| modules/logging.py                      |       18 |        1 |        6 |        1 |     92% |        25 |
| modules/propertysavechecker.py          |       35 |       17 |       16 |        2 |     39% |22-26, 31-47 |
| ports.py                                |       34 |        0 |        0 |        0 |    100% |           |
| properties.py                           |       95 |       79 |       18 |        1 |     15% |17-25, 35-59, 63-79, 83-96, 100-146, 150-184 |
| robot.py                                |       27 |        0 |        0 |        0 |    100% |           |
| subsystems/\_\_init\_\_.py              |        0 |        0 |        0 |        0 |    100% |           |
| subsystems/arm.py                       |       43 |        3 |        4 |        1 |     91% |33, 49, 55 |
| subsystems/claw.py                      |       27 |        1 |        0 |        0 |     96% |        33 |
| subsystems/climber.py                   |       66 |        2 |        8 |        2 |     95% |45->exit, 68, 90 |
| subsystems/drivetrain.py                |       97 |        8 |        4 |        2 |     90% |94->exit, 121, 141, 144, 153-162, 245 |
| subsystems/elevator.py                  |      124 |        5 |       14 |        2 |     95% |66->exit, 116, 148, 157, 160, 163 |
| subsystems/intake.py                    |       91 |        8 |        8 |        4 |     88% |50->exit, 58-59, 74, 83, 113, 119, 122, 125 |
| subsystems/printer.py                   |      128 |        4 |       16 |        2 |     96% |68->exit, 121->129, 160, 166, 169, 172 |
| tests/\_\_init\_\_.py                   |        0 |        0 |        0 |        0 |    100% |           |
| tests/test\_arm.py                      |      129 |        0 |        0 |        0 |    100% |           |
| tests/test\_claw.py                     |      113 |        0 |        0 |        0 |    100% |           |
| tests/test\_climber.py                  |       56 |        0 |        0 |        0 |    100% |           |
| tests/test\_common.py                   |        1 |        0 |        0 |        0 |    100% |           |
| tests/test\_drivetrain.py               |       10 |        0 |        0 |        0 |    100% |           |
| tests/test\_elevator.py                 |      162 |        0 |        4 |        0 |    100% |           |
| tests/test\_intake.py                   |       65 |        0 |        0 |        0 |    100% |           |
| tests/test\_printer.py                  |      159 |        4 |        8 |        2 |     96% |229-230, 270-271 |
| ultime/\_\_init\_\_.py                  |        0 |        0 |        0 |        0 |    100% |           |
| ultime/affinecontroller.py              |       77 |       77 |        2 |        0 |      0% |     1-122 |
| ultime/alert.py                         |       74 |        6 |       12 |        3 |     90% |42, 70, 83, 87, 98, 101, 106->105 |
| ultime/autoproperty.py                  |       61 |       34 |       22 |        2 |     35% |35, 39, 53-106 |
| ultime/axistrigger.py                   |        8 |        8 |        2 |        0 |      0% |      1-16 |
| ultime/command.py                       |       34 |        3 |        2 |        1 |     89% |     38-40 |
| ultime/coroutinecommand.py              |       27 |       27 |        6 |        0 |      0% |      1-41 |
| ultime/gyro.py                          |      122 |       51 |       10 |        5 |     58% |19, 28->exit, 31->exit, 34->exit, 37->exit, 40, 43, 49-51, 56-62, 65, 68, 71, 74, 79-83, 86, 89, 92, 95, 114, 122, 126, 131-135, 138, 141, 144, 147, 152-161, 164, 167, 170-171, 174-175, 178, 181 |
| ultime/immutable.py                     |        6 |        2 |        0 |        0 |     67% |      3, 8 |
| ultime/linearinterpolator.py            |       25 |       25 |        6 |        0 |      0% |      1-36 |
| ultime/module.py                        |       78 |       10 |       16 |        1 |     88% |15, 21, 24, 27, 45, 51, 63, 66, 69, 97 |
| ultime/modulerobot.py                   |       43 |        3 |        4 |        2 |     89% |18->exit, 24->exit, 55, 58, 61 |
| ultime/subsystem.py                     |       27 |        3 |        4 |        0 |     90% |11, 15, 37 |
| ultime/swerve.py                        |       63 |        1 |        2 |        1 |     97% |14, 55->exit |
| ultime/swerveconfig.py                  |       41 |        0 |        0 |        0 |    100% |           |
| ultime/switch.py                        |       66 |        6 |       42 |        7 |     88% |29->exit, 41, 53, 57, 67, 71, 81 |
| ultime/tests/\_\_init\_\_.py            |        7 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_alert.py             |       41 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_commands.py          |       75 |        4 |       54 |        4 |     94% |60->52, 62-65, 78->68, 80-83 |
| ultime/tests/test\_modules.py           |       41 |        1 |        0 |        0 |     98% |        17 |
| ultime/tests/test\_properties.py        |        3 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_subsystems.py        |       17 |        0 |        8 |        0 |    100% |           |
| ultime/tests/test\_switch.py            |       33 |        0 |        0 |        0 |    100% |           |
| ultime/tests/utils.py                   |       60 |       12 |       10 |        0 |     83% |25-26, 37-41, 51-55 |
| ultime/trapezoidalmotion.py             |      104 |       29 |       42 |        6 |     65% |20, 22, 40-44, 59->exit, 73-91, 110-111, 168, 199-200, 203 |
|                               **TOTAL** | **3516** |  **489** |  **432** |   **73** | **84%** |           |


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