# Command: python3.6 -m unittest tests.TestRandom

import unittest, math
from model.util.Combinatorics import Combinatorics

class TestCombinatorics(unittest.TestCase):

    def test_all_combinations(self):
        numberOfTasks = 96
        maxMagnitudeOfTechChange = 2
        iterable = range(1, numberOfTasks+1)

        # print('Calling: Random.all_combinations')
        allCombinationsInRange = Combinatorics.all_combinations(iterable, 0, maxMagnitudeOfTechChange)
        # print("Length of allCombinationsInRange: {:d}".format(len(allCombinationsInRange)))
        self.assertIsInstance(allCombinationsInRange, list)

        for magnitude in range(0, maxMagnitudeOfTechChange+1):
            allCombinations = list(combinations for combinations in allCombinationsInRange if len(combinations) == magnitude)
            numberOfCombinations = len(allCombinations)
            # print("{:d} combinations with magnitude {:d}".format(len(allCombinations), magnitude))

            # Magnitude: combinations
            # 0: 96! / ((96 - 0)! * 0!)
            # 1: 96! / ((96 - 1)! * 1!)
            # 2: 96! / ((96 - 2)! * 2!) 
            # 3: 96! / ((96 - 3)! * 3!)
            # ...
            # 8: 96! / ((96 - 8)! * 8!)
            trueNumberOfCombinations = math.factorial(numberOfTasks) / (math.factorial(numberOfTasks - magnitude) * math.factorial(magnitude))
            # print("True number of combinations with magnitude {:d}: {:f}".format(magnitude, trueNumberOfCombinations))
            self.assertEqual(numberOfCombinations, trueNumberOfCombinations)

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





