# Linesim
[![Build status](https://img.shields.io/github/actions/workflow/status/meme8383/linesim/pylint.yml?style=for-the-badge)](https://github.com/meme8383/linesim/actions/workflows/pylint.yml)
[![PyPI version](https://img.shields.io/pypi/v/linesim?style=for-the-badge)](https://pypi.org/project/linesim/)
[![License](https://img.shields.io/github/license/meme8383/linesim?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python versions](https://img.shields.io/pypi/pyversions/linesim?style=for-the-badge)](https://pypi.org/project/linesim/)
[![Wheel](https://img.shields.io/pypi/wheel/linesim?style=for-the-badge)](https://pypi.org/project/linesim/)

Line simulation made with pygame for testing a robot's pathfinding abilities.

Intended for testing pathfinding code for Purdue's ENGR 161 Project 3.

![Test track](https://raw.githubusercontent.com/meme8383/linesim/main/linesim/assets/background.png)

## Features
- Multiple line sensor support
- Default track with curves, broken lines, and multiple paths.

## Installation

Linesim is available on [PyPI](https://pypi.org/project/linesim/).

```
pip install linesim
```

Note: If you are having difficulty installing pygame 2.1.2 and you are using Python 3.11, first run `pip install pygame==2.1.3-dev8` before installing.
## Usage
First, import the `LineSimulation` class.

```py
from linesim import LineSimulation
```
Initialize the simulation and run `sim.add_sensor(offset)` for each sensor to initialize, with positive x values as horizontal offset and positive y vales as vertical offset from the center of the robot.

Note: pygame defines the positive y direction as downwards.
```py
sim = LineSimulation()
robot = sim.robot
sensors = [
    sim.add_sensor((20, 10)),
    sim.add_sensor((20, -10)),
    sim.add_sensor((0, 0))
]
```
Now, create your loop. Use `sim.running` to check if the simulation is still running, and run `sim.update()` to update the game after every movement.
```py
while sim.running:
    if sensors[0].read_line():
        robot.rotate(4)  # Turn right
    elif sensors[1].read_line():
        robot.rotate(-4)  # Turn left
    else:
        robot.move(4)  # Go straight

    sim.update()
```


