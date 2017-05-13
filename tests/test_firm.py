#!/usr/bin/env python3

# Command: python3.6 -m unittest tests.TestFirm

import unittest, datetime
from model.firm import Firm
from model.industry import Industry
from model.technology import Technology
from model.parameters import Parameters
from model.util.random import Random
from model.util.logger import Logger
from simulation import SystemConfig

class TestFirm(unittest.TestCase):

    def test_updateMarginalCost(self):
        # Firm (self, firmId, industry, technology)
        oldNumberOfTasks = Parameters.NumberOfTasks
        Parameters.NumberOfTasks = 10
        optimalTech = 0b0000000000

        Random.appendFakeGetRandBits(optimalTech) # Will be obtained by Industry's constructor to define optimal tech.
        industry = Industry(1)

        # Cases for Hamming distances from 0 to all tasks
        for dist in range(Parameters.NumberOfTasks+1):
            #print("dist={:d}".format(dist))
            for i in range(Parameters.NumberOfTasks-(dist-1)):
                tasks = 0
                for j in range(i,dist+i):
                    tasks += 2 ** j

                #print("tasks={:010b}".format(tasks))
                firm = Firm(1, industry, Technology(tasks))
                firm.updateMarginalCost()
                self.assertEqual(firm.MC, 100*dist/Parameters.NumberOfTasks)

        Parameters.NumberOfTasks = oldNumberOfTasks

    def test_updateOutput(self):

        # Firm (self, firmId, industry, technology)
        Parameters.NumberOfTasks = 5
        Parameters.MeanMarketSize = 4
        optimalTech = 0b10101
        Random.appendFakeGetRandBits(optimalTech) # Will be obtained by Industry's constructor to define optimal tech.
        industry = Industry(1)
        industry.nextPeriod()
        self.assertEqual(industry.currentOptimalTech.tasks, optimalTech)
        
        firm1 = Firm(1, industry, Technology(0b00000)) # Dist = 3
        self.assertEqual(firm1.updateMarginalCost(), 60)
        industry.activeFirms.append(firm1)

        firm2 = Firm(2, industry, Technology(0b10000)) # Dist = 2
        self.assertEqual(firm2.updateMarginalCost(), 40)
        industry.activeFirms.append(firm2)
        
        firm3 = Firm(3, industry, Technology(0b10100)) # Dist = 1
        self.assertEqual(firm3.updateMarginalCost(), 20)
        industry.activeFirms.append(firm3)

        self.assertEqual(industry.updateSumOfActiveFirmsMC(), 120)
        
        # q = s * ((1 / (m + 1)) * (a + sumOfMC) - c)
        self.assertEqual(industry.demand.updateEqPrice(), 105)

        
        self.assertEqual(firm1.updateOutput(), 180)
        self.assertEqual(firm2.updateOutput(), 260)
        self.assertEqual(firm3.updateOutput(), 340)

    def test_selectCompetitorFromRouletteWheel(self):
        # Parameters
        numberOfOtherCompetitors = 41

        industry = Industry(1)
        industry.profitableFirmsPrevPeriod = []
        sumOfProfits = 0
        for firmId in range(1, numberOfOtherCompetitors + 1):
            firm = Firm(firmId, industry, Technology.generateRandomTechnology())
            firm.profits = firmId * 100
            sumOfProfits += firm.profits
            # sumOfProfits is 1*100 + 2*100 + 3*100 + ... + numberOfFirms*100
            # Or: 100 * (numberOfFirms + 1) * numberOFFirms / 2. In case of 41 firms, sumOfProfits = 86,100
            # Expected point in CDF after each loop:
            # 1) 100/86100 = .00116144
            # 2) 100/86100 + 200/86100 = 300/86100 = .003484321
            # ...
            # 11) 6600/86100 = .076655052 
            # ...
            # 21) 23100/86100 = .268292683
            # ...
            # 30) 46500/86100 = .540069686
            # 31) 49600/86100 = .576074332 <----- Selected competitor
            # ...
            # 41) 86100/86100 = 1

            industry.profitableFirmsPrevPeriod.append(firm)

        firmA = Firm(numberOfOtherCompetitors+1, industry, Technology.generateRandomTechnology())
        industry.profitableFirmsPrevPeriod.append(firmA)

        for competitorToBeSelected in range(1, numberOfOtherCompetitors+1):
            pointInCDFBefore = 100 * (competitorToBeSelected) * (competitorToBeSelected - 1) / 2 / sumOfProfits
            pointInCDFAfter = 100 * (competitorToBeSelected + 1) * competitorToBeSelected / 2 / sumOfProfits
            middlePoint = (pointInCDFAfter + pointInCDFBefore) / 2
            firmB = firmA.selectCompetitorFromRouletteWheel(middlePoint)
            self.assertIsNotNone(firmB)
            self.assertEqual(firmB.firmId, competitorToBeSelected)

    def setUp(self):
        Logger.initialize(datetime.datetime.now(), SystemConfig.LogLevel)