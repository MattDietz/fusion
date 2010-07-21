import unittest
import eventlet

pool = eventlet.GreenPool()

class EventedTestSuite(unittest.TestSuite):
    def __init__(self, tests=(), pool=pool):
        self.pool = pool
        unittest.TestSuite.__init__(self, tests)

    def run(self, result):
        for test in self._tests:
            if isinstance(test, EventedTestSuite):
                test(result)
            else:
                self.pool.spawn_n(test, result)
        self.pool.waitall()

class Fusion(object):
    def __init__(self):
        unittest.TestLoader.suiteClass = EventedTestSuite
        unittest.main()
        
main = Fusion

