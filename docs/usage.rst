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

Initialize the simulation and run ``sim.add_sensor(offset)`` for each sensor
to initialize, with positive x values as horizontal offset and positive y
values as vertical offset from the center of the robot.

.. note::
    Pygame defines the positive y direction as downwards.

.. code-block:: python

    sim = LineSimulation()
    robot = sim.robot
    sensors = [
        sim.add_sensor((20, 10)),
        sim.add_sensor((20, -10)),
        sim.add_sensor((0, 0))
    ]

Now, create your loop. Use ``sim.running`` to check if the simulation is
still running, and run ``sim.update()`` to update the game after every
movement.

.. code-block:: python

    while sim.running:
        if sensors[0].read_line():
            robot.rotate(4)  # Turn right
        elif sensors[1].read_line():
            robot.rotate(-4)  # Turn left
        else:
            robot.move(4)  # Go straight

Using Custom Tracks
-------------------

You may use any image as a track for the robot. Simply draw black lines on a
white canvas for the sensor to read. Use a red (``RGB = (>230, <50, <50)``)
surface as the end goal.

.. code-block:: python

    sim = LineSimulation(
        start=(x, y),  # Start coordinates
        background="path/to/image"
    )

Setting the Sensor Threshold
----------------------------

By default, the ``Sensor.read_line()`` method will return true when the RGB
value under the sensor's position has an average value under ``50``. A custom
threshold can be supplied:

.. code-block:: python

    Sensor.read_line(threshold=50)

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
