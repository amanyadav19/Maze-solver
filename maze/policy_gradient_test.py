import numpy as np
import tensorflow as tf
import unittest

from maze import movement
from maze import simulation
from maze import world
import maze.policy_gradient as pg


class TestPolicyGradientNetwork(unittest.TestCase):
  def testPredict(self):
    g = tf.Graph()
    net = pg.PolicyGradientNetwork('testPredict', g, (7, 11))

    s = tf.Session(graph=g)
    with g.as_default():
      init = tf.global_variables_initializer()
      s.run(init)

    sim = simulation.Simulation(world.Generator(11, 7))
    state = sim.to_array()
    [[act], _] = net.predict(s, [state])
    self.assertTrue(0 <= act)
    self.assertTrue(act < len(movement.ALL_ACTIONS))

  def testTrain(self):
    g = tf.Graph()
    net = pg.PolicyGradientNetwork('testTrain', g, (4, 4))

    s = tf.Session(graph=g)
    with g.as_default():
      init = tf.global_variables_initializer()
      s.run(init)

    sim = simulation.Simulation(world.Generator(4, 4))
    state = sim.to_array()
    net.train(s, [[(state, 3, 7), (state, 3, -1)], [(state, 0, 1000)]])

  def testActionOut_untrainedPrediction(self):
    g = tf.Graph()
    net = pg.PolicyGradientNetwork('testActionOut_untrainedPrediction', g,
                                   (17, 13))
    s = tf.Session(graph=g)
    with g.as_default():
      init = tf.global_variables_initializer()
      s.run(init)
    act = s.run(net.action_out,
                feed_dict={net.state: [np.zeros((17, 13))]})
    self.assertTrue(0 <= act)
    self.assertTrue(act < len(movement.ALL_ACTIONS))

  def testUpdate(self):
    g = tf.Graph()
    net = pg.PolicyGradientNetwork('testUpdate', g, (13, 23))
    s = tf.Session(graph=g)
    with g.as_default():
      init = tf.global_variables_initializer()
      s.run(init)
    s.run(net.update, feed_dict={
        net.state: np.zeros((7, 13, 23)),
        net.action_in: np.zeros((7, 1)),
        net.advantage: np.zeros((7, 1)),
      })

  def testUpdate_lossDecreases(self):
    w = world.World.parse('@.....$')

    g = tf.Graph()
    net = pg.PolicyGradientNetwork('testUpdate_lossDecreases', g, (w.h, w.w))
    s = tf.Session(graph=g)
    with g.as_default():
      init = tf.global_variables_initializer()
      s.run(init)

    state = simulation.Simulation(world.Static(w)).to_array()
    losses = []
    for _ in range(10):
      loss, _ = s.run([net.loss, net.update], feed_dict={
            net.state: [state],
            net.action_in: [[1]],
            net.advantage: [[2]]
          })
      losses.append(loss)
    self.assertTrue(losses[-1] < losses[0])
