import unittest, datetime
from model.util.Random import Random
from model.util.Logger import Logger
from model.Firm import Firm
from model.Technology import Technology
from model.Industry import Industry
from model.Parameters import Parameters

class TestDemand(unittest.TestCase):

    def test_updateEqPrice(self):
        # Firm (self, firmId, industry, technology)
        # q = s * ((1 / (m + 1)) * (a + sumOfMC) - c)
        Parameters.NumberOfTasks = 5
        Parameters.DemandIntercept = 300
        optimalTech = 0b10101
        Random.appendFakeGetRandBits(optimalTech) # Will be obtained by Industry's constructor to define optimal tech.
        industry = Industry(1)
        industry.nextPeriod()
        self.assertEqual(industry.currentOptimalTech.tasks, optimalTech)
        
        firm1 = Firm(1, industry, Technology(0b00000)) # Dist = 3
        firm1.updateMarginalCost()
        industry.activeIncumbentFirms.append(firm1)
        self.assertEqual(firm1.MC, 60)

        firm2 = Firm(2, industry, Technology(0b10000)) # Dist = 2
        firm2.updateMarginalCost()
        self.assertEqual(firm2.MC, 40)
        industry.activeIncumbentFirms.append(firm2)
        
        firm3 = Firm(3, industry, Technology(0b10100)) # Dist = 1
        firm3.updateMarginalCost()
        self.assertEqual(firm3.MC, 20)
        industry.activeIncumbentFirms.append(firm3)

        industry.updateSumOfMC()
        self.assertEqual(industry.currentActiveSumOfMC, 120)
        
        # P = 1 / (m + 1) * (a + sumOfMC) = 1 / (3 + 1) * (300 + 120) = 105
        industry.demand.updateEqPrice()
        self.assertEqual(industry.demand.eqPrice, 105)

    def setUp(self):
        timestamp = datetime.datetime.now()
        Logger.initialize(timestamp)