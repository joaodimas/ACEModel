from Firm import Firm, FirmStatus
from Technology import Technology
from Demand import Demand
from AggregateData import AggregateData
from Parameters import Parameters
from Logger import Logger
from Shocks import Shocks

class Industry:

    def __init__(self):
        self.lastUsedId = 0
        self.currentPeriod = 0
        self.demand = Demand(self)
        self.incumbentFirms = []
        self.survivorsOfCurrentPeriod = []
        self.activeSurvivorsOfCurrentPeriod = []
        self.sumOfActiveSurvivorsMC = 0
        self.deadFirms = []
        self.data = AggregateData(self)
        self.currentOptimalTech = Technology.generateRandomTechnology()

    # Prepare a fresh new period. Surviving firms from t-1 are still incumbents.
    def nextPeriod(self):
        self.currentPeriod += 1
        self.clearFlags()
        self.industryOutput = 0
        self.activeIncumbentFirms = []
        self.survivorsOfPreviousPeriod = self.survivorsOfCurrentPeriod
        self.activeSurvivorsOfPreviousPeriod = self.activeSurvivorsOfCurrentPeriod
        self.incumbentFirms = list(self.survivorsOfPreviousPeriod)
        self.nextPeriodIncumbentFirms = []
        self.nmbEnteringFirms = 0
        self.nmbExitingFirms = 0
        self.currentOptimalTech.magnitudeOfChange = 0
        self.refreshPoolOfPotentialEntrants()

    def processCurrentPeriod(self):
        Logger.log("----------------------------------\nPROCESSING PERIOD {:d}\n".format(self.currentPeriod))
        
        # Process all external shocks that were added to the file Shocks.py.
        Shocks.processShocks(self)

        # See which potential entrants will enter the market (i.e. become an incumbent)
        self.processFirmsEntering()

        # Activate all incumbents
        self.activateAllIncumbents()

        # Some firms might decide to not produce
        self.processShutdownDecisions()
        
        # Update the sum of MC (used to calculate demand)
        self.updateSumOfMC()

        # Now we have only the incumbents that are willing to produce
        self.updateActiveIncumbents()

        # Update weighted MC (used for posterior analysis)
        self.updateWeightedMC()

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

        # Update the sum of surviving firms' MC of previous period. 
        # This will allow potential entrants to estimate profits in the next period.
        self.updateSumOfActiveSurvivorsMC()
        self.updateAgesOfSurvivors()

        Logger.log("\nDONE PROCESSING PERIOD {:d}.".format(self.currentPeriod))    

    def processFirmsEntering(self):
        Logger.debug("Entry decisions: Processing...")
        Logger.log("Active survivors of prev. period: {:d}\n"
                   "Sum of MC of active survivors of prev. period : {:.2f}"
                   .format(len(self.activeSurvivorsOfPreviousPeriod), self.sumOfActiveSurvivorsMC))
        for firm in self.potentialEntrants:
            if firm.decideIfEnters():
                self.incumbentFirms.append(firm)
                self.nmbEnteringFirms += 1
        Logger.debug("Entry decisions: OK!")

    def processShutdownDecisions(self):
        # If there are too many active incumbents, the price will be low. In this case, some active incumbents might decide to not produce. 
        # However, as the least efficient active incumbent is deactivated, the price will increase and some inactive incumbents might change their decision.
        # Repeat the loop until the new active incumbents are the same as before (no more deactivations)
        Logger.debug("Shutdown decisions: Processing...")
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
        Logger.debug("Shutdown decisions: OK! %d loops" % loops)

    def processExitDecisions(self):
        Logger.debug("Exit decisions: Processing...")
        for firm in self.incumbentFirms:
            firm.decideIfExits()
            if(firm.exiting):
                self.nmbExitingFirms += 1
        Logger.debug("Exit decisions: OK!")

    def processFirmsExiting(self):
        Logger.debug("Firms exiting: Processing...")
        # Two things are done here:
        # (1) The list of active survivors is updated to allow potential new entrants to estimate profits in the next period.
        # (2) The list of survivors irrespective to their status is updated for data collection.
        self.activeSurvivorsOfCurrentPeriod = list(self.activeIncumbentFirms)
        self.survivorsOfCurrentPeriod = list(self.incumbentFirms)
        for firm in [firm for firm in self.incumbentFirms if firm.exiting]:
            if(firm in self.activeSurvivorsOfCurrentPeriod):
                self.activeSurvivorsOfCurrentPeriod.remove(firm)
            firm.status = FirmStatus.DEAD
            self.deadFirms.append(self)
            self.survivorsOfCurrentPeriod.remove(firm)
        Logger.debug("Firms exiting: OK!")

    def activateAllIncumbents(self):
        self.activeIncumbentFirms = self.incumbentFirms
        self.inactiveIncumbentFirms = []
        for firm in self.activeIncumbentFirms:
            firm.status = FirmStatus.ACTIVE_INCUMBENT
            firm.updateMarginalCost()
            firm.updateExpWealthAfterThisPeriod()

    def deactivateFirm(self, firm):
        firm.output = 0
        firm.status = FirmStatus.INACTIVE_INCUMBENT
        self.activeIncumbentFirms.remove(firm)
        self.inactiveIncumbentFirms.append(firm)

    def clearFlags(self):
        for firm in self.incumbentFirms:
            firm.entering = False
            firm.exiting = False
            firm.deactivating = False

    def getActiveIncumbents(self):
        return [firm for firm in self.incumbentFirms if firm.status == FirmStatus.ACTIVE_INCUMBENT]

    def updateSumOfMC(self): 
        self.currentActiveSumOfMC = 0
        for firm in self.activeIncumbentFirms:
            self.currentActiveSumOfMC += firm.MC

        Logger.log("Current active incumbents: {:d}\n"
                   "Sum of MC of current active incumbents : {:.2f}"
                   .format(len(self.activeIncumbentFirms), self.currentActiveSumOfMC))

    def updateWeightedMC(self): 
        self.weightedMC = 0
        if self.industryOutput != 0:
            for firm in self.activeIncumbentFirms:
                self.weightedMC += firm.MC * firm.output / self.industryOutput
    
    def updateSumOfActiveSurvivorsMC(self):
        self.sumOfActiveSurvivorsMC = 0
        for firm in self.activeSurvivorsOfCurrentPeriod:
            self.sumOfActiveSurvivorsMC += firm.MC

    def updateAgesOfSurvivors(self):
        for firm in self.survivorsOfCurrentPeriod:
            firm.age += 1

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

    def updateActiveIncumbents(self):
        Logger.debug("Updating %d active firms: Processing..." % len(self.activeIncumbentFirms))
        for firm in self.activeIncumbentFirms:
            firm.updateOutput() # Calculate new equilibrium output after all inactive firms were taken out of the equation
            firm.updateProfits()
            firm.updateWealth()
            self.industryOutput += firm.output
        Logger.debug("Updating %d active firms: OK!" % len(self.activeIncumbentFirms))

    def updateInactiveIncumbents(self):
        Logger.debug("Updating %d inactive firms: Processing..." % len(self.inactiveIncumbentFirms))
        for firm in self.inactiveIncumbentFirms:
            firm.updateProfits()
            firm.updateWealth()
        Logger.debug("Updating %d inactive firms: OK!" % len(self.inactiveIncumbentFirms))  

    def refreshPoolOfPotentialEntrants(self):
        self.potentialEntrants = []
        for x in range(Parameters.NumberOfPotentialEntrants):
            self.potentialEntrants.append(Firm(self.newFirmId(), self, Technology.generateRandomTechnology()))

    def newFirmId(self):
        self.lastUsedId += 1
        return self.lastUsedId
