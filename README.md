# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2025/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                            |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|------------------------------------------------ | -------: | -------: | -------: | -------: | ------: | --------: |
| commands/\_\_init\_\_.py                        |        0 |        0 |        0 |        0 |    100% |           |
| commands/alignwithreefside.py                   |       47 |        1 |        2 |        1 |     96% |        41 |
| commands/arm/\_\_init\_\_.py                    |        0 |        0 |        0 |        0 |    100% |           |
| commands/arm/extendarm.py                       |       31 |        3 |        6 |        3 |     84% |25-26, 38->exit, 40 |
| commands/arm/retractarm.py                      |       31 |        1 |        6 |        2 |     92% |38->exit, 40 |
| commands/autonomous/megaautonomous.py           |       56 |        0 |        0 |        0 |    100% |           |
| commands/autonomous/simpleauto.py               |       32 |        0 |        0 |        0 |    100% |           |
| commands/claw/\_\_init\_\_.py                   |        0 |        0 |        0 |        0 |    100% |           |
| commands/claw/autodrop.py                       |        9 |        0 |        0 |        0 |    100% |           |
| commands/claw/drop.py                           |       56 |        0 |        0 |        0 |    100% |           |
| commands/claw/ejectcoral.py                     |        0 |        0 |        0 |        0 |    100% |           |
| commands/claw/loadcoral.py                      |       39 |        0 |        6 |        1 |     98% |  47->exit |
| commands/claw/retractcoral.py                   |       38 |        6 |        0 |        0 |     84% |48, 51-52, 55, 58-59 |
| commands/claw/waituntilcoral.py                 |       16 |        2 |        0 |        0 |     88% |    19, 22 |
| commands/climber/\_\_init\_\_.py                |        0 |        0 |        0 |        0 |    100% |           |
| commands/climber/moveclimber.py                 |       52 |        3 |        2 |        1 |     93% |24, 28, 33 |
| commands/climber/resetclimber.py                |       25 |        0 |        6 |        0 |    100% |           |
| commands/diagnostics/\_\_init\_\_.py            |        0 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/arm/\_\_init\_\_.py        |        9 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/arm/armmotor.py            |       38 |        0 |        2 |        1 |     98% |  71->exit |
| commands/diagnostics/claw/\_\_init\_\_.py       |       10 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/claw/hascoral.py           |       12 |        0 |        2 |        1 |     93% |  13->exit |
| commands/diagnostics/claw/leftmotor.py          |       41 |        0 |        8 |        1 |     98% |  54->exit |
| commands/diagnostics/claw/rightmotor.py         |       41 |        0 |        8 |        1 |     98% |  54->exit |
| commands/diagnostics/climber/\_\_init\_\_.py    |        8 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/climber/switchandmotor.py  |       32 |        2 |        6 |        3 |     87% |34, 43->48, 49 |
| commands/diagnostics/diagnoseall.py             |        7 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/drivetrain/\_\_init\_\_.py |        9 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/drivetrain/odometry.py     |       36 |        1 |       10 |        1 |     96% |        49 |
| commands/diagnostics/drivetrain/swerve.py       |       53 |        3 |        4 |        2 |     91% | 48-52, 88 |
| commands/diagnostics/elevator/\_\_init\_\_.py   |        9 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/elevator/motor.py          |       35 |        0 |        2 |        1 |     97% |  61->exit |
| commands/diagnostics/elevator/switch.py         |       20 |        3 |        6 |        3 |     77% |24, 28, 30 |
| commands/diagnostics/intake/\_\_init\_\_.py     |       10 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/intake/extend.py           |       16 |        3 |        4 |        1 |     70% |     19-22 |
| commands/diagnostics/intake/hasalgae.py         |       12 |        1 |        2 |        1 |     86% |        14 |
| commands/diagnostics/intake/retract.py          |       16 |        0 |        4 |        2 |     90% |18->exit, 21->exit |
| commands/diagnostics/printer/\_\_init\_\_.py    |        9 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/printer/motor.py           |       30 |        0 |        2 |        1 |     97% |  58->exit |
| commands/diagnostics/printer/switch.py          |       22 |        3 |        8 |        4 |     77% |25, 27, 30->32, 33 |
| commands/diagnostics/utils/\_\_init\_\_.py      |        0 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/utils/setrunningtest.py    |       15 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/\_\_init\_\_.py             |        0 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/drive.py                    |       53 |       11 |       14 |        4 |     72% |17, 21-24, 61-63, 66, 81-83 |
| commands/drivetrain/driverelative.py            |       38 |        0 |        0 |        0 |    100% |           |
| commands/drivetrain/drivetoposes.py             |      105 |        7 |       18 |        4 |     89% |26, 29-38, 97, 103->106, 106->109, 109->112, 112->115 |
| commands/drivetrain/resetgyro.py                |       17 |        1 |        2 |        1 |     89% |        18 |
| commands/drivetrain/resetpose.py                |       13 |        6 |        0 |        0 |     54% |9-12, 15, 18 |
| commands/dropautonomous.py                      |       34 |        0 |        0 |        0 |    100% |           |
| commands/dropprepareloading.py                  |       33 |        0 |        0 |        0 |    100% |           |
| commands/elevator/\_\_init\_\_.py               |        0 |        0 |        0 |        0 |    100% |           |
| commands/elevator/maintainelevator.py           |       18 |        0 |        2 |        0 |    100% |           |
| commands/elevator/manualmoveelevator.py         |       31 |        0 |        0 |        0 |    100% |           |
| commands/elevator/moveelevator.py               |      105 |       13 |       14 |        1 |     80% |20-34, 163 |
| commands/elevator/resetelevator.py              |       24 |        1 |        4 |        1 |     93% |        29 |
| commands/intake/\_\_init\_\_.py                 |        0 |        0 |        0 |        0 |    100% |           |
| commands/intake/dropalgae.py                    |       27 |        0 |        2 |        0 |    100% |           |
| commands/intake/grabalgae.py                    |       29 |        0 |        2 |        0 |    100% |           |
| commands/intake/moveintake.py                   |       51 |        1 |        4 |        1 |     96% |        76 |
| commands/intake/resetintake.py                  |       22 |        0 |        2 |        0 |    100% |           |
| commands/prepareloading.py                      |       12 |        0 |        0 |        0 |    100% |           |
| commands/printer/\_\_init\_\_.py                |        0 |        0 |        0 |        0 |    100% |           |
| commands/printer/manualmoveprinter.py           |       34 |        0 |        4 |        1 |     97% |  34->exit |
| commands/printer/moveprinter.py                 |       97 |        2 |        8 |        2 |     96% |  122, 133 |
| commands/printer/resetprinter.py                |       21 |        0 |        2 |        0 |    100% |           |
| commands/printer/scanprinter.py                 |       71 |       11 |       16 |        5 |     77% |62->79, 66, 69-77, 80, 91-97 |
| commands/resetall.py                            |       13 |        0 |        0 |        0 |    100% |           |
| commands/resetallbutclimber.py                  |       16 |        0 |        0 |        0 |    100% |           |
| commands/resetautonomous.py                     |       14 |        0 |        0 |        0 |    100% |           |
| commands/vision/\_\_init\_\_.py                 |        0 |        0 |        0 |        0 |    100% |           |
| commands/vision/alignwithalgae.py               |       46 |       19 |       10 |        0 |     48% |38-64, 67-69 |
| conftest.py                                     |        1 |        0 |        0 |        0 |    100% |           |
| modules/\_\_init\_\_.py                         |        0 |        0 |        0 |        0 |    100% |           |
| modules/algaevision.py                          |       14 |        6 |        4 |        0 |     44% | 12, 15-21 |
| modules/armcollision.py                         |       26 |        0 |       10 |        0 |    100% |           |
| modules/autonomous.py                           |       74 |       25 |        4 |        2 |     65% |32, 58-136, 152, 156 |
| modules/batterysim.py                           |       11 |       11 |        0 |        0 |      0% |      1-15 |
| modules/blockelevatoruntilcoral.py              |       12 |        0 |        2 |        0 |    100% |           |
| modules/control.py                              |       48 |        0 |        0 |        0 |    100% |           |
| modules/coralretraction.py                      |       16 |        2 |        4 |        2 |     80% |    21, 28 |
| modules/dashboard.py                            |      134 |        1 |       12 |        2 |     98% |265, 269->272 |
| modules/diagnostics.py                          |       54 |        3 |        4 |        0 |     95% | 68-69, 73 |
| modules/hardware.py                             |       32 |        0 |        0 |        0 |    100% |           |
| modules/loadingdetection.py                     |       25 |        1 |        2 |        0 |     96% |        33 |
| modules/logging.py                              |       17 |        0 |        0 |        0 |    100% |           |
| modules/propertysavechecker.py                  |       35 |       17 |       16 |        2 |     39% |22-26, 31-47 |
| modules/tagvision.py                            |       35 |        5 |        6 |        2 |     78% |36-38, 50, 58 |
| ports.py                                        |       41 |        0 |        0 |        0 |    100% |           |
| properties.py                                   |       85 |       72 |       18 |        1 |     14% |17-24, 34-58, 62-78, 82-127, 131-158 |
| robot.py                                        |       35 |        0 |        0 |        0 |    100% |           |
| subsystems/\_\_init\_\_.py                      |        0 |        0 |        0 |        0 |    100% |           |
| subsystems/arm.py                               |       48 |        4 |        4 |        2 |     88% |40, 47, 56, 65 |
| subsystems/claw.py                              |       40 |        1 |        0 |        0 |     98% |        60 |
| subsystems/climber.py                           |       87 |        3 |       10 |        1 |     96% |60->exit, 120, 123, 126 |
| subsystems/drivetrain.py                        |      161 |       21 |       12 |        3 |     85% |190->exit, 226, 251, 260-261, 269-278, 286-295, 353, 363, 388-395, 410-411, 414, 420 |
| subsystems/elevator.py                          |      136 |        5 |       16 |        2 |     95% |91->exit, 148, 182, 191, 194, 197 |
| subsystems/intake.py                            |      106 |        5 |       10 |        2 |     94% |59->66, 109, 145, 151, 154, 157 |
| subsystems/led.py                               |      185 |       60 |       54 |        8 |     62% |16-17, 78, 80, 86-99, 112, 115-123, 126, 129, 132, 135, 138, 144, 161-170, 190-204, 220, 225-241, 246, 249, 256, 261, 267 |
| subsystems/printer.py                           |      133 |        4 |       16 |        2 |     96% |89->exit, 141->148, 184, 190, 193, 196 |
| tests/\_\_init\_\_.py                           |        0 |        0 |        0 |        0 |    100% |           |
| tests/test\_arm.py                              |      213 |        0 |        6 |        1 |     99% |  304->314 |
| tests/test\_autonomouslevel4.py                 |       11 |        0 |        4 |        1 |     93% |      8->7 |
| tests/test\_blockelevatoruntilcoral.py          |       48 |        0 |        0 |        0 |    100% |           |
| tests/test\_claw.py                             |      163 |        0 |        0 |        0 |    100% |           |
| tests/test\_climber.py                          |       89 |        0 |        0 |        0 |    100% |           |
| tests/test\_common.py                           |        1 |        0 |        0 |        0 |    100% |           |
| tests/test\_completedropsequence.py             |       23 |        0 |        0 |        0 |    100% |           |
| tests/test\_dashboard.py                        |        3 |        0 |        0 |        0 |    100% |           |
| tests/test\_diagnostics.py                      |        9 |        0 |        0 |        0 |    100% |           |
| tests/test\_drivetrain.py                       |       33 |        0 |        0 |        0 |    100% |           |
| tests/test\_elevator.py                         |      156 |        1 |        2 |        1 |     99% |       107 |
| tests/test\_intake.py                           |       91 |        0 |        0 |        0 |    100% |           |
| tests/test\_printer.py                          |      146 |        5 |        8 |        3 |     95% |52, 214-215, 254-255 |
| tests/test\_resetall.py                         |       35 |        0 |        0 |        0 |    100% |           |
| tests/test\_resetautonomous.py                  |       42 |        0 |        0 |        0 |    100% |           |
| ultime/\_\_init\_\_.py                          |        0 |        0 |        0 |        0 |    100% |           |
| ultime/affinecontroller.py                      |       77 |       77 |        2 |        0 |      0% |     1-122 |
| ultime/alert.py                                 |       89 |        5 |       14 |        1 |     94% |44, 85, 89, 100, 103 |
| ultime/auto.py                                  |        5 |        1 |        0 |        0 |     80% |         7 |
| ultime/autoproperty.py                          |       61 |       33 |       22 |        1 |     37% |39, 52-105 |
| ultime/axistrigger.py                           |        8 |        1 |        2 |        1 |     80% |        15 |
| ultime/cache.py                                 |       40 |        2 |       12 |        2 |     92% |    16, 29 |
| ultime/command.py                               |       71 |        4 |        4 |        2 |     92% |43-45, 94, 98->101 |
| ultime/coroutinecommand.py                      |       27 |       27 |        6 |        0 |      0% |      1-41 |
| ultime/dynamicmotion.py                         |       56 |        5 |       14 |        4 |     87% |11, 79, 115->118, 149->154, 163, 171, 177 |
| ultime/followpath.py                            |       87 |       87 |       18 |        0 |      0% |     1-183 |
| ultime/gyro.py                                  |      131 |       47 |       10 |        5 |     63% |29->exit, 32->exit, 35->exit, 38->exit, 41, 44, 57-63, 66, 69, 72, 75, 80-84, 87, 90, 93, 96, 132, 136, 142, 163-167, 170, 173, 176, 179, 184-193, 196, 199, 202-203, 206-207, 210, 213 |
| ultime/immutable.py                             |        6 |        2 |        0 |        0 |     67% |      3, 8 |
| ultime/linearinterpolator.py                    |       25 |       25 |        6 |        0 |      0% |      1-36 |
| ultime/module.py                                |       81 |        8 |       20 |        2 |     90% |21, 24, 42, 48, 54, 60, 66, 97, 109->108 |
| ultime/modulerobot.py                           |       45 |        1 |        4 |        2 |     94% |22->exit, 28->exit, 65 |
| ultime/proxy.py                                 |       19 |        0 |        2 |        0 |    100% |           |
| ultime/subsystem.py                             |       26 |        2 |        4 |        0 |     93% |    13, 35 |
| ultime/swerve.py                                |       87 |        2 |        2 |        1 |     97% |17, 58->exit, 161 |
| ultime/swerveconfig.py                          |       41 |        0 |        0 |        0 |    100% |           |
| ultime/switch.py                                |       66 |        6 |       42 |        7 |     88% |29->exit, 41, 53, 57, 67, 71, 81 |
| ultime/tests/\_\_init\_\_.py                    |       10 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_alert.py                     |       39 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_cache.py                     |      189 |        0 |       14 |        0 |    100% |           |
| ultime/tests/test\_commands.py                  |       75 |        4 |       54 |        4 |     94% |61->53, 63-66, 79->69, 81-84 |
| ultime/tests/test\_modules.py                   |       48 |        1 |        0 |        0 |     98% |        17 |
| ultime/tests/test\_properties.py                |        3 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_proxy.py                     |       27 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_subsystems.py                |       17 |        0 |        8 |        0 |    100% |           |
| ultime/tests/test\_switch.py                    |       33 |        0 |        0 |        0 |    100% |           |
| ultime/tests/test\_timethis.py                  |        3 |        0 |        0 |        0 |    100% |           |
| ultime/tests/utils.py                           |       74 |        7 |       10 |        0 |     92% |28-29, 40-44 |
| ultime/timethis.py                              |       63 |       40 |       16 |        2 |     34% |20-45, 53-57, 64-93 |
| ultime/trapezoidalmotion.py                     |      106 |       28 |       42 |        5 |     67% |21, 23, 42-46, 62->exit, 76-94, 113-114, 206-207, 210 |
| ultime/vision.py                                |       73 |       13 |       20 |        5 |     72% |49->exit, 56-59, 80->exit, 84-87, 91, 96-97, 101, 107, 115 |
|                                       **TOTAL** | **6308** |  **784** |  **772** |  **132** | **85%** |           |


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