# Command: python3.6 -m unittest tests.TestCombinatorics

import unittest, itertools, math
from model.util.combinatorics import Combinatorics
from model.util.math import Math

class TestCombinatorics(unittest.TestCase):

    def test_2_getProbabilitiesOfDrawingSize(self):
        numberOfTasks = 96
        maxDistance = 4
        minDistance = 0
        probs = Combinatorics.getProbabilitiesOfDrawingSize(numberOfTasks, minDistance, maxDistance)

        tasks = list(range(1, numberOfTasks+1))
        allTechs = []
        totalNmbCombs = 0
        for d in range(minDistance, maxDistance+1):
            combs = list(itertools.combinations(tasks, d))
            allTechs.append(combs)
            totalNmbCombs += len(combs)

        trueTotalNmbCombs = 0
        for x in range(minDistance, maxDistance+1):
            trueTotalNmbCombs += math.factorial(numberOfTasks) / (math.factorial(x) * math.factorial(numberOfTasks - x))

        self.assertEquivalent(totalNmbCombs, trueTotalNmbCombs)

        for x in range(minDistance, maxDistance+1):
            p = [p for d, p in probs if d == x][0]
            trueP = len(allTechs[x])/totalNmbCombs
            self.assertEquivalent(p, trueP)
            trueP = math.factorial(numberOfTasks) / (math.factorial(x) * math.factorial(numberOfTasks - x)) / trueTotalNmbCombs
            self.assertEquivalent(p, trueP)
            trueP = math.factorial(numberOfTasks) / math.factorial(x) / math.factorial(numberOfTasks - x) / trueTotalNmbCombs
            self.assertEquivalent(p, trueP)

        # With distance 8

        maxDistance = 8
        probs = Combinatorics.getProbabilitiesOfDrawingSize(numberOfTasks, minDistance, maxDistance)

        sumOfP = 0
        for d, p in probs:
            sumOfP += p
        self.assertEqual(sumOfP, 1)

        tasks = list(range(1, numberOfTasks+1))

        trueTotalNmbCombs = 0
        for x in range(minDistance, maxDistance+1):
            trueTotalNmbCombs += math.factorial(numberOfTasks) / (math.factorial(x) * math.factorial(numberOfTasks - x))

        for x in range(minDistance, maxDistance+1):
            p = [p for d, p in probs if d == x][0]
            trueP = math.factorial(numberOfTasks) / math.factorial(x) / math.factorial(numberOfTasks - x) / trueTotalNmbCombs
            self.assertEquivalent(p, trueP)


    def test_getProbabilitiesOfDrawingSize(self):
        numberOfTasks = 10
        maxMagnitudeOfTechChange = 3
        choices = Combinatorics.getProbabilitiesOfDrawingSize(numberOfTasks, 0, maxMagnitudeOfTechChange)
        self.assertTrue(len(choices)>1)

        # Total = 176 combinations
        # 3 draws: 10! / ((10 - 3)! * 3!) = 120 (prob: 0.681; cumulative: 0.681)
        prob3 = 120/176
        cumul3 = 120/176
        # 2 draws: 10! / ((10 - 2)! * 2!) = 45 (prob: 0.937; cumulative: 0.937)
        prob2 = 45/176
        cumul2 = (120+45)/176
        # 1 draw: 10! / ((10 - 1)! * 1!) = 10 (prob: 0.056; cumulative: 0.994)
        prob1 = 10/176
        cumul1 = (120+45+10)/176
        # 0 draws: 10! / ((10 - 0)! * 0!) = 1 (prob: 0.005; cumulative: 1)
        prob0 = 1
        cumul0 = 1


        selectionPoint = cumul3 - 0.0000001
        selection = None
        cumulative = 0
        tempChoices = list(choices)
        # print("Selecting 3. len(tempChoices)={:d}".format(len(tempChoices)))
        while selection is None:
            r, prob = tempChoices.pop()
            # print('r={:d}, prob={:.2f}, len(tempChoices)={:d}'.format(r, prob, len(tempChoices)))
            cumulative += prob
            if(r == 0): 
                self.assertEqual(prob, prob0)
                self.assertEqual(cumulative, cumul0)
            if(r == 1):
                self.assertEqual(prob, prob1)
                self.assertEqual(cumulative, cumul1)
            if(r == 2):
                self.assertEqual(prob, prob2)
                self.assertEqual(cumulative, cumul2)
            if(r == 3):
                self.assertEqual(prob, prob3)
                self.assertEqual(cumulative, cumul3)
            if cumulative > selectionPoint:
                selection = r
        self.assertEqual(selection, 3)

        selectionPoint = cumul2 - 0.0000001
        selection = None
        cumulative = 0
        tempChoices = list(choices)
        # print("Selecting 2. len(tempChoices)={:d}".format(len(tempChoices)))
        while selection is None:
            r, prob = tempChoices.pop()
            # print('r={:d}, prob={:.2f}, len(tempChoices)={:d}'.format(r, prob, len(tempChoices)))
            cumulative += prob
            if cumulative > selectionPoint:
                selection = r
        self.assertEqual(selection, 2)

        selectionPoint = cumul1 - 0.0000001
        selection = None
        cumulative = 0
        tempChoices = list(choices)
        # print("Selecting 1. len(tempChoices)={:d}".format(len(tempChoices)))
        while selection is None:
            r, prob = tempChoices.pop()
            # print('r={:d}, prob={:.2f}, len(tempChoices)={:d}'.format(r, prob, len(tempChoices)))
            cumulative += prob
            if cumulative > selectionPoint:
                selection = r
        self.assertEqual(selection, 1)

        selectionPoint = cumul0 - 0.0000001
        selection = None
        cumulative = 0
        tempChoices = list(choices)
        # print("Selecting 0. len(tempChoices)={:d}".format(len(tempChoices)))
        while selection is None:
            r, prob = tempChoices.pop()
            # print('r={:d}, prob={:.2f}, len(tempChoices)={:d}'.format(r, prob, len(tempChoices)))
            cumulative += prob
            if cumulative > selectionPoint:
                selection = r
        self.assertEqual(selection, 0)

    def assertEquivalent(self, a, b):   
        self.assertTrue(Math.isEquivalent(a, b), msg='{0}, {1}'.format(a, b))



