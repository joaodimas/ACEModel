import unittest
from model.util.math import Math

class TestMath(unittest.TestCase):

    def test_isEquivalent(self):
        
        self.assertTrue(Math.isEquivalent(5, 5.1, 0))
        self.assertFalse(Math.isEquivalent(5, 5.1, 1))
        self.assertTrue(Math.isEquivalent(5, 5.01, 1))
        self.assertFalse(Math.isEquivalent(5, 5.01, 2))
        self.assertTrue(Math.isEquivalent(5, 5.001, 2))
        self.assertFalse(Math.isEquivalent(5, 5.001, 3))
        self.assertTrue(Math.isEquivalent(5, 5.0001, 3))
        self.assertFalse(Math.isEquivalent(5, 5.0001, 4))
        self.assertTrue(Math.isEquivalent(5, 5.00001, 4))
        self.assertFalse(Math.isEquivalent(5, 5.00001, 5))
        self.assertFalse(Math.isEquivalent(5, 5.00001))

