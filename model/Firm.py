from enum import Enum
from model.util.Random import Random
from model.util.Logger import Logger
from model.Parameters import Parameters
from model.Technology import Technology


class Firm :
    def __init__(self, firmId, industry, technology):
        self.firmId = firmId
        self.industry = industry
        self.technology = technology
        technology.firmId = firmId
        self.status = FirmStatus.POTENTIAL_ENTRANT
        self.wealth = Parameters.StartupWealth
        self.prevWealth = 0
        self.profits = 0
        self.expProfits = 0
        self.expPrice = 0
        self.MC = 0
        self.output = 0
        self.entering = False
        self.exiting = False
        self.age = 0
        self.investmentInResearch = 0
        self.attractionForResearch = Parameters.InitialAttractionForResearch
        self.attractionForNoResearch = Parameters.InitialAttractionForNoResearch
        self.attractionForInnovation = Parameters.InitialAttractionForInnovation
        self.attractionForImitation = Parameters.InitialAttractionForImitation

    def getDescription(self):
        return "id: " + str(self.firmId)

    def updateMarginalCost(self):
        self.techDistToOptimal = self.technology.calculateHammingDistance(self.industry.currentOptimalTech)
        self.MC = 100 * self.techDistToOptimal / Parameters.NumberOfTasks

    def getTotalCost(self, quantity):
        return Parameters.FixedProductionCost + quantity * self.MC

    # Derived from the FOC
    def updateOutput(self):
        self.output = self.industry.demand.marketSize * (self.industry.demand.eqPrice - self.MC)

    # Derived from the FOC
    def updateProfits(self):
        self.profits = self.output * (self.industry.demand.eqPrice - self.MC) - Parameters.FixedProductionCost
        return self.profits

    # Derived from the FOC
    def updateExpWealthAfterThisPeriod(self):
        self.expPrice = self.industry.demand.getExpEqPrice(self)
        Logger.trace("[FIRM {:d}] Expects an equilibrium price of {:.2f}. Active survivors of previous period: {:d}; Sum of MC of active survivores {:.2f}; MC of potential entrant: {:.2f}.", (self.firmId, self.expPrice, len(self.industry.activeSurvivorsOfPreviousPeriod), self.industry.sumOfActiveSurvivorsMC, self.MC), industry=self.industry)
        self.expOutput = self.industry.demand.marketSize * (self.expPrice - self.MC)
        if(self.expOutput < 0):
            self.expOutput = 0

        self.expProfits = self.expOutput * (self.expPrice - self.MC) - Parameters.FixedProductionCost
        self.expWealth = self.wealth + self.expProfits

    def updateWealth(self):
        self.prevWealth = self.wealth
        self.wealth += self.profits

    def decideIfEnters(self):
        self.updateMarginalCost()
        self.updateExpWealthAfterThisPeriod()
        
        if(self.expWealth > Parameters.ThresholdNetWealthForSurvival):
            self.entering = True
            self.status = FirmStatus.ACTIVE_INCUMBENT
            Logger.trace("[FIRM {:d}] Potential entrant decided to ENTER. Expected price: {:.2f}; MC: {:.2f}; Exp. Output: {:.2f}; Exp. Profits: {:.2f}; Current wealth: {:.2f}; Exp. Wealth: {:.2f}.", (self.firmId, self.expPrice, self.MC, self.expOutput, self.expProfits, self.wealth, self.expWealth), industry=self.industry)
        else:
            Logger.trace("[FIRM {:d}] Potential entrant decided to NOT ENTER. Expected price: {:.2f}; MC: {:.2f}; Exp. Output: {:.2f}; Exp. Profits: {:.2f}; Current wealth: {:.2f}; Exp. Wealth: {:.2f}.", (self.firmId, self.expPrice, self.MC, self.expOutput, self.expProfits, self.wealth, self.expWealth), industry=self.industry)
  
        return self.entering

    def decideIfExits(self):
        if(self.wealth < Parameters.ThresholdNetWealthForSurvival):
            self.exiting = True
            Logger.trace("[FIRM {:d}] Decided to EXIT. Price: {:.2f}; Exp. Price: {:.2f}; MC: {:.2f}; Exp. Output: {:.2f}; Output: {:.2f}; Exp. Profits: {:.2f}; Profits: {:.2f}; Wealth: {:.2f}.", (self.firmId, self.industry.demand.eqPrice, self.expPrice, self.MC, self.expOutput, self.output, self.expProfits, self.profits, self.wealth), industry=self.industry)
        return self.exiting

    def decideIfDeactivates(self):
        self.updateOutput()
        if(self.output <= 0): # Yes. This firm doesn't want to produce. It will be deactivated.
            self.deactivating = True
            Logger.trace("[FIRM {:d}] Decided to DEACTIVATE. Price: {:.2f}; MC: {:.2f}; Exp. Price: {:.2f}; Exp. Output: {:.2f}; Exp. Profits: {:.2f}; Wealth: {:.2f}.", (self.firmId, self.industry.demand.eqPrice, self.MC, self.expPrice, self.expOutput, self.expProfits, self.wealth), industry=self.industry)
        else:
            self.deactivating = False
            Logger.trace("[FIRM {:d}] Decided to NOT DEACTIVATE. Price: {:.2f}; MC: {:.2f}; Exp. Price: {:.2f}; Exp. Output: {:.2f}; Exp. Profits: {:.2f}; Wealth: {:.2f}.", (self.firmId, self.industry.demand.eqPrice, self.MC, self.expPrice, self.expOutput, self.expProfits, self.wealth), industry=self.industry)
        return self.deactivating

    def processResearch(self):
        Logger.trace("[FIRM {:d}] Deciding about R&D. Wealth: {:.2f}; Attraction to R&D: {:.2f}; Attraction to Not-R&D: {:.2f}; Attraction to Innovation: {:.2f}; Attraction to Imitation: {:.2f}.", (self.firmId, self.wealth, self.attractionForResearch, self.attractionForNoResearch, self.attractionForInnovation, self.attractionForImitation), industry=self.industry)
        self.updateMarginalCost() # Update marginal cost after a possible technological shock.
        # Only consider R&D if we have enough wealth
        if self.wealth >= max(Parameters.FixedCostOfImitation, Parameters.FixedCostOfInnovation):
            # Decide if it will do R&D
            if(Random.random() < self.getProbOfResearch()):
                # Decide if it will innovate
                if(Random.random() < self.getProbOfInnovation()):
                    Logger.trace("[FIRM {:d}] Decided to INNOVATE. Prob of R&D: {:.2f}; Prob of Innovation: {:.2f}.", (self.firmId, self.getProbOfResearch(), self.getProbOfInnovation()), industry=self.industry)
                    self.investmentInResearch = self.processInnovation()
                    self.industry.nmbInnovating += 1
                    self.industry.totalInvestmentInInnovation += self.investmentInResearch
                # Instead of innovating, we will imitate
                else:
                    Logger.trace("[FIRM {:d}] Decided to IMITATE. Prob of R&D: {:.2f}; Prob of Imitation: {:.2f}.", (self.firmId, self.getProbOfResearch(), 1 - self.getProbOfInnovation()), industry=self.industry)
                    self.investmentInResearch = self.processImitation()
                    self.industry.nmbImitating += 1
                    self.industry.totalInvestmentInImitation += self.investmentInResearch

                self.wealth -= self.investmentInResearch
                self.industry.totalInvestmentInResearch += self.investmentInResearch
                self.industry.nmbResearching += 1
                Logger.trace("[FIRM {:d}] Completed R&D. Wealth: {:.2f}; Attraction to R&D: {:.2f}; Attraction to Not-R&D: {:.2f}; Attraction to Innovation: {:.2f}; Attraction to Imitation: {:.2f}.", (self.firmId, self.wealth, self.attractionForResearch, self.attractionForNoResearch, self.attractionForInnovation, self.attractionForImitation), industry=self.industry)

            # No R&D in this period
            else:
                Logger.trace("[FIRM {:d}] Decided to NOT pursue R&D. Prob of R&D: {:.2f}.", (self.firmId, self.getProbOfResearch()), industry=self.industry)                
        # We're too poor to do R&D
        else:
            Logger.trace("[FIRM {:d}] No wealth to pursue R&D. Wealth: {:.2f}", (self.firmId, self.wealth), industry=self.industry)

    def processInnovation(self):
        oldTechnology = Technology(self.technology.tasks)
        oldMC = self.MC
  
        self.technology.flipRandomTask()
        Logger.trace("[FIRM {:d}] Modified task {:d}", (self.firmId, self.technology.taskChanged), industry=self.industry)
        Logger.trace("[FIRM {:d}] Before: {:0{:d}b}", (self.firmId, oldTechnology.tasks, Parameters.NumberOfTasks), industry=self.industry)
        Logger.trace("[FIRM {:d}] After: {:0{:d}b}", (self.firmId, self.technology.tasks, Parameters.NumberOfTasks), industry=self.industry)
        
        # If new tehnology is more efficient, adopt it.
        self.updateMarginalCost()
        if(self.MC < oldMC):
            Logger.trace("[FIRM {:d}] Lowered marginal cost through INNOVATION. Previous MC: {:.2f}; New MC: {:.2f}", (self.firmId, oldMC, self.MC), industry=self.industry)
            self.attractionForResearch += 1
            self.attractionForInnovation += 1
        else:
            Logger.trace("[FIRM {:d}] Failed to reduce its marginal cost through INNOVATION. Previous MC: {:.2f}, Experimental MC: {:.2f}", (self.firmId, oldMC, self.MC), industry=self.industry)
            self.technology = oldTechnology
            self.updateMarginalCost()
            self.attractionForNoResearch += 1
            self.attractionForImitation += 1

        return Parameters.FixedCostOfInnovation

    def processImitation(self):
        oldTechnology = Technology(self.technology.tasks)
        oldMC = self.MC
        firmToImitate = self.selectFirmToImitate()
        
        if(firmToImitate != None):
            self.imitate(firmToImitate)
            self.updateMarginalCost()
        else:
            Logger.trace("[FIRM {:d}] Found NO PROFITABLE FIRM to immitate.", self.firmId, industry=self.industry)

        # If new tehnology is more efficient, adopt it.
        if(self.MC < oldMC):
            Logger.trace("[FIRM {:d}] Lowered marginal cost through IMMITATION. Previous MC: {:.2f}; New MC: {:.2f}", (self.firmId, oldMC, self.MC), industry=self.industry)
            self.attractionForResearch += 1
            self.attractionForImitation += 1
        else:
            Logger.trace("[FIRM {:d}] Failed to reduce its marginal cost through IMMITATION. Previous MC: {:.2f}, Experimental MC: {:.2f}", (self.firmId, oldMC, self.MC), industry=self.industry)
            self.technology = oldTechnology
            self.updateMarginalCost()
            self.attractionForNoResearch += 1
            self.attractionForInnovation += 1

        return Parameters.FixedCostOfImitation

    def imitate(self, otherFirm):
        Logger.trace("[FIRM {:d}] Current technology: {:0{:d}b}", (self.firmId, self.technology.tasks, Parameters.NumberOfTasks), industry=self.industry)
        Logger.trace("[FIRM {:d}] Technology to imitate: {:0{:d}b}", (self.firmId, otherFirm.prevTechnology.tasks, Parameters.NumberOfTasks), industry=self.industry)
        self.technology.copyOneRandomTask(otherFirm.prevTechnology)
        Logger.trace("[FIRM {:d}] Task copied: {:d}", (self.firmId, self.technology.taskChanged), industry=self.industry)
        Logger.trace("[FIRM {:d}] New technology: {:0{:d}b}", (self.firmId, self.technology.tasks, Parameters.NumberOfTasks), industry=self.industry) 
   

    # More profitable competitors have a higher likelihood of being observed by this firm.
    # This function uses the Roulette Wheel Algorithm (more info: http://geneticalgorithms.ai-depot.com/Tutorial/Overview.html)
    def selectFirmToImitate(self):
        Logger.trace("[FIRM {:d}] Selecting a firm to imitage...", (self.firmId), industry=self.industry)
        
        # The point in the CDF from which we select a firm to be observed
        pointInCDF = Random.random()
        
        return self.selectCompetitorFromRouletteWheel(pointInCDF)

    def selectCompetitorFromRouletteWheel(self, pointInCDF):
        Logger.trace("[FIRM {:d}] Point in CDF: {:.3f}", (self.firmId, pointInCDF), industry=self.industry)

        otherFirms = [firm for firm in self.industry.profitableFirmsPrevPeriod if firm.firmId != self.firmId]

        # Really bad previous period. No profitable firms.
        if(len(otherFirms) == 0):
            return None

        # Sum the profits 
        sumOfProfits = 0.0
        for firm in otherFirms:
            sumOfProfits += firm.profits
        Logger.trace("[FIRM {:d}] Sum of profits of competitors: {:.2f}", (self.firmId, sumOfProfits), industry=self.industry)

        # Since we already have a random selection from 0 to 1, 
        # the firm for which the range of probability in the CDF contains the selection will be the observed one.
        # Firms with higher share of profits will occupy a broader range in the CDF, which will increase its likelihood of being observed.
        cdf = 0.0
        for firm in otherFirms:
            probOfBeingObserved = firm.profits / sumOfProfits
            Logger.trace("[FIRM {:d}] Competitor {:d} has a {:.2%} probability of being observed. Its range in the CDF is from {:.3f} to {:.3f}", (self.firmId, firm.firmId, probOfBeingObserved, cdf, cdf + probOfBeingObserved), industry=self.industry)
            if(cdf < pointInCDF <= cdf + probOfBeingObserved):
                Logger.trace("[FIRM {:d}] Competitor {:d} was observed. Point in CDF: {:.3f}", (self.firmId, firm.firmId, pointInCDF), industry=self.industry)
                return firm
            cdf = cdf + probOfBeingObserved
            assert 0 <= cdf <= 1

    # Calculate the probability of engaging in R&D (innovation OR imitation) according to the attraction values.
    def getProbOfResearch(self):
        return self.attractionForResearch / (self.attractionForResearch + self.attractionForNoResearch)

    # Calculate the probability of engaging in Innovation instead of Imitation according to the attraction values.
    def getProbOfInnovation(self):
        return self.attractionForInnovation / (self.attractionForInnovation + self.attractionForImitation)

    def clearStatus(self):
        self.entering = False
        self.exiting = False
        self.deactivating = False

    def __str__(self):
        return str(self.firmId)

class FirmStatus(Enum):
    POTENTIAL_ENTRANT = 1
    INACTIVE_INCUMBENT = 2
    ACTIVE_INCUMBENT = 3
    DEAD = 4

