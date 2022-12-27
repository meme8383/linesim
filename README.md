# LineSim

Line simulation made with pygame for testing a robot's pathfinding abilities.

Intended for testing pathfinding code for Purdue's ENGR 161 Project 3.

![Test track](linesim/assets/background.png)

## Features
- Multiple line sensor support
- Default track with curves, broken lines, and multiple paths.

## Usage
First, import the `LineSimulation` class.
```py
from linesim import LineSimulation
```
Initialize the simulation and run `sim.add_sensor(offset)` for each sensor to initialize, with positive x values as horizontal offset and positive y vales as vertical offset from the center of the robot.

Note: pygame defines the positive y direction as downwards.
```py
sim = LineSimulation((50, 450))
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


