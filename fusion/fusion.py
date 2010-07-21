import unittest
import eventlet
import types
import sys
import time

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

class EventedTextTestRunner(unittest.TextTestRunner):
    def run(self, test, pool=pool):
        result = self._makeResult()
        startTime = time.time()
        test(result)

        # Where the magic happens
        pool.waitall()
        
        stopTime = time.time()
        timeTaken = stopTime - startTime
        result.printErrors()
        self.stream.writeln(result.separator2)
        run = result.testsRun
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (run, run != 1 and "s" or "", timeTaken))
        self.stream.writeln()
        if not result.wasSuccessful():
            self.stream.write("FAILED (")
            failed, errored = map(len, (result.failures, result.errors))
            if failed:
                self.stream.write("failures=%d" % failed)
            if errored:
                if failed: self.stream.write(", ")
                self.stream.write("errors=%d" % errored)
            self.stream.writeln(")")
        else:
            self.stream.writeln("OK")
        return result

class Fusion(object):
    def __init__(self):
        unittest.TestLoader.suiteClass = EventedTestSuite
        unittest.main(testRunner=EventedTextTestRunner)
        
main = Fusion

