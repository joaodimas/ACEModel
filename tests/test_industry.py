import unittest
from model.industry import Industry
from model.firm import Firm
from model.shocks import Shocks
from model.technology import Technology
from model.util.random import Random

class TestIndustry(unittest.TestCase):

    def test_LowerCostsHigherProfits(self):
        industry = Industry(1)
        optTasks = industry.currentOptimalTech.tasks
        industry.nextPeriod()

        Random.appendFakeRandom(1) # Higher than tech change rate => No shock.
        Shocks.processShocks(industry)
        self.assertEqual(optTasks, industry.currentOptimalTech.tasks) # No shock indeed.
        self.assertEqual(len(industry.survivorsOfPreviousPeriod), 0) # No firm yet.

        # Each survivor will decide by doing or not R&D
        self.processResearch()
        self.assertEqual(industry.nmbResearching, 0) # No firm yet.

        # Activate survivors
        self.activateAllIncumbents()
        self.assertEqual(len(industry.activeFirms), 0) # No firm yet
        
        industry.potentialEntrants = []
        
        firm1 = Firm(1, industry, Technology(optTasks))
        industry.potentialEntrants.append(firm1)
        firm1.decideIfEnters()
        self.assertEqual(firm1.MC, 0)
        self.assertEqual(firm1.)

        industry.potentialEntrants.append(Firm(1, industry, Technology(optTasks).flipTask(1)))
        industry.potentialEntrants.append(Firm(2, industry, Technology(optTasks).flipTask(1).flipTask(2)))
        industry.potentialEntrants.append(Firm(3, industry, Technology(optTasks).flipTask(1).flipTask(2).flipTask(3)))
        industry.potentialEntrants.append(Firm(4, industry, Technology(optTasks).flipTask(1).flipTask(2).flipTask(3).flipTask(4)))


        # See which potential entrants will enter the market (i.e. become an incumbent)
        self.processFirmsEntering()


        # Some firms might decide to not produce
        self.processShutdownDecisions()

        # Now we have only the incumbents that are willing to produce
        self.updateActiveIncumbents()