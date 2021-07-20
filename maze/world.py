import random

from maze import movement


# Grid world maps are specified with characters a bit like NetHack:
# #, (blank) are impassable
# . is passable
# @ is the player start point
# ^ is a trap, with a large negative reward
# $ is the goal
VALID_CHARS = set(['#', '.', '@', '$', '^', ' '])


class WorldFailure(Exception):
  pass


class World(object):
  '''A grid world.'''
  def __init__(self, init_state, lines):
    '''Creates a grid world.
    init_state: the (x,y) player start position
    lines: list of strings of VALID_CHARS, the map'''
    self.init_state = init_state
    self._lines = [] + lines

  @classmethod
  def parse(cls, s):
    '''Parses a grid world in the string s.
s must be made up of equal-length lines of VALID_CHARS with one start position
denoted by @.'''
    init_state = None

    lines = s.split()
    if not lines:
      raise WorldFailure('no content')
    for (y, line) in enumerate(lines):
      if y > 0 and len(line) != len(lines[0]):
        raise WorldFailure('line %d is a different length (%d vs %d)' %
                                (y, len(line), len(lines[0])))
      for (x, ch) in enumerate(line):
        if not ch in VALID_CHARS:
          raise WorldFailure('invalid char "%c" at (%d, %d)' % (ch, x, y))
        if ch == '@':
          if init_state:
            raise WorldFailure('multiple initial states, at %o and '
                               '(%d, %d)' % (init_state, x, y))
          init_state = (x, y)
    if not init_state:
      raise WorldFailure('no initial state, use "@"')
    # The player start position is in fact ordinary ground.
    x, y = init_state
    line = lines[y]
    lines[y] = line[0:x] + '.' + line[x+1:]
    return World(init_state, lines)

  @property
  def size(self):
    '''The size of the grid world, width by height.'''
    return self.w, self.h

  @property
  def h(self):
    '''The height of the grid world.'''
    return len(self._lines)

  @property
  def w(self):
    '''The width of the grid world.'''
    return len(self._lines[0])

  def at(self, pos):
    '''Gets the character at an (x, y) coordinate.
Positions are indexed from the origin 0,0 at the top, left of the map.'''
    x, y = pos
    return self._lines[y][x]

  def pretty_str(self):
    copy = [] + self._lines
    x, y = self.init_state
    start_line = copy[y]
    copy[y] = start_line[0:x] + '@' + start_line[x+1:]
    return '\n'.join(copy)


class Static(object):
  def __init__(self, value):
    self._value = value

  def generate(self):
    return self._value

  @property
  def size(self):
    '''The size of the grid world, width by height.'''
    return self._value.size


class Generator(object):
  '''Generates random grid worlds.'''
  def __init__(self, width, height):
    '''Creates a generator for worlds with a fixed size.
    width: The width of the world. Must be at least two cells wide.
    height: The height of the world. Must be at least one cell high.
    '''
    assert 2 <= width
    assert 1 <= height
    self._width = width
    self._height = height
    self._grid = None
    self._passable = None

  @property
  def size(self):
    return (self._width, self._height)

  def generate(self):
    '''Generates and returns a new world.'''
    self._grid = list(map(lambda _: [' '] * self._width, range(self._height)))
    self._passable = set()

    x = random.randrange(0, self._width - 1)
    y = random.randrange(0, self._height)

    # Make at least two squares passable
    self._paint((x, y), '.')
    self._paint((x + 1, y), '.')

    # Take a random walk, for a while
    d = random.randrange(0, 4)
    for _ in range(random.randrange(self._width + self._height,
                                    self._width * self._height + 2)):
      self._paint((x, y), '.')
      dx, dy = movement.ALL_MOTIONS[d]
      x += dx
      y += dy
      x = max(0, min(x, self._width - 1))
      y = max(0, min(y, self._height - 1))
      d = (d + random.choice([-1, 0, 0, 0, 0, 0, 1])) % 4  # Turn sometimes

    start = self._random_passable()
    self._passable.discard(start)
    end = self._random_passable()
    self._paint(end, '$')

    n_squares = len(self._passable)
    for _ in range(random.randrange(n_squares // 6, n_squares // 4 + 1)):
      p = self._random_passable()
      self._paint(p, '^')
      if not self._is_reachable(start, end):
        # Oops, put it back.
        self._paint(p, '.')

    grid = list(map(''.join, self._grid))
    return World(start, grid)

  def _random_passable(self):
    return random.choice(tuple(self._passable))

  def _paint(self, p, ch):
    self._grid[p[1]][p[0]] = ch
    if ch == '.':
      self._passable.add(p)
    else:
      self._passable.discard(p)

  def _is_reachable(self, start, end):
    work = [start]
    visited = set(work)
    if start == end:
      return True
    while work:
      (x, y) = work.pop()
      for dx, dy in movement.ALL_MOTIONS:
        p = x + dx, y + dy
        if p == end:
          return True
        elif self._is_passable(p) and p not in visited:
          visited.add(p)
          work.append(p)
    return False

  def _is_passable(self, p):
    return p in self._passable
