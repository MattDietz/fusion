An eventlet based version of the python unittest module. Used primarily as a means of speeding up integration testing while using a familiar framework.


Example:

<pre>
import fusion
import unittest

class SampleTest(unittest.TestCase):
    def test_foo(self):
        self.assertEqual(True, True)

    def test_bar(self):
        self.assertEqual(True, True)

    def test_fail(self):
        self.assertEqual(True, False)

if __name__ == '__main__':
    fusion.main()
</pre>


Example with sleeps to prove tests are being spawned in a pool:

<pre>
import fusion
import unittest
from eventlet import sleep

class SampleTest(unittest.TestCase):
    def test_foo(self):
        sleep(4)
        self.assertEqual(True, True)

    def test_bar(self):
        sleep(3)
        self.assertEqual(True, True)

    def test_fail(self):
        sleep(1)
        self.assertEqual(True, False)

if __name__ == '__main__':
    fusion.main()
</pre>
