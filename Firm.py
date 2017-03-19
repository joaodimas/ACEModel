from Parameters import Parameters
from enum import Enum
from Logger import Logger


class Firm :
    def __init__(self, firmId, industry, technology):
        self.firmId = firmId
        self.industry = industry
        self.technology = technology
        self.status = FirmStatus.POTENTIAL_ENTRANT
        self.wealth = Parameters.StartupWealth
        self.prevWealth = 0
        self.profits = 0
        self.expProfits = 0
        self.expPrice = 0
        self.MC = 0
        self.prevMC = 0
        self.output = 0
        self.entering = False
        self.exiting = False
        self.age = 0

    def getDescription(self):
        return "id: " + str(self.firmId)

    def updateMarginalCost(self):
        self.prevMC = self.MC
        self.techDistToOptimal = self.technology.calculateHammingDistance(self.industry.currentOptimalTech)
        self.MC = 100 * self.techDistToOptimal / Parameters.NumberOfTasks

    def getTotalCost(self, quantity):
        return Parameters.FixedCost + quantity * self.MC

    # Derived from the FOC
    def updateOutput(self):
        self.output = self.industry.demand.marketSize * (self.industry.demand.eqPrice - self.MC)

    # Derived from the FOC
    def updateProfits(self):
        self.profits = self.output ** 2 / self.industry.demand.marketSize - Parameters.FixedCost
        return self.profits

    # Derived from the FOC
    def updateExpWealthAfterThisPeriod(self):
        self.expPrice = self.industry.demand.getExpEqPrice(self)
        self.expOutput = self.industry.demand.marketSize * (self.expPrice - self.MC)
        if(self.expOutput < 0):
            self.expOutput = 0

        self.expProfits = self.expOutput ** 2 / self.industry.demand.marketSize - Parameters.FixedCost
        self.expWealth = self.wealth + self.expProfits

    def updateWealth(self):
        self.prevWealth = self.wealth
        self.wealth += self.profits

    def decideIfEnters(self):
        self.updateMarginalCost()
        self.updateExpWealthAfterThisPeriod()
        
        if(self.status == FirmStatus.POTENTIAL_ENTRANT and self.expWealth > Parameters.MinimumWealthForSurvival):
            self.entering = True
            Logger.trace("Firm {:d} decided to ENTER. Price: {:.2f}; MC: {:.2f}; Exp. Output: {:.2f}; Exp. Profits: {:.2f}; Current wealth: {:.2f}; Exp. Wealth: {:.2f}.".format(self.firmId, self.expPrice, self.MC, self.expOutput, self.expProfits, self.wealth, self.expWealth))
  
        return self.entering

    def decideIfExits(self):
        if(self.wealth < Parameters.MinimumWealthForSurvival):
            self.exiting = True
            Logger.trace("Firm {:d} decided to EXIT. Price: {:.2f}; MC: {:.2f}; Exp. Output: {:.2f}; Output: {:.2f}; Exp. Profits: {:.2f}; Profits: {:.2f}; Wealth: {:.2f}.".format(self.firmId, self.expPrice, self.MC, self.expOutput, self.output, self.expProfits, self.profits, self.wealth))
        return self.exiting

    def decideIfDeactivates(self):
        self.updateOutput()
        if(self.output <= 0): # Yes. This firm doesn't want to produce. It will be deactivated.
            self.deactivating = True
            Logger.trace("Firm {:d} decided to DEACTIVATE. Price: {:.2f}; MC: {:.2f}; Exp. Output: {:.2f}; Output: {:.2f}; Exp. Profits: {:.2f}; Profits: {:.2f}; Wealth: {:.2f}.".format(self.firmId, self.expPrice, self.MC, self.expOutput, self.output, self.expProfits, self.profits, self.wealth))
        else:
            self.deactivating = False
        return self.deactivating


class FirmStatus(Enum):
    POTENTIAL_ENTRANT = 1
    INACTIVE_INCUMBENT = 2
    ACTIVE_INCUMBENT = 3
    DEAD = 4

