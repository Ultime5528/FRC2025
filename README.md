# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2025/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                    |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|---------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| commands/\_\_init\_\_.py                |        0 |        0 |        0 |        0 |    100% |           |
| commands/arm/\_\_init\_\_.py            |        0 |        0 |        0 |        0 |    100% |           |
| commands/arm/extendarm.py               |       31 |        3 |        6 |        3 |     84% |25-26, 38->exit, 40 |
| commands/arm/retractarm.py              |       31 |        1 |        6 |        2 |     92% |38->exit, 40 |
| commands/claw/\_\_init\_\_.py           |        0 |        0 |        0 |        0 |    100% |           |
| commands/claw/autodrop.py               |        9 |        0 |        0 |        0 |    100% |           |
| commands/claw/drop.py                   |       56 |        0 |        0 |        0 |    100% |           |
| commands/claw/loadcoral.py              |       30 |        0 |        4 |        1 |     97% |  39->exit |
| commands/claw/retractcoral.py           |       23 |        6 |        0 |        0 |     74% |20, 23-24, 27, 30-31 |
| commands/climber/\_\_init\_\_.py        |        0 |        0 |        0 |        0 |    100% |           |
| commands/climber/moveclimber.py         |       45 |        3 |        2 |        1 |     91% |20, 24, 29 |
| commands/climber/resetclimber.py        |       25 |        1 |        6 |        1 |     94% |        31 |
| commands/diagnostics/\_\_init\_\_.py    |        0 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/\_\_init\_\_.py     |        0 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/drive.py            |       56 |       12 |       12 |        4 |     71% |18, 22-25, 68-70, 79-80, 83-85 |
| commands/drivetrain/drivetoposes.py     |       67 |       36 |        4 |        0 |     44% |13, 19-26, 43-47, 53, 59-72, 82-84, 87-114, 117, 120, 123, 129 |
| commands/drivetrain/resetgyro.py        |       17 |        1 |        2 |        1 |     89% |        18 |
| commands/drivetrain/resetpose.py        |       13 |        6 |        0 |        0 |     54% |9-12, 15, 18 |
| commands/elevator/\_\_init\_\_.py       |        0 |        0 |        0 |        0 |    100% |           |
| commands/elevator/maintainelevator.py   |       16 |        0 |        2 |        0 |    100% |           |
| commands/elevator/manualmoveelevator.py |       28 |        0 |        0 |        0 |    100% |           |
| commands/elevator/moveelevator.py       |       83 |        1 |        4 |        1 |     98% |       134 |
| commands/elevator/resetelevator.py      |       24 |        1 |        4 |        1 |     93% |        29 |
| commands/intake/\_\_init\_\_.py         |        0 |        0 |        0 |        0 |    100% |           |
| commands/intake/dropalgae.py            |       27 |        0 |        2 |        0 |    100% |           |
| commands/intake/grabalgae.py            |       29 |        0 |        2 |        0 |    100% |           |
| commands/intake/moveintake.py           |       51 |        1 |        4 |        1 |     96% |        76 |
| commands/intake/resetintake.py          |       22 |        0 |        2 |        0 |    100% |           |
| commands/prepareloading.py              |       12 |        0 |        0 |        0 |    100% |           |
| commands/printer/\_\_init\_\_.py        |        0 |        0 |        0 |        0 |    100% |           |
| commands/printer/manualmoveprinter.py   |       31 |        0 |        4 |        1 |     97% |  31->exit |
| commands/printer/moveprinter.py         |       93 |        2 |        4 |        2 |     96% |  123, 128 |
| commands/printer/resetprinter.py        |       21 |        0 |        2 |        0 |    100% |           |
| commands/printer/scanprinter.py         |       50 |       22 |       14 |        0 |     44% |28-31, 34-45, 48-62, 68-69 |
| commands/resetall.py                    |       18 |        0 |        0 |        0 |    100% |           |
| conftest.py                             |        1 |        0 |        0 |        0 |    100% |           |
| modules/\_\_init\_\_.py                 |        0 |        0 |        0 |        0 |    100% |           |
| modules/armcollision.py                 |       26 |        0 |       10 |        0 |    100% |           |
| modules/autonomous.py                   |       18 |        2 |        4 |        2 |     82% |    30, 34 |
| modules/batterysim.py                   |       11 |        2 |        0 |        0 |     82% |     14-15 |
| modules/control.py                      |        6 |        0 |        0 |        0 |    100% |           |
| modules/coralretraction.py              |       13 |        1 |        2 |        1 |     87% |        20 |
| modules/dashboard.py                    |      104 |        2 |       12 |        3 |     96% |146, 150->153, 158 |
| modules/diagnostics.py                  |       38 |        8 |        4 |        1 |     74% |27-30, 33-34, 38, 48 |
| modules/hardware.py                     |       26 |        0 |        0 |        0 |    100% |           |
| modules/logging.py                      |       18 |        1 |        6 |        1 |     92% |        25 |
| modules/propertysavechecker.py          |       35 |       17 |       16 |        2 |     39% |22-26, 31-47 |
| modules/tagvision.py                    |       16 |        2 |        2 |        1 |     83% |     26-27 |
| ports.py                                |       35 |        0 |        0 |        0 |    100% |           |
| properties.py                           |       85 |       72 |       18 |        1 |     14% |17-24, 34-58, 62-78, 82-127, 131-158 |
| robot.py                                |       31 |        0 |        0 |        0 |    100% |           |
| subsystems/\_\_init\_\_.py              |        0 |        0 |        0 |        0 |    100% |           |
| subsystems/arm.py                       |       43 |        4 |        4 |        2 |     87% |33, 40, 49, 55 |
| subsystems/claw.py                      |       36 |        1 |        2 |        0 |     97% |        42 |
| subsystems/climber.py                   |       81 |        3 |       10 |        1 |     96% |48->exit, 105, 108, 111 |
| subsystems/drivetrain.py                |      112 |       10 |        4 |        2 |     90% |110->exit, 137, 160, 169-178, 272-273, 276, 282 |
| subsystems/elevator.py                  |      122 |        6 |       14 |        3 |     93% |65->exit, 111, 115, 149, 158, 161, 164 |
| subsystems/intake.py                    |      100 |        5 |       10 |        2 |     94% |56->exit, 91, 127, 133, 136, 139 |
| subsystems/printer.py                   |      126 |        4 |       16 |        2 |     96% |67->exit, 119->126, 157, 163, 166, 169 |
| tests/\_\_init\_\_.py                   |        0 |        0 |        0 |        0 |    100% |           |
| tests/test\_arm.py                      |      212 |        0 |        6 |        1 |     99% |  304->325 |
| tests/test\_claw.py                     |      116 |        0 |        0 |        0 |    100% |           |
| tests/test\_climber.py                  |       90 |        0 |        0 |        0 |    100% |           |
| tests/test\_common.py                   |        1 |        0 |        0 |        0 |    100% |           |
| tests/test\_drivetrain.py               |       10 |        0 |        0 |        0 |    100% |           |
| tests/test\_elevator.py                 |      155 |        0 |        0 |        0 |    100% |           |
| tests/test\_intake.py                   |       91 |        0 |        0 |        0 |    100% |           |
| tests/test\_printer.py                  |      147 |        5 |        8 |        3 |     95% |54, 216-217, 256-257 |
| tests/test\_resetall.py                 |       19 |        0 |        0 |        0 |    100% |           |
| ultime/\_\_init\_\_.py                  |        0 |        0 |        0 |        0 |    100% |           |
| ultime/affinecontroller.py              |       77 |       77 |        2 |        0 |      0% |     1-122 |
| ultime/alert.py                         |       74 |        6 |       12 |        3 |     90% |42, 70, 83, 87, 98, 101, 106->105 |
| ultime/auto.py                          |        5 |        1 |        0 |        0 |     80% |         7 |
| ultime/autoproperty.py                  |       61 |       34 |       22 |        2 |     35% |35, 39, 52-105 |
| ultime/axistrigger.py                   |        8 |        8 |        2 |        0 |      0% |      1-16 |
| ultime/command.py                       |       44 |        3 |        2 |        1 |     91% |     40-42 |
| ultime/coroutinecommand.py              |       27 |       27 |        6 |        0 |      0% |      1-41 |
| ultime/gyro.py                          |      125 |       48 |       10 |        5 |     61% |28->exit, 31->exit, 34->exit, 37->exit, 40, 43, 56-62, 65, 68, 71, 74, 79-83, 86, 89, 92, 95, 118, 126, 130, 136, 153-157, 160, 163, 166, 169, 174-183, 186, 189, 192-193, 196-197, 200, 203 |
| ultime/immutable.py                     |        6 |        2 |        0 |        0 |     67% |      3, 8 |
| ultime/linearinterpolator.py            |       25 |       25 |        6 |        0 |      0% |      1-36 |
| ultime/module.py                        |       81 |        8 |       20 |        2 |     90% |15, 24, 45, 51, 63, 66, 69, 97, 109->108 |
| ultime/modulerobot.py                   |       43 |        3 |        4 |        2 |     89% |18->exit, 24->exit, 55, 58, 61 |
| ultime/subsystem.py                     |       27 |        3 |        4 |        0 |     90% |11, 15, 37 |
| ultime/swerve.py                        |       63 |        1 |        2 |        1 |     97% |14, 55->exit |
| ultime/swerveconfig.py                  |       41 |        0 |        0 |        0 |    100% |           |
| ultime/switch.py                        |       66 |        6 |       42 |        7 |     88% |29->exit, 41, 53, 57, 67, 71, 81 |
| ultime/tests/\_\_init\_\_.py            |        7 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_alert.py             |       41 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_commands.py          |       75 |        4 |       54 |        4 |     94% |60->52, 62-65, 78->68, 80-83 |
| ultime/tests/test\_modules.py           |       48 |        1 |        0 |        0 |     98% |        17 |
| ultime/tests/test\_properties.py        |        3 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_subsystems.py        |       17 |        0 |        8 |        0 |    100% |           |
| ultime/tests/test\_switch.py            |       33 |        0 |        0 |        0 |    100% |           |
| ultime/tests/utils.py                   |       60 |       12 |       10 |        0 |     83% |25-26, 37-41, 51-55 |
| ultime/trapezoidalmotion.py             |      104 |       28 |       42 |        5 |     66% |20, 22, 40-44, 59->exit, 73-91, 110-111, 199-200, 203 |
| ultime/vision.py                        |       63 |       19 |       18 |        3 |     58% |29-31, 34-40, 43-46, 67->exit, 72, 77-80, 83-84, 88, 96 |
|                               **TOTAL** | **4056** |  **557** |  **500** |   **82** | **83%** |           |


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