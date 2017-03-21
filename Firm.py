import logging, random
from Parameters import Parameters
from Technology import Technology
from enum import Enum


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
        self.investmentInResearch = 0
        self.attractionForResearch = Parameters.InitialAttractionForResearch
        self.attractionForNoResearch = Parameters.InitialAttractionForNoResearch
        self.attractionForInnovation = Parameters.InitialAttractionForInnovation
        self.attractionForImitation = Parameters.InitialAttractionForImitation
        self.logger = logging.getLogger("ACEModel")

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
            self.logger.trace("Firm {:d} decided to ENTER. Expected price: {:.2f}; MC: {:.2f}; Exp. Output: {:.2f}; Exp. Profits: {:.2f}; Current wealth: {:.2f}; Exp. Wealth: {:.2f}.".format(self.firmId, self.expPrice, self.MC, self.expOutput, self.expProfits, self.wealth, self.expWealth))
  
        return self.entering

    def decideIfExits(self):
        if(self.wealth < Parameters.MinimumWealthForSurvival):
            self.exiting = True
            self.logger.trace("Firm {:d} decided to EXIT. Price: {:.2f}; Exp. Price: {:.2f}; MC: {:.2f}; Exp. Output: {:.2f}; Output: {:.2f}; Exp. Profits: {:.2f}; Profits: {:.2f}; Wealth: {:.2f}.".format(self.firmId, self.industry.demand.eqPrice, self.expPrice, self.MC, self.expOutput, self.output, self.expProfits, self.profits, self.wealth))
        return self.exiting

    def decideIfDeactivates(self):
        self.updateOutput()
        if(self.output <= 0): # Yes. This firm doesn't want to produce. It will be deactivated.
            self.deactivating = True
            self.logger.trace("Firm {:d} decided to DEACTIVATE. Price: {:.2f}; MC: {:.2f}; Exp. Price: {:.2f}; Exp. Output: {:.2f}; Exp. Profits: {:.2f}; Wealth: {:.2f}.".format(self.firmId, self.industry.demand.eqPrice, self.MC, self.expPrice, self.expOutput, self.expProfits, self.wealth))
        else:
            self.deactivating = False
        return self.deactivating

    def processResearch(self):
        self.logger.trace("Firm {:d} will make a decision regarding R&D. Wealth: {:.2f}; Attraction to R&D: {:.2f}; Attraction to Not-R&D: {:.2f}; Attraction to Innovation: {:.2f}; Attraction to Imitation: {:.2f}.".format(self.firmId, self.wealth, self.attractionForResearch, self.attractionForNoResearch, self.attractionForInnovation, self.attractionForImitation))
        investmentInResearch = 0
        researching = False
        innovating = False
        imitating = False
        # Only consider R&D if we have enough wealth
        if self.wealth >= max(Parameters.ImitationCost, Parameters.InnovationCost):
            # Decide if it will do R&D
            if(random.random() < self.getProbOfResearch()):
                # Decide if it will innovate
                if(random.random() < self.getProbOfInnovation()):
                    self.logger.trace("Firm {:d} decided to INNOVATE. Prob of R&D: {:.2f}; Prob of Innovation: {:.2f}.".format(self.firmId, self.getProbOfResearch(), self.getProbOfInnovation()))
                    investmentInResearch = self.processInnovation()
                    innovating = True
                # Instead of innovating, we will imitate
                else:
                    self.logger.trace("Firm {:d} decided to IMITATE. Prob of R&D: {:.2f}; Prob of Imitation: {:.2f}.".format(self.firmId, self.getProbOfResearch(), 1 - self.getProbOfInnovation()))
                    investmentInResearch = self.processImitation()
                    imitating = True

                self.wealth -= investmentInResearch
                researching = True
                self.logger.trace("Firm {:d} completed R&D. Wealth: {:.2f}; Attraction to R&D: {:.2f}; Attraction to Not-R&D: {:.2f}; Attraction to Innovation: {:.2f}; Attraction to Imitation: {:.2f}.".format(self.firmId, self.wealth, self.attractionForResearch, self.attractionForNoResearch, self.attractionForInnovation, self.attractionForImitation))

            # No R&D in this period
            else:
                self.logger.trace("Firm {:d} decided to NOT pursue R&D. Prob of R&D: {:.2f}.".format(self.firmId, self.getProbOfResearch()))                
        # We're too poor to do R&D
        else:
            self.logger.trace("Firm {:d} has no wealth to pursue R&D. Wealth: {:.2f}".format(self.firmId, self.wealth))

        self.investmentInResearch = investmentInResearch
        return investmentInResearch, researching, innovating, imitating

    def processInnovation(self):
        oldTechnology = Technology(self.technology.tasks)
        oldMC = self.MC
        self.technology.flipRandomTask()
        self.updateMarginalCost()

        # If new tehnology is more efficient, adopt it.
        if(self.MC < oldMC):
            self.logger.trace("Firm {:d} lowered its marginal cost through INNOVATION. Previous MC: {:.2f}; New MC: {:.2f}".format(self.firmId, oldMC, self.MC))
            self.attractionForResearch += 1
            self.attractionForInnovation += 1
        else:
            self.logger.trace("Firm {:d} failed to reduce its marginal cost through INNOVATION. Previous MC: {:.2f}, Experimental MC: {:.2f}".format(self.firmId, oldMC, self.MC))
            self.technology = oldTechnology
            self.updateMarginalCost()
            self.attractionForNoResearch += 1
            self.attractionForImitation += 1

        return Parameters.InnovationCost

    def processImitation(self):
        oldTechnology = Technology(self.technology.tasks)
        oldMC = self.MC
        firmToImitate = self.selectFirmToImitate()
        
        if(firmToImitate != None):
            self.imitate(firmToImitate)
            self.updateMarginalCost()
        else:
            self.logger.trace("Found NO PROFITABLE FIRM to immitate.")

        # If new tehnology is more efficient, adopt it.
        if(self.MC < oldMC):
            self.logger.trace("Firm {:d} lowered its marginal cost through IMMITATION. Previous MC: {:.2f}; New MC: {:.2f}".format(self.firmId, oldMC, self.MC))
            self.attractionForResearch += 1
            self.attractionForImitation += 1
        else:
            self.logger.trace("Firm {:d} failed to reduce its marginal cost through IMMITATION. Previous MC: {:.2f}, Experimental MC: {:.2f}".format(self.firmId, oldMC, self.MC))
            self.technology = oldTechnology
            self.updateMarginalCost()
            self.attractionForNoResearch += 1
            self.attractionForInnovation += 1

        return Parameters.ImitationCost

    def imitate(self, otherFirm):
        self.technology.copyOneRandomTask(otherFirm.technology)

    # More profitable competitors have a higher likelihood of being observed by this firm.
    # This function uses the Roulette Wheel Algorithm (more info: http://geneticalgorithms.ai-depot.com/Tutorial/Overview.html)
    def selectFirmToImitate(self):
        self.logger.trace("Selecting a firm to imitage...")
        otherFirms = [firm for firm in self.industry.profitableFirmsPrevPeriod if firm.firmId != self.firmId]

        # Really bad previous period. No profitable firms.
        if(len(otherFirms) == 0):
            return None

        # The point in the CDF from which we select a firm to be observed
        selection = random.random()
        self.logger.trace("Point in CDF: {:.3f}".format(selection))

        # Sum the profits 
        sumOfProfits = 0.0
        for firm in otherFirms:
            sumOfProfits += firm.profits
        self.logger.trace("Sum of profits of competitors: {:.2f}".format(sumOfProfits))

        # Since we already have a random selection from 0 to 1, 
        # the firm for which the range of probability in the CDF contains the selection will be the observed one.
        # Firms with higher share of profits will occupy a broader range in the CDF, which will increase its likelihood of being observed.
        cdf = 0.0
        for firm in otherFirms:
            probOfBeingObserved = firm.profits / sumOfProfits
            self.logger.trace("Competitor {:d} has a {:.2%} probability of being observed. Its range in the CDF is from {:.3f} to {:.3f}".format(firm.firmId, probOfBeingObserved, cdf, cdf + probOfBeingObserved))
            if(cdf < selection <= cdf + probOfBeingObserved):
                self.logger.trace("Competitor {:d} was observed. Point in CDF: {:.3f}".format(firm.firmId, selection))
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

class FirmStatus(Enum):
    POTENTIAL_ENTRANT = 1
    INACTIVE_INCUMBENT = 2
    ACTIVE_INCUMBENT = 3
    DEAD = 4

