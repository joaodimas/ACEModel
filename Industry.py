import logging
from Firm import Firm, FirmStatus
from Technology import Technology
from Demand import Demand
from AggregateData import AggregateData
from Parameters import Parameters
from Shocks import Shocks

class Industry:

    # This is the main method to understand what happends in each period.
    def processPeriod(self):
        # WARNING: DO NOT CHANGE THE ORDER OF STEPS. ONE DEPENDS ON THE OTHER.

        # Prepare state variables for a new period
        self.nextPeriod()

        self.logger.debug("----------------------------------")
        self.logger.info("PROCESSING PERIOD {:d}".format(self.currentPeriod))
        
        # Process all external shocks that were added to the file Shocks.py.
        Shocks.processShocks(self)

        # Each survivor will decide by doing or not R&D
        self.processResearch()

        # See which potential entrants will enter the market (i.e. become an incumbent)
        self.processFirmsEntering()

        # Activate all incumbents
        self.activateAllIncumbents()

        # Some firms might decide to not produce
        self.processShutdownDecisions()

        # Now we have only the incumbents that are willing to produce
        self.updateActiveIncumbents()

        # Update weighted MC (used for posterior analysis)
        self.updateWeightedMC()

        # Update the average proximity to optimal technology
        self.updateAvgProximityToOptTech()

        self.updateMarketShares()

        # Calculate Herfindahl-Hirschmann Index
        self.updateHIndex()

        # Calculate the degree of technological diversity
        self.updateDegreeOfTechDiv()

        # Calculate the Gini coefficient with regard to the market share
        self.updateGiniCoefficient()    

        # Calculate Price-Cost margin
        self.updatePCM()

        # Calculate Consumer Surplus
        self.updateCS()

        # Calculate total profits
        self.updateTotalProfits()

        # Calculate Total Surplus
        self.updateTS()

        # Update wealth of inactive firms (they'll lose the fixed cost)
        self.updateInactiveIncumbents()
        
        # Incumbent firms decide if exit (die) or not
        self.processExitDecisions()

        # Update average age and oldest firm
        self.updateAgeStats()

        # Store data
        self.data.storeCurrentPeriod()

        # Process firms exiting
        self.processFirmsExiting()

        # Update the sum of surviving firms' MC of previous period. This will allow potential entrants to estimate profits in the next period.
        self.updateSumOfActiveSurvivorsMC()

        # Increment the ages of each survivor
        self.updateAgesOfSurvivors()

    # Prepare a fresh new period. Surviving firms from t-1 are still incumbents.
    def nextPeriod(self):
        self.currentPeriod += 1
        self.industryOutput = 0
        self.activeIncumbentFirms = []
        self.survivorsOfPreviousPeriod = self.survivorsOfCurrentPeriod
        self.activeSurvivorsOfPreviousPeriod = self.activeSurvivorsOfCurrentPeriod
        self.incumbentFirms = list(self.survivorsOfPreviousPeriod)
        self.profitableFirmsPrevPeriod = [firm for firm in self.activeSurvivorsOfPreviousPeriod if firm.profits > 0]
        self.nextPeriodIncumbentFirms = []
        self.nmbEnteringFirms = 0
        self.nmbExitingFirms = 0
        self.nmbProfitableFirms = 0
        self.currentOptimalTech.magnitudeOfChange = 0
        self.clearFirmsStatus()
        self.refreshPoolOfPotentialEntrants()

    def processResearch(self):
        self.totalInvestmentInResearch = 0
        self.nmbResearching = 0
        self.nmbInnovating = 0
        self.nmbImitating = 0
        for firm in self.survivorsOfPreviousPeriod:
            result = firm.processResearch()
            self.totalInvestmentInResearch += result[0]
            if(result[1]):
                self.nmbResearching += 1
            if(result[2]):
                self.nmbInnovating += 1
            if(result[3]):
                self.nmbImitating += 1


    def processFirmsEntering(self):
        self.logger.trace("Entry decisions: Processing...")
        self.logger.trace("Activem survivors of prev. period: {:d}\n"
                   "Sum of MC of active survivors of prev. period : {:.2f}"
                   .format(len(self.activeSurvivorsOfPreviousPeriod), self.sumOfActiveSurvivorsMC))
        for firm in self.potentialEntrants:
            if firm.decideIfEnters():
                self.incumbentFirms.append(firm)
                self.nmbEnteringFirms += 1
        self.entryRate = self.nmbEnteringFirms / len(self.incumbentFirms) if len(self.incumbentFirms) > 0 else 0
        self.logger.trace("Entry decisions: OK!")

    def activateAllIncumbents(self):
        self.activeIncumbentFirms = self.incumbentFirms
        self.inactiveIncumbentFirms = []
        for firm in self.activeIncumbentFirms:
            firm.status = FirmStatus.ACTIVE_INCUMBENT
            firm.updateMarginalCost()
            firm.updateExpWealthAfterThisPeriod()

    def processShutdownDecisions(self):
        # If there are too many active incumbents, the price will be low. In this case, some active incumbents might decide to not produce. 
        # Repeat the loop until the new active incumbents are the same as before (no more deactivations)
        self.logger.trace("Shutdown decisions: Processing...")
        loops = 0
        prevActiveIncumbents = []
        # Sort from the least to the most efficient firm.
        self.activeIncumbentFirms = sorted(self.activeIncumbentFirms, key=lambda firm: firm.MC, reverse= True)
        # Check least efficient firms and process deactivations.
        while len(prevActiveIncumbents) != len(self.activeIncumbentFirms):
            prevActiveIncumbents = list(self.activeIncumbentFirms)

            # The actual sum of MC is necessary to find the equilibrium price. 
            # Therefore, it needs to be recalculated after each deactivation.
            self.updateSumOfMC()

            # Calculate the equilibrium price. This is obtained from the FOC for each firm and 
            # depends only on: (1) the number of active incumbents and (2) the sum of the marginal costs of active incumbents.
            self.demand.updateEqPrice() 

            # Get the least efficient firm and see if it leaves the market.
            if(len(self.activeIncumbentFirms) > 0):
                leastEfficient = self.activeIncumbentFirms[0]
                if leastEfficient.decideIfDeactivates():
                    self.deactivateFirm(leastEfficient)

            loops += 1
        self.logger.trace("Shutdown decisions: OK! {:d} firms deactivated.".format(loops - 1))

    def updateSumOfMC(self): 
        self.currentActiveSumOfMC = 0
        for firm in self.activeIncumbentFirms:
            self.currentActiveSumOfMC += firm.MC

        self.logger.trace("Current active incumbents: {:d}\n"
                   "Sum of MC of current active incumbents : {:.2f}"
                   .format(len(self.activeIncumbentFirms), self.currentActiveSumOfMC))

    def updateActiveIncumbents(self):
        self.logger.trace("Updating %d active firms: Processing..." % len(self.activeIncumbentFirms))
        for firm in self.activeIncumbentFirms:
            firm.updateOutput() # Calculate new equilibrium output after all inactive firms were taken out of the equation
            firm.updateProfits()
            firm.updateWealth()
            self.industryOutput += firm.output
            if(firm.profits > 0):
                self.nmbProfitableFirms += 1
        self.logger.trace("Updating %d active firms: OK!" % len(self.activeIncumbentFirms))

    def updateWeightedMC(self): 
        self.weightedMC = 0
        if self.industryOutput != 0:
            for firm in self.activeIncumbentFirms:
                self.weightedMC += firm.MC * firm.output / self.industryOutput

    def updateAvgProximityToOptTech(self):
        self.averageProximityToOptimalTech = 1 - (self.currentActiveSumOfMC / len(self.activeIncumbentFirms) / 100) if len(self.activeIncumbentFirms) != 0 else 0

    def updateMarketShares(self):
        for firm in self.incumbentFirms:
            firm.marketShare = firm.output / self.industryOutput

    # Herfindahl-Hirschmann Index
    def updateHIndex(self):
        self.HIndex = 0
        for firm in self.activeIncumbentFirms:
            self.HIndex += (firm.marketShare * 100) ** 2 

    def updateDegreeOfTechDiv(self):
        sumOfHammingDist = 0
        for firmA in self.incumbentFirms:
            for firmB in [firm for firm in self.incumbentFirms if firm.firmId != firmA.firmId]:
                sumOfHammingDist += firmA.technology.calculateHammingDistance(firmB.technology)

        self.degreeOfTechDiv = (2 / (Parameters.NumberOfTasks * len(self.incumbentFirms) * (len(self.incumbentFirms) - 1))) * sumOfHammingDist

    def updateGiniCoefficient(self):
        a = 0
        nmbIncumbents = len(self.incumbentFirms)
        for i, firm in enumerate(self.incumbentFirms):
            a += (i + 1) * firm.output / self.industryOutput

        self.gini = 2 * a / nmbIncumbents - (nmbIncumbents + 1) / nmbIncumbents 

    # Price-margin cost
    def updatePCM(self):
        self.PCM = 0
        for firm in self.incumbentFirms:
            self.PCM += firm.output / self.industryOutput * (self.demand.eqPrice - firm.MC) / self.demand.eqPrice

    # Consumer Surplus
    def updateCS(self):
        self.CS = (Parameters.DemandIntercept - self.demand.eqPrice) * self.industryOutput / 2

    def updateTotalProfits(self):
        self.totalProfits = 0
        for firm in self.incumbentFirms:
            self.totalProfits += firm.profits

    # Total Surplus
    def updateTS(self):
        self.TS = self.CS + self.totalProfits                                  

    def updateInactiveIncumbents(self):
        self.logger.trace("Updating %d inactive firms: Processing..." % len(self.inactiveIncumbentFirms))
        for firm in self.inactiveIncumbentFirms:
            firm.updateProfits()
            firm.updateWealth()
        self.logger.trace("Updating %d inactive firms: OK!" % len(self.inactiveIncumbentFirms))  

    def processExitDecisions(self):
        self.logger.trace("Exit decisions: Processing...")
        for firm in self.incumbentFirms:
            firm.decideIfExits()
            if(firm.exiting):
                self.nmbExitingFirms += 1
        self.exitRate = self.nmbExitingFirms / len(self.incumbentFirms) if len(self.incumbentFirms) > 0 else 0
        self.logger.trace("Exit decisions: OK!")

    def updateAgeStats(self):
        self.oldestAge = 0
        self.youngestAge = Parameters.NumberOfPeriods
        sumOfAges = 0
        for firm in self.incumbentFirms:
            sumOfAges += firm.age
            if(firm.age > self.oldestAge):
                self.oldestAge = firm.age
            if(firm.age < self.youngestAge):
                self.youngestAge = firm.age
        self.averageAge = sumOfAges / len(self.incumbentFirms) if len(self.incumbentFirms) > 0 else 0

    def processFirmsExiting(self):
        self.logger.trace("Firms exiting: Processing...")
        # Two things are done here:
        # (1) The list of active survivors is updated to allow potential new entrants to estimate profits in the next period.
        # (2) The list of survivors irrespective to their status is updated for data collection.
        self.activeSurvivorsOfCurrentPeriod = list(self.activeIncumbentFirms)
        self.survivorsOfCurrentPeriod = list(self.incumbentFirms)
        exitingFirms = [firm for firm in self.incumbentFirms if firm.exiting]
        for firm in exitingFirms:
            if(firm in self.activeSurvivorsOfCurrentPeriod):
                self.activeSurvivorsOfCurrentPeriod.remove(firm)
            firm.status = FirmStatus.DEAD
            self.survivorsOfCurrentPeriod.remove(firm)
        self.logger.trace("Firms exiting: OK! {:d} left the market.".format(len(exitingFirms)))

    def updateSumOfActiveSurvivorsMC(self):
        self.sumOfActiveSurvivorsMC = 0
        for firm in self.activeSurvivorsOfCurrentPeriod:
            self.sumOfActiveSurvivorsMC += firm.MC

    def updateAgesOfSurvivors(self):
        for firm in self.survivorsOfCurrentPeriod:
            firm.age += 1

    def deactivateFirm(self, firm):
        firm.output = 0
        firm.status = FirmStatus.INACTIVE_INCUMBENT
        self.activeIncumbentFirms.remove(firm)
        self.inactiveIncumbentFirms.append(firm)

    def clearFirmsStatus(self):
        for firm in self.incumbentFirms:
            firm.clearStatus()

    def getActiveIncumbents(self):
        return [firm for firm in self.incumbentFirms if firm.status == FirmStatus.ACTIVE_INCUMBENT]

    def refreshPoolOfPotentialEntrants(self):
        self.potentialEntrants = []
        for x in range(Parameters.NumberOfPotentialEntrants):
            self.potentialEntrants.append(Firm(self.newFirmId(), self, Technology.generateRandomTechnology()))

    def newFirmId(self):
        self.lastUsedId += 1
        return self.lastUsedId
 
    def __init__(self):
        self.lastUsedId = 0
        self.currentPeriod = 0
        self.demand = Demand(self)
        self.survivorsOfCurrentPeriod = []
        self.activeSurvivorsOfCurrentPeriod = []
        self.sumOfActiveSurvivorsMC = 0
        self.data = AggregateData(self)
        self.currentOptimalTech = Technology.generateRandomTechnology()
        self.logger = logging.getLogger("ACEModel")
