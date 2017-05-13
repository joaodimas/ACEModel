import unittest
from model.util.random import Random

class TestRandom(unittest.TestCase):

    def test_appendFakeRandom(self):
        random = Random()
        for x in range(0,11):
            random.appendFakeRandom(x/10)

        for x in range(0,11):
            self.assertEqual(random.random(), x/10)