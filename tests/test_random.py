"""
Agent-based model based in Chang (2015), "Computational Industrial Economics: A generative approach to dynamic analysis in industrial organization". Additional features are described in my master thesis for Panthéon-Sorbonne MSc in Economics.

Author: João Dimas (joaohenriqueavila@gmail.com)
Supervisor: Prof. Angelo Secchi (Paris 1, PSE)

"""

import unittest
from model.util.random import Random

class TestRandom(unittest.TestCase):

    def test_appendFakeRandom(self):
        random = Random()
        for x in range(0,11):
            random.appendFakeRandom(x/10)

        for x in range(0,11):
            self.assertEqual(random.random(), x/10)