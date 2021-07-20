import unittest

from maze import context


class TestRunLoop(unittest.TestCase):
  def test_empty_run_loop_quits(self):
    run_loop = context.RunLoop()
    run_loop.start()
    # Test passes if this does not hang.

  def test_post_task(self):
    run_loop = context.RunLoop()
    log = []
    run_loop.post_task(lambda: log.append('a'))
    self.assertEqual([], log,
                     'post_task should not complete tasks synchronously')
    run_loop.start()
    self.assertEqual(['a'], log, 'run loop should have run the callback')

  def test_posted_tasks_run_in_order(self):
    run_loop = context.RunLoop()
    log = []
    run_loop.post_task(lambda: log.append('a'))
    run_loop.post_task(lambda: log.append('b'))
    run_loop.start()
    self.assertEqual(['a', 'b'], log,
                     'run loop should run tasks in the order they are posted')

  def test_post_quit(self):
    run_loop = context.RunLoop()
    log = []
    run_loop.post_task(lambda: log.append('a'))
    run_loop.post_task(lambda: run_loop.post_quit())
    run_loop.post_task(lambda: run_loop.post_task(lambda: log.append('c')))
    run_loop.post_task(lambda: log.append('b'))
    run_loop.start()
    self.assertEqual(
        ['a', 'b'], log,
        'run loop should run tasks posted before quit, but not after')

  def test_post_repeat(self):
    run_loop = context.RunLoop()
    n = 0
    def count():
      nonlocal n
      n += 1
      if n == 3:
        run_loop.post_quit()
    run_loop.post_task(count, repeat=True)
    run_loop.start()
    self.assertEqual(3, n, 'the task should have run repetitively')
