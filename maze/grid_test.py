from unittest.mock import patch
import unittest

from maze import context
from maze import movement
from maze import simulation
from maze import world
from maze import grid


class TestMachinePlayer(unittest.TestCase):
  def test_interact(self):
    TEST_ACTION = movement.ACTION_RIGHT
    q = grid.QTable(-1)
    q.set((0, 0), TEST_ACTION, 1)

    player = grid.MachinePlayer(grid.GreedyQ(q), grid.StubLearner())
    w = world.World.parse('@.')
    with patch.object(simulation.Simulation, 'act') as mock_act:
      sim = simulation.Simulation(world.Static(w))
      ctx = context.StubContext()
      player.interact(ctx, sim)
    mock_act.assert_called_once_with(TEST_ACTION)
