import numpy as np

from maze import movement


class Simulation(object):
  '''Tracks the player in a world and implements the rules and rewards.

  score is the cumulative score of the player in this run of the
  simulation.
  '''
  def __init__(self, generator):
    self._generator = generator

    # Initialized by reset()
    self.state = None
    self.world = None

    self.reset()

  def reset(self):
    '''Resets the simulation to the initial state.'''
    self.world = self._generator.generate()
    self.state = self.world.init_state
    self.score = 0

  @property
  def in_terminal_state(self):
    '''Whether the simulation is in a terminal state (stopped.)'''
    return self.world.at(self.state) in ['^', '$'] or self.score < -500

  @property
  def x(self):
    '''The x coordinate of the player.'''
    return self.state[0]

  @property
  def y(self):
    '''The y coordinate of the player.'''
    return self.state[1]

  def act(self, action):
    '''Performs action and returns the reward from that step.'''
    reward = -1

    delta = movement.MOVEMENT[action]
    new_state = self.x + delta[0], self.y + delta[1]

    if self._valid_move(new_state):
      ch = self.world.at(new_state)
      if ch == '^':
        reward = -10000
      elif ch == '$':
        reward = 10000
      self.state = new_state
    else:
      # Penalty for hitting the walls.
      reward -= 5

    self.score += reward
    return reward

  def _valid_move(self, new_state):
    '''Gets whether movement to new_state is a valid move.'''
    new_x, new_y = new_state
    # TODO: Could check that there's no teleportation cheating.
    return (0 <= new_x and new_x < self.world.w and
            0 <= new_y and new_y < self.world.h and
            self.world.at(new_state) in ['.', '^', '$'])

  def to_array(self):
    '''Converts the state of a simulation to numpy ndarray.

    The returned array has numpy.int8 units with the following mapping.
    This mapping has no special meaning because these indices are fed
    into an embedding layer.
        ' ' -> 0
        '#' -> 1
        '$' -> 2
        '.' -> 3
        '@' -> 4
        '^' -> 5
    Args:
      sim: A simulation.Simulation to externalize the state of.
    Returns:
      The world map and player position represented as an numpy ndarray.
    '''
    key = ' #$.@^'
    w = np.empty(shape=(self.world.h, self.world.w), dtype=np.int8)
    for v in range(self.world.h):
      for u in range(self.world.w):
        w[v, u] = key.index(self.world.at((u, v)))
    w[self.y, self.x] = key.index('@')
    return w
