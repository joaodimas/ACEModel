import unittest, datetime
from model.industry import Industry
from model.parameters import Parameters
from model.firm import Firm
from model.exogenous_effects import ExogenousEffects
from model.technology import Technology
from model.demand import Demand
from model.util.random import Random
from model.util.math import Math
from model.util.logger import Logger
from simulation import SystemConfig

class TestIndustry(unittest.TestCase):

    # Hypothesis: 
    #  When there are previous incumbents, 
    #  (1) potential entrants are miscalculating expected profits when deciding to enter;
    #  (2) incumbents are miscalculating expected profits when deciding to shutdown;
    def test_ProcessPeriod_entryDecisions_previousIncumbents(self):
        self.assertTrue(Random.noFakes())
        Parameters.MaximumOptimalTechnologies = 1
        industry = Industry(1)
        industry.nextPeriod()
        optTasks = industry.currentOptimalTechs[0].tasks

        prevIncumbentsMC = 100*10/96
        trueNumberOfPrevIncumbents = 13
        trueSumOfPrevIncumbentsMC = 135.416667
        for x in range(trueNumberOfPrevIncumbents):
            technology = Technology(optTasks)
            for x in range(10):
                technology = technology.flipTask(x+1)
            firm = Firm(x+1, industry, technology)
            industry.survivorsOfCurrentPeriod.append(firm)
            industry.activeSurvivorsOfCurrentPeriod.append(firm)
            
            firm.updateMarginalCost()
            
            self.assertEquivalent(firm.MC, prevIncumbentsMC)

        industry.updateSumOfActiveSurvivorsMC()
        
        self.assertEquivalent(industry.sumOfActiveSurvivorsMC, trueSumOfPrevIncumbentsMC)

        # We created survivorsOfCurrentPeriod such that the equilibrium price is below 31. Thus, (1) the 10 least efficient firms will not enter because their MC is above expected price, and (2) more 6 firms wont enter because, even though the price is above their MC, the expected profits wont cover fixed costs.
        # Therefore, we expect that only the 23 most efficient firms, from a total of 40, will enter the market.
        industry.nextPeriod()

        Random.appendFakeRandom(1) # Higher than tech change rate => No shock.
        ExogenousEffects.process(industry)
        Random.clearAllFakes()
        
        self.assertEqual(optTasks, industry.currentOptimalTechs[0].tasks) # No shock indeed.

        for x in range(trueNumberOfPrevIncumbents): # No firm will perform R&D
            Random.appendFakeRandom(1)
        industry.processResearch()
        Random.clearAllFakes()
        self.assertEqual(industry.nmbResearching, 0)
        self.assertEqual(industry.nmbImitating, 0)
        self.assertEqual(industry.nmbInnovating, 0)
        self.assertEqual(industry.totalInvestmentInResearch, 0)
        self.assertEqual(industry.totalInvestmentInImitation, 0)
        self.assertEqual(industry.totalInvestmentInInnovation, 0)

        industry.activateAllIncumbents()
        
        self.assertEqual(len(industry.activeFirms), 13)
        
        industry.potentialEntrants = []

        sumOfMC = 0
        sumOfExpOutput = 0
        for x in range(40):
            firm = Firm(x+101, industry, Technology(optTasks)) # The Ids will start at 101 so they don't repeat with the previous incumbents.
            for t in range(x):
                firm.technology.flipTask(t+1)

            industry.potentialEntrants.append(firm)
            firm.decideIfEnters()
            sumOfMC += firm.MC
            sumOfExpOutput += firm.expOutput
            self.assertEqual(firm.techDistToOptimal, x)
            firm.techDistToOptimal = None
            self.assertEquivalent(firm.MC, x/96*100)
            self.assertEquivalent(firm.expPrice, 1/(trueNumberOfPrevIncumbents+2)*(Parameters.DemandIntercept + trueSumOfPrevIncumbentsMC + firm.MC))  
            self.assertEquivalent(firm.expPrice, Demand.calculatePrice(trueNumberOfPrevIncumbents + 1, Parameters.DemandIntercept, trueSumOfPrevIncumbentsMC + firm.MC))
            trueExpOutput = industry.demand.marketSize*(1/(trueNumberOfPrevIncumbents + 2)*(Parameters.DemandIntercept+trueSumOfPrevIncumbentsMC+firm.MC)-firm.MC)
            if trueExpOutput < 0:
                trueExpOutput = 0
            self.assertEquivalent(firm.expOutput, trueExpOutput)
            self.assertEquivalent(firm.expOutput, Demand.calculateFirmOutput(industry.demand.marketSize, trueNumberOfPrevIncumbents + 1, Parameters.DemandIntercept, trueSumOfPrevIncumbentsMC + firm.MC, firm.MC) if trueExpOutput > 0 else 0)
            self.assertEquivalent(firm.expProfits, firm.expOutput * (firm.expPrice-firm.MC) - Parameters.FixedProductionCost)
            self.assertEqual(firm.expProfits, firm.expWealth)
            self.assertTrue((firm.expOutput > 0 and firm.firmId <= 130) or (firm.expOutput <= 0 and firm.firmId > 130))
            self.assertTrue((firm.entering and firm.firmId <= 123) or (not firm.entering and firm.firmId > 123))
            self.assertTrue(firm.expProfits > 0 or not firm.entering) 
            self.assertTrue(firm.expProfits <= 0 or firm.entering) 

    
            if firm.firmId == 122: # Just a random firm to check if the values correspond to the true ones.
                self.assertEquivalent(firm.expOutput, 34.444444)

            if 101 <= firm.firmId <= 123:
                self.assertTrue(firm.entering)
            else:
                self.assertFalse(firm.entering)

            firm.expPrice = None
            firm.MC = None
            firm.expOutput = None
            firm.expProfits = None
            firm.expWealth = None

        self.assertEquivalent(sumOfMC, 812.50000)
        self.assertEquivalent(sumOfExpOutput, 1791.66667)
        self.assertEquivalent(Demand.calculatePrice(40, Parameters.DemandIntercept, sumOfMC), 27.13414)
        
        industry.processFirmsEntering()

        self.assertEqual(industry.nmbEnteringFirms, 23)
        self.assertEqual(len(industry.incumbentFirms), 36)
        self.assertEqual(len(industry.activeFirms), 36)

        # At this point, (1) all potential entrants calculated the expected price, output and profits correctly, (2) the total number of incumbents is correct.

        industry.processShutdownDecisions()

        self.assertEquivalent(len(industry.activeFirms),31)
        self.assertEquivalent(industry.sumOfActiveFirmsMC, 294.79167)
        self.assertEquivalent(industry.demand.eqPrice, 18.58724)

        industry.updateActiveIncumbents()

        # Checking two random firms
        self.assertEquivalent([firm.output for firm in industry.activeFirms if firm.firmId == 107][0], 49.34896)
        self.assertEquivalent([firm.output for firm in industry.activeFirms if firm.firmId == 115][0], 16.01562)
        
        self.assertEquivalent(industry.industryOutput, 1125.65104)

        industry.activeFirms = sorted(industry.activeFirms, key=lambda firm: firm.firmId)
        for firm in industry.activeFirms:
            if(firm.firmId <= trueNumberOfPrevIncumbents):
                self.assertEquivalent(firm.MC, 100*10/96)
            elif(firm.firmId > trueNumberOfPrevIncumbents):
                self.assertEquivalent(firm.MC, 100*(firm.firmId - 101)/96)  
            trueOutput = industry.demand.marketSize * ((1/(len(industry.activeFirms)+1))*(Parameters.DemandIntercept+industry.sumOfActiveFirmsMC)-firm.MC)
            self.assertEquivalent(firm.output, trueOutput)
            trueProfits = (Parameters.DemandIntercept - industry.industryOutput / industry.demand.marketSize) * firm.output - Parameters.FixedProductionCost - firm.MC * firm.output
            self.assertEquivalent(firm.profits, trueProfits)

        # At this point, all activeFirms have the correct MC, output and profits.

        self.assertEqual(len(industry.inactiveFirms), 5)

        industry.updateInactiveIncumbents()

        for firm in industry.inactiveFirms:
            self.assertEqual(firm.profits, -Parameters.FixedProductionCost)
            self.assertEqual(firm.wealth, -Parameters.FixedProductionCost)

        industry.updateMarketShares()

        industry.updateWeightedMC()

        # Update the average proximity to optimal technology
        industry.updateAvgProximityToOptTech()

        industry.updateMarketShares()

        # Calculate Herfindahl-Hirschmann Index
        industry.updateHIndex()

        # Calculate the degree of technological diversity
        industry.updateDegreeOfTechDiv()

        # Calculate the Gini coefficient with regard to the market share
        industry.updateGiniCoefficient()    

        # Calculate Price-Cost margin
        industry.updatePCM()

        # Calculate Consumer Surplus
        industry.updateCS()

        # Calculate total profits
        industry.updateTotalProfits()

        # Calculate Total Surplus
        industry.updateTS()

        industry.processExitDecisions()

        for firm in industry.incumbentFirms:
            self.assertTrue((firm.exiting and firm.firmId > 112) or (not firm.exiting and firm.firmId <= 112))


        industry.updateAgeStats()

        self.assertEquivalent(industry.totalProfits, 5195.04920)
        self.assertEqual(industry.nmbExitingFirms, 11) # 11 of the active firms had losses

        industry.processFirmsExiting()

        for firm in industry.survivorsOfCurrentPeriod:
            self.assertTrue(firm.firmId <= 112) 

        industry.updateSumOfActiveSurvivorsMC()

        self.assertEquivalent(industry.sumOfActiveSurvivorsMC, 204.166667)

        # All hyphotesis rejected.


    def test_ProcessPeriod_entryDecisions_noPreviousIncumbents(self):
        self.assertTrue(Random.noFakes())
        Parameters.MaximumOptimalTechnologies = 1
        Parameters.TypeOfCycle = None
        Parameters.DemandIntercept = 300
        Parameters.PeriodStartOfTechnologicalShocks = 99999
        industry = Industry(1)
        industry.currentOptimalTechs[0].tasks = 0
        optTasks = industry.currentOptimalTechs[0].tasks
        industry.nextPeriod()

        ExogenousEffects.process(industry)
        self.assertEqual(industry.demand.marketSize, 4) # No business cycles
        self.assertEqual(optTasks, industry.currentOptimalTechs[0].tasks) # No shock indeed.
        self.assertEqual(len(industry.survivorsOfPreviousPeriod), 0) # No firm yet.

        industry.processResearch()
        self.assertEqual(industry.nmbResearching, 0) # No firm yet.

        industry.activateAllIncumbents()
        self.assertEqual(len(industry.activeFirms), 0) # No firm yet
        
        industry.potentialEntrants = []

        sumOfMC = 0
        sumOfExpOutput = 0

        print("Optimal tech:\n{:096b}".format(optTasks))

        for x in range(40):
            firm = Firm(x+1, industry, Technology(optTasks))
            print("Firm {:d}".format(firm.firmId))
            print("Technology before flipping task:\n{:096b}".format(firm.technology.tasks))
            for t in range(x):
                print("Flipping task {:d}".format(t+1))
                firm.technology.flipTask(t+1)

            if x == 0:
                industry.potentialEntrants.append(firm)
                firm.decideIfEnters()
            print("Technology:\n{:096b}".format(firm.technology.tasks))
            #print("Technology:\n{:096b}\nMC:{:.2f}\nExp price:{:.2f}\nExp output:{:.2f}".format(firm.technology.tasks, firm.MC, firm.expPrice, firm.expOutput))

            self.assertEqual(industry.sumOfActiveSurvivorsMC, 0)
            self.assertEqual(len(industry.activeSurvivorsOfPreviousPeriod), 0)
            self.assertEqual(firm.expPrice, (300 + firm.MC)/2)
            if firm.firmId is 1: 
                self.assertEquivalent(firm.MC, 0)
                self.assertEquivalent(firm.expPrice, 150)
                self.assertEquivalent(firm.expOutput, 600)
            
            self.assertTrue(firm.entering)
            sumOfMC += firm.MC
            sumOfExpOutput += firm.expOutput
            self.assertEqual(firm.techDistToOptimal, x)
            firm.techDistToOptimal = None
            if firm.MC == 20:
                print("Firm {:d} has MC 20".format(firm.firmId))
            self.assertEquivalent(firm.MC, x/96*100)
            self.assertEqual(firm.expPrice, 1/2*(Parameters.DemandIntercept + firm.MC))  

            self.assertEqual(firm.expPrice, Demand.calculatePrice(1, Parameters.DemandIntercept, firm.MC))
            self.assertEquivalent(firm.expOutput, industry.demand.marketSize*(1/(1+1)*(Parameters.DemandIntercept+firm.MC)-firm.MC))
            self.assertEquivalent(firm.expOutput, Demand.calculateFirmOutput(industry.demand.marketSize, 1, Parameters.DemandIntercept, firm.MC, firm.MC))
            self.assertEquivalent(firm.expOutput, Demand.calculateAggregateOutput(industry.demand.marketSize, 1, Parameters.DemandIntercept, firm.MC))
            self.assertEquivalent(firm.expProfits, (Parameters.DemandIntercept-1/industry.demand.marketSize*firm.expOutput)*firm.expOutput-Parameters.FixedProductionCost-firm.MC*firm.expOutput)
            self.assertEquivalent(firm.expProfits, firm.expOutput * (firm.expPrice-firm.MC) - Parameters.FixedProductionCost)
            self.assertEqual(firm.expProfits, firm.expWealth)
            firm.expPrice = None
            firm.MC = None
            firm.expOutput = None
            firm.expProfits = None
            firm.expWealth = None

        self.assertEquivalent(sumOfMC, 812.50000)
        self.assertEquivalent(len(industry.currentOptimalTechs), 1)
        self.assertEquivalent(sumOfExpOutput, 22375.00000)
        self.assertEquivalent(Demand.calculatePrice(40, Parameters.DemandIntercept, sumOfMC), 27.13414)
        
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

        self.assertEquivalent(len(industry.activeFirms),23)
        self.assertEquivalent(industry.sumOfActiveFirmsMC, 263.54167)
        self.assertEquivalent(industry.demand.eqPrice, 23.48090)

        # # Now we have only the incumbents that are willing to produce
        industry.updateActiveIncumbents()
        self.assertEquivalent(industry.industryOutput, 1106.07639)

        industry.activeFirms = sorted(industry.activeFirms, key=lambda firm: firm.firmId)
        for x in range(len(industry.activeFirms)):
             firm = industry.activeFirms[x]
             self.assertEquivalent(firm.MC, x/96*100)
             trueOutput = industry.demand.marketSize * ((1/(len(industry.activeFirms)+1))*(Parameters.DemandIntercept+industry.sumOfActiveFirmsMC)-firm.MC)
             self.assertEquivalent(firm.output, trueOutput)
             trueProfits = (Parameters.DemandIntercept - industry.industryOutput / industry.demand.marketSize) * firm.output - Parameters.FixedProductionCost - firm.MC * firm.output
             self.assertEquivalent(firm.profits, trueProfits)

        self.assertEqual(len(industry.inactiveFirms), 17)
        industry.updateInactiveIncumbents()
        for firm in industry.inactiveFirms:
            self.assertEqual(firm.profits, -Parameters.FixedProductionCost)
            self.assertEqual(firm.wealth, -Parameters.FixedProductionCost)

        industry.updateTotalProfits()
        self.assertEquivalent(industry.totalProfits, 9690.24131)

        industry.processExitDecisions()
        self.assertEqual(industry.nmbExitingFirms, 24) # 7 of the active firms had losses

        for firm in industry.incumbentFirms:
            self.assertTrue(not firm.exiting or firm.firmId in range(17,41)) # Firms with Id between 17 and 40 had marginal cost above profitable.

        industry.processFirmsExiting()
        for firm in industry.survivorsOfCurrentPeriod:
            self.assertTrue(firm.firmId in range(1,17)) # Only firms with Id between 1 and 16 survive.


    def assertEquivalent(self, a, b):
        self.assertTrue(Math.isEquivalent(a, b), msg='{0}, {1}'.format(a, b))

    def setUp(self):
        Logger.initialize(datetime.datetime.now(), SystemConfig.LogLevel)

    def tearDown(self):
        Random.clearAllFakes()
    