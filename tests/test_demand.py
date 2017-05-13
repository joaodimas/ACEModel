import unittest, datetime
from model.util.logger import Logger
from model.firm import Firm
from model.technology import Technology
from model.industry import Industry
from model.parameters import Parameters
from simulation import SystemConfig

class TestDemand(unittest.TestCase):

    def test_updateEqPrice(self):
        # Firm (self, firmId, industry, technology)
        # q = s * ((1 / (m + 1)) * (a + sumOfMC) - c)
        Parameters.NumberOfTasks = 5
        Parameters.DemandIntercept = 300
        Parameters.MaximumOptimalTechnologies = 1
        optimalTech = 0b10101
        industry = Industry(1)
        industry.currentOptimalTechs = []
        industry.random.appendFakeGetRandBits(optimalTech) # Will be obtained by Industry's constructor to define optimal tech.
        industry.addNewOptimalTech()
        industry.nextPeriod()
        self.assertEqual(industry.currentOptimalTechs[0].tasks, optimalTech)
        
        firm1 = Firm(1, industry, Technology(industry=industry, tasks=0b00000)) # Dist = 3
        industry.activeFirms.append(firm1)
        self.assertEqual(firm1.updateMarginalCost(), 60)

        firm2 = Firm(2, industry, Technology(industry=industry, tasks=0b10000)) # Dist = 2
        self.assertEqual(firm2.updateMarginalCost(), 40)
        industry.activeFirms.append(firm2)
        
        firm3 = Firm(3, industry, Technology(industry=industry, tasks=0b10100)) # Dist = 1
        self.assertEqual(firm3.updateMarginalCost(), 20)
        industry.activeFirms.append(firm3)

        self.assertEqual(industry.updateSumOfActiveFirmsMC(), 120)
        
        # P = 1 / (m + 1) * (a + sumOfMC) = 1 / (3 + 1) * (300 + 120) = 105
        industry.demand.updateEqPrice()
        self.assertEqual(industry.demand.eqPrice, 105)

    def setUp(self):
        Logger.initialize(datetime.datetime.now(), SystemConfig.LogLevel)
        Parameters.setInitialParameters()