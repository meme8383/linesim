"""Control the robot using only sensor values"""

from linesim import LineSimulation

sim = LineSimulation()
robot = sim.robot
sensors = [
    sim.add_sensor((20, 10)),
    sim.add_sensor((20, -10)),
    sim.add_sensor((0, 0))
]

while sim.running:
    if sensors[0].read_line():
        robot.rotate(4)  # Turn right
    elif sensors[1].read_line():
        robot.rotate(-4)  # Turn left
    else:
        robot.move(4)  # Go straight

    sim.update()
