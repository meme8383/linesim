Usage
=====

Installation
------------

Linesim is available on `PyPI <https://pypi.org/project/linesim/>`_.

.. code-block:: console

    $ pip install linesim

Quick Start
-----------
First, import the ``LineSimulation`` class.

.. code-block:: python

    from linesim import LineSimulation

Initialize the simulation by creating a ``LineSimulation`` object. Specify
the track to be used as ``background``

.. code-block:: python

    sim = LineSimulation(background="maze")

Get the robot object and run ``sim.add_sensor(offset)`` for each sensor
to initialize, with positive x values as horizontal offset and positive y
values as vertical offset from the center of the robot.

.. note::
    Pygame defines the positive y direction as downwards.

.. code-block:: python

    robot = sim.robot
    # Initialize 3 line sensors in a triangle
    line_sensors = [
        sim.add_sensor((20, 10), "line"),
        sim.add_sensor((20, -10), "line"),
        sim.add_sensor((0, 0), "line")
    ]

    # Initialize 2 ultrasonic sensors facing 25 degrees outwards
    right_ultrasonic = sim.add_sensor((30, 10), "ultrasonic", 25)
    left_ultrasonic = sim.add_sensor((30, -10), "ultrasonic", -25)

Now, create your loop. Use ``sim.running`` to check if the simulation is
still running, and run ``sim.update()`` to update the game after every
movement.

.. code-block:: python

    while sim.running:
        if sensors[0]:
            robot.rotate(4)  # Turn right
        elif sensors[1]:
            robot.rotate(-4)  # Turn left
        else:
            robot.move(4)  # Go straight

Using Custom Tracks
-------------------

You may use any image as a track for the robot. Use black lines for
line sensors to follow, use red to mark the finish line, and use blue for
walls.

.. code-block:: python

    sim = LineSimulation(
        start=(x, y),  # Start coordinates
        custom_background="path/to/image"
    )

Setting the Sensor Threshold
----------------------------

By default, the line sensors will return true when the RGB
value under the sensor's position has an average value under ``50``. A custom
threshold can be supplied:

.. code-block:: python

    Line.threshold = 50

You can also set the range of the ultrasonic sensors in pixels
(default ``100``):

.. code-block:: python

    Ultrasonic.max_range = 100  # pixels

Changing the Sim Behavior
-------------------------

The ``LineSimulation.update()`` method includes some optional arguments to
change the behavior of the simulator.

.. code-block:: python

    LineSimulation.update(
        check_bounds=True,
        fps=30
    )

The ``check_bounds`` argument determines whether the simulation ends when the
robot leaves the frame (default ``True``). The ``fps`` argument determines the
maximum framerate of the simulation. Higher values will speed up the
simulation and vice versa.
