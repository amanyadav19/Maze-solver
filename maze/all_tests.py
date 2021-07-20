#!/usr/bin
import unittest

from maze import context_test
from maze import grid_test
from maze import policy_gradient_test
from maze import simulation_test
from maze import world_test


def load_tests(loader, unused_tests, unused_pattern):
  # pylint: disable=unused-argument
  test_modules = [
      context_test,
      grid_test,
      policy_gradient_test,
      simulation_test,
      world_test,
    ]
  return unittest.TestSuite(map(loader.loadTestsFromModule, test_modules))


if __name__ == '__main__':
  unittest.main()
