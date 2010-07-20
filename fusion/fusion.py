import unittest
import eventlet

class EventedTestSuite(unittest.TestSuite):
    def run(self, result):
        pool = eventlet.GreenPool()
        for test in self._tests:
            pool.spawn_n(test, result)
        pool.waitall()

class Fusion(object):
    def __init__(self):
        unittest.TestLoader.suiteClass = EventedTestSuite
        unittest.main()
        
main = Fusion

