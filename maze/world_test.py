import unittest

from maze import world


class TestWorld(unittest.TestCase):
  def test_size(self):
    g = world.World.parse('@$')
    self.assertEqual((2, 1), g.size)

  def test_init_state(self):
    g = world.World.parse('####\n#.@#\n####')
    self.assertEqual((2, 1), g.init_state)

  def test_parse_no_init_state_fails(self):
    with self.assertRaises(world.WorldFailure):
      world.World.parse('#')


class TestGenerator(unittest.TestCase):
  def test_generate_tiny_world(self):
    g = world.Generator(2, 1)
    w = g.generate()
    # The world should have a start and goal
    if w.init_state == (0, 0):
      self.assertEqual('$', w.at((1, 0)))
    elif w.init_state == (1, 0):
      self.assertEqual('$', w.at((0, 0)))
    else:
      self.fail('the start position %s is invalid' % (w.init_state,))
