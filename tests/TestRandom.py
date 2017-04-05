import unittest
from model.util.Random import Random

class TestRandom(unittest.TestCase):

    def test_appendFakeRandom(self):

        for x in range(0,11):
            Random.appendFakeRandom(x/10)

        for x in range(0,11):
            self.assertEqual(Random.random(), x/10)