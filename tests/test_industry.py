import unittest, datetime
from model.industry import Industry
from model.parameters import Parameters
from model.firm import Firm
from model.shocks import Shocks
from model.technology import Technology
from model.demand import Demand
from model.util.random import Random
from model.util.math import Math
from model.util.logger import Logger

class TestIndustry(unittest.TestCase):

    def test_ProcessPeriod(self):
        print('')
        industry = Industry(1)
        optTasks = industry.currentOptimalTech.tasks
        industry.nextPeriod()

        Random.appendFakeRandom(1) # Higher than tech change rate => No shock.
        Shocks.processShocks(industry)
        self.assertEqual(optTasks, industry.currentOptimalTech.tasks) # No shock indeed.
        self.assertEqual(len(industry.survivorsOfPreviousPeriod), 0) # No firm yet.

        industry.processResearch()
        self.assertEqual(industry.nmbResearching, 0) # No firm yet.

        industry.activateAllIncumbents()
        self.assertEqual(len(industry.activeFirms), 0) # No firm yet
        
        industry.potentialEntrants = []

        sumOfMC = 0
        sumOfExpOutput = 0
        for x in range(40):
            firm = Firm(x+1, industry, Technology(optTasks))
            for t in range(x):
                firm.technology.flipTask(t+1)

            industry.potentialEntrants.append(firm)
            firm.decideIfEnters()
            sumOfMC += firm.MC
            sumOfExpOutput += firm.expOutput
            self.assertEqual(firm.techDistToOptimal, x)
            firm.techDistToOptimal = None
            self.assertTrue(Math.isEquivalent(firm.MC, x/96*100))
            self.assertEqual(firm.expPrice, 1/2*(Parameters.DemandIntercept + firm.MC))  
            self.assertEqual(firm.expPrice, Demand.calculatePrice(1, Parameters.DemandIntercept, firm.MC))
            self.assertTrue(Math.isEquivalent(firm.expOutput, industry.demand.marketSize*(1/(1+1)*(Parameters.DemandIntercept+firm.MC)-firm.MC)))
            self.assertTrue(Math.isEquivalent(firm.expOutput, Demand.calculateFirmOutput(industry.demand.marketSize, 1, Parameters.DemandIntercept, firm.MC, firm.MC)))
            self.assertTrue(Math.isEquivalent(firm.expOutput, Demand.calculateAggregateOutput(industry.demand.marketSize, 1, Parameters.DemandIntercept, firm.MC)))
            self.assertTrue(Math.isEquivalent(firm.expProfits, (Parameters.DemandIntercept-1/industry.demand.marketSize*firm.expOutput)*firm.expOutput-Parameters.FixedProductionCost-firm.MC*firm.expOutput))
            self.assertTrue(Math.isEquivalent(firm.expProfits, firm.expOutput * (firm.expPrice-firm.MC) - Parameters.FixedProductionCost))
            self.assertEqual(firm.expProfits, firm.expWealth)
            firm.expPrice = None
            firm.MC = None
            firm.expOutput = None
            firm.expProfits = None
            firm.expWealth = None

        self.assertTrue(Math.isEquivalent(sumOfMC, 812.50000))
        self.assertTrue(Math.isEquivalent(sumOfExpOutput, 22375.00000))
        self.assertTrue(Math.isEquivalent(Demand.calculatePrice(40, Parameters.DemandIntercept, sumOfMC), 27.13414))
        
        industry.processFirmsEntering()
        self.assertEqual(industry.nmbEnteringFirms, 40)
        self.assertEqual(len(industry.incumbentFirms), 40)
        self.assertEqual(len(industry.activeFirms), 40)

        industry.incumbentFirms = sorted(industry.incumbentFirms, key=lambda firm: firm.firmId)
        for x in range(40):
            if(x < 39):
                self.assertGreater(industry.incumbentFirms[x].expProfits, industry.incumbentFirms[x+1].expProfits)

        # Some firms might decide to not produce
        industry.processShutdownDecisions()

        self.assertTrue(Math.isEquivalent(len(industry.activeFirms),23))
        self.assertTrue(Math.isEquivalent(industry.sumOfActiveFirmsMC, 263.54167))
        self.assertTrue(Math.isEquivalent(industry.demand.eqPrice, 23.48090))

        # # Now we have only the incumbents that are willing to produce
        industry.updateActiveIncumbents()
        self.assertTrue(Math.isEquivalent(industry.industryOutput, 1106.07639))

        industry.activeFirms = sorted(industry.activeFirms, key=lambda firm: firm.firmId)
        for x in range(len(industry.activeFirms)):
             firm = industry.activeFirms[x]
             self.assertTrue(Math.isEquivalent(firm.MC, x/96*100))
             trueOutput = industry.demand.marketSize * ((1/(len(industry.activeFirms)+1))*(Parameters.DemandIntercept+industry.sumOfActiveFirmsMC)-firm.MC)
             self.assertTrue(Math.isEquivalent(firm.output, trueOutput))
             trueProfits = (Parameters.DemandIntercept - industry.industryOutput / industry.demand.marketSize) * firm.output - Parameters.FixedProductionCost - firm.MC * firm.output
             self.assertTrue(Math.isEquivalent(firm.profits, trueProfits))


    def setUp(self):
        Logger.initialize(datetime.datetime.now())