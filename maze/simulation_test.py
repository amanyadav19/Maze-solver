import numpy as np
import unittest

from maze import movement
from maze import simulation
from maze import world


class TestSimulation(unittest.TestCase):
  def test_in_terminal_state(self):
    w = world.World.parse('@^')
    sim = simulation.Simulation(world.Static(w))
    self.assertFalse(sim.in_terminal_state)
    sim.act(movement.ACTION_RIGHT)
    self.assertTrue(sim.in_terminal_state)

  def test_act_accumulates_score(self):
    w = world.World.parse('@.')
    sim = simulation.Simulation(world.Static(w))
    sim.act(movement.ACTION_RIGHT)
    sim.act(movement.ACTION_LEFT)
    self.assertEqual(-2, sim.score)

  def test_to_array(self):
    w = world.World.parse('$.@^#')
    sim = simulation.Simulation(world.Static(w))
    self.assertTrue(
      (np.array([[2, 3, 4, 5, 1]], dtype=np.int8) == sim.to_array())
      .all())
