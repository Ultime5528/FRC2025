# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/Ultime5528/FRC2025/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                            |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|------------------------------------------------ | -------: | -------: | -------: | -------: | ------: | --------: |
| commands/\_\_init\_\_.py                        |        0 |        0 |        0 |        0 |    100% |           |
| commands/alignwithreefside.py                   |       47 |       21 |        2 |        0 |     53% |45-59, 63-65, 77, 82-85, 89-97 |
| commands/arm/\_\_init\_\_.py                    |        0 |        0 |        0 |        0 |    100% |           |
| commands/arm/extendarm.py                       |       31 |        3 |        6 |        3 |     84% |25-26, 38->exit, 40 |
| commands/arm/retractarm.py                      |       31 |        1 |        6 |        2 |     92% |38->exit, 40 |
| commands/claw/\_\_init\_\_.py                   |        0 |        0 |        0 |        0 |    100% |           |
| commands/claw/autodrop.py                       |        9 |        0 |        0 |        0 |    100% |           |
| commands/claw/drop.py                           |       56 |        0 |        0 |        0 |    100% |           |
| commands/claw/ejectcoral.py                     |        0 |        0 |        0 |        0 |    100% |           |
| commands/claw/loadcoral.py                      |       34 |        0 |        4 |        1 |     97% |  40->exit |
| commands/claw/retractcoral.py                   |       38 |        6 |        0 |        0 |     84% |48, 51-52, 55, 58-59 |
| commands/claw/waituntilcoral.py                 |       10 |        1 |        0 |        0 |     90% |        15 |
| commands/climber/\_\_init\_\_.py                |        0 |        0 |        0 |        0 |    100% |           |
| commands/climber/moveclimber.py                 |       45 |        3 |        2 |        1 |     91% |20, 24, 29 |
| commands/climber/resetclimber.py                |       25 |        0 |        6 |        0 |    100% |           |
| commands/diagnostics/\_\_init\_\_.py            |        0 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/arm/\_\_init\_\_.py        |        9 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/arm/armmotor.py            |       37 |        0 |        2 |        1 |     97% |  69->exit |
| commands/diagnostics/claw/\_\_init\_\_.py       |       10 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/claw/hascoral.py           |       12 |        0 |        2 |        1 |     93% |  13->exit |
| commands/diagnostics/claw/leftmotor.py          |       41 |        0 |        8 |        1 |     98% |  54->exit |
| commands/diagnostics/claw/rightmotor.py         |       41 |        0 |        8 |        1 |     98% |  54->exit |
| commands/diagnostics/diagnoseall.py             |        7 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/drivetrain/\_\_init\_\_.py |        9 |        0 |        0 |        0 |    100% |           |
| commands/diagnostics/drivetrain/odometry.py     |       36 |        1 |       10 |        1 |     96% |        49 |
| commands/diagnostics/drivetrain/swerve.py       |       53 |        3 |        4 |        2 |     91% | 48-52, 88 |
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
| commands/drivetrain/drive.py                    |       60 |       13 |       14 |        5 |     70% |18, 22-25, 69-71, 74, 85-86, 89-91 |
| commands/drivetrain/drivetoposes.py             |       85 |        5 |       14 |        6 |     89% |13, 67, 96->99, 99->102, 102->105, 105->108, 123, 149, 166 |
| commands/drivetrain/resetgyro.py                |       17 |        1 |        2 |        1 |     89% |        18 |
| commands/drivetrain/resetpose.py                |       13 |        6 |        0 |        0 |     54% |9-12, 15, 18 |
| commands/dropautonomous.py                      |       33 |        0 |        0 |        0 |    100% |           |
| commands/dropprepareloading.py                  |       33 |        0 |        0 |        0 |    100% |           |
| commands/elevator/\_\_init\_\_.py               |        0 |        0 |        0 |        0 |    100% |           |
| commands/elevator/maintainelevator.py           |       16 |        0 |        2 |        0 |    100% |           |
| commands/elevator/manualmoveelevator.py         |       28 |        0 |        0 |        0 |    100% |           |
| commands/elevator/moveelevator.py               |      101 |       13 |       14 |        1 |     79% |20-34, 157 |
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
| commands/printer/scanprinter.py                 |       63 |        7 |       14 |        5 |     82% |55->65, 59, 62-63, 66, 77-83 |
| commands/resetall.py                            |       13 |        0 |        0 |        0 |    100% |           |
| commands/resetallbutclimber.py                  |       16 |        0 |        0 |        0 |    100% |           |
| commands/resetautonomous.py                     |       14 |        0 |        0 |        0 |    100% |           |
| commands/vision/\_\_init\_\_.py                 |        0 |        0 |        0 |        0 |    100% |           |
| commands/vision/alignwithalgae.py               |       46 |       19 |       10 |        0 |     48% |38-64, 67-69 |
| conftest.py                                     |        1 |        0 |        0 |        0 |    100% |           |
| modules/\_\_init\_\_.py                         |        0 |        0 |        0 |        0 |    100% |           |
| modules/algaevision.py                          |       14 |        6 |        4 |        0 |     44% | 12, 15-21 |
| modules/armcollision.py                         |       26 |        0 |       10 |        0 |    100% |           |
| modules/autonomous.py                           |       81 |        2 |        4 |        2 |     95% |  163, 167 |
| modules/batterysim.py                           |       11 |       11 |        0 |        0 |      0% |      1-15 |
| modules/blockelevatoruntilcoral.py              |       12 |        0 |        2 |        0 |    100% |           |
| modules/control.py                              |       43 |        0 |        0 |        0 |    100% |           |
| modules/coralretraction.py                      |       16 |        2 |        4 |        2 |     80% |    21, 28 |
| modules/dashboard.py                            |      115 |        2 |       12 |        3 |     96% |205, 209->212, 217 |
| modules/diagnostics.py                          |       46 |        3 |        4 |        0 |     94% | 57-58, 62 |
| modules/hardware.py                             |       30 |        0 |        0 |        0 |    100% |           |
| modules/loadingdetection.py                     |       24 |        1 |        2 |        0 |     96% |        32 |
| modules/logging.py                              |       21 |        1 |        6 |        1 |     93% |        26 |
| modules/propertysavechecker.py                  |       35 |       17 |       16 |        2 |     39% |22-26, 31-47 |
| modules/tagvision.py                            |       34 |        5 |        6 |        2 |     78% |35-37, 49, 57 |
| ports.py                                        |       39 |        0 |        0 |        0 |    100% |           |
| properties.py                                   |       85 |       72 |       18 |        1 |     14% |17-24, 34-58, 62-78, 82-127, 131-158 |
| robot.py                                        |       35 |        0 |        0 |        0 |    100% |           |
| subsystems/\_\_init\_\_.py                      |        0 |        0 |        0 |        0 |    100% |           |
| subsystems/arm.py                               |       48 |        4 |        4 |        2 |     88% |40, 47, 56, 65 |
| subsystems/claw.py                              |       44 |        1 |        0 |        0 |     98% |        65 |
| subsystems/climber.py                           |       84 |        3 |       10 |        1 |     96% |49->exit, 109, 112, 115 |
| subsystems/drivetrain.py                        |      140 |       15 |       10 |        3 |     88% |174->exit, 207, 232, 241-250, 298, 308, 333-340, 355-356, 359, 365 |
| subsystems/elevator.py                          |      132 |        5 |       16 |        2 |     95% |72->exit, 129, 163, 172, 175, 178 |
| subsystems/intake.py                            |      106 |        5 |       10 |        2 |     94% |59->66, 109, 145, 151, 154, 157 |
| subsystems/led.py                               |      168 |       59 |       50 |        8 |     60% |15-16, 65, 68-70, 75, 77, 83-96, 109, 112-120, 123, 126, 129, 132, 135, 141, 163-164, 170-184, 200, 205-221, 226, 229, 237, 243 |
| subsystems/printer.py                           |      131 |        4 |       16 |        2 |     96% |88->exit, 140->147, 183, 189, 192, 195 |
| tests/\_\_init\_\_.py                           |        0 |        0 |        0 |        0 |    100% |           |
| tests/test\_arm.py                              |      213 |        0 |        6 |        1 |     99% |  304->314 |
| tests/test\_blockelevatoruntilcoral.py          |       48 |        0 |        0 |        0 |    100% |           |
| tests/test\_claw.py                             |      163 |        0 |        0 |        0 |    100% |           |
| tests/test\_climber.py                          |       89 |        0 |        0 |        0 |    100% |           |
| tests/test\_common.py                           |        1 |        0 |        0 |        0 |    100% |           |
| tests/test\_completedropsequence.py             |       23 |        0 |        0 |        0 |    100% |           |
| tests/test\_diagnostics.py                      |        9 |        0 |        0 |        0 |    100% |           |
| tests/test\_drivetrain.py                       |       10 |        0 |        0 |        0 |    100% |           |
| tests/test\_elevator.py                         |      161 |        0 |        0 |        0 |    100% |           |
| tests/test\_intake.py                           |       91 |        0 |        0 |        0 |    100% |           |
| tests/test\_printer.py                          |      146 |        5 |        8 |        3 |     95% |52, 214-215, 254-255 |
| tests/test\_resetall.py                         |       35 |        0 |        0 |        0 |    100% |           |
| tests/test\_resetautonomous.py                  |       42 |        0 |        0 |        0 |    100% |           |
| ultime/\_\_init\_\_.py                          |        0 |        0 |        0 |        0 |    100% |           |
| ultime/affinecontroller.py                      |       77 |       77 |        2 |        0 |      0% |     1-122 |
| ultime/alert.py                                 |       88 |        5 |       14 |        1 |     94% |42, 83, 87, 98, 101 |
| ultime/auto.py                                  |        5 |        1 |        0 |        0 |     80% |         7 |
| ultime/autoproperty.py                          |       61 |       33 |       22 |        1 |     37% |39, 52-105 |
| ultime/axistrigger.py                           |        8 |        1 |        2 |        1 |     80% |        15 |
| ultime/cache.py                                 |       40 |        2 |       12 |        2 |     92% |    16, 29 |
| ultime/command.py                               |       70 |       15 |        4 |        1 |     76% |42-44, 93, 96-100, 103, 106, 109-110, 113-114 |
| ultime/coroutinecommand.py                      |       27 |       27 |        6 |        0 |      0% |      1-41 |
| ultime/followpath.py                            |       87 |       37 |       18 |        0 |     57% |24, 59, 62, 71-78, 81-105, 108-145, 171, 174-178 |
| ultime/gyro.py                                  |      126 |       48 |       10 |        5 |     61% |28->exit, 31->exit, 34->exit, 37->exit, 40, 43, 56-62, 65, 68, 71, 74, 79-83, 86, 89, 92, 95, 123, 131, 135, 141, 158-162, 165, 168, 171, 174, 179-188, 191, 194, 197-198, 201-202, 205, 208 |
| ultime/immutable.py                             |        6 |        2 |        0 |        0 |     67% |      3, 8 |
| ultime/linearinterpolator.py                    |       25 |       25 |        6 |        0 |      0% |      1-36 |
| ultime/module.py                                |       81 |        6 |       20 |        2 |     92% |21, 42, 48, 60, 66, 97, 109->108 |
| ultime/modulerobot.py                           |       45 |        1 |        4 |        2 |     94% |22->exit, 28->exit, 65 |
| ultime/proxy.py                                 |       19 |        0 |        2 |        0 |    100% |           |
| ultime/subsystem.py                             |       25 |        2 |        4 |        0 |     93% |    12, 34 |
| ultime/swerve.py                                |       86 |        2 |        2 |        1 |     97% |16, 57->exit, 160 |
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
| ultime/trapezoidalmotion.py                     |      104 |       25 |       42 |        5 |     68% |20, 22, 40-44, 59->exit, 73-91, 110-111 |
| ultime/vision.py                                |       67 |       13 |       20 |        5 |     70% |36->exit, 43-46, 67->exit, 71-74, 78, 83-84, 88, 94, 102 |
|                                       **TOTAL** | **5853** |  **717** |  **730** |  **122** | **85%** |           |


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