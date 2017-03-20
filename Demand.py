import logging
from Parameters import Parameters

class Demand:

    def __init__(self, industry):
        self.marketSize = Parameters.MeanMarketSize
        self.industry = industry
        self.eqPrice = 0
        self.logger = logging.getLogger("ACEModel")
	# Obtained from the first order condition for each firm.
    def updateEqPrice(self):
        self.eqPrice = (1 / (len(self.industry.activeIncumbentFirms) + 1)) * (Parameters.DemandIntercept + self.industry.currentActiveSumOfMC)
        self.logger.trace("Equilibrium price is {:.2f}; Demand intercept: {:d}; Active incumbents: {:d}; Active sum of MC: {:.2f}".format(self.eqPrice, Parameters.DemandIntercept, len(self.industry.activeIncumbentFirms), self.industry.currentActiveSumOfMC))

    def getExpEqPrice(self, potentialEntrant):
        sumOfMC = self.industry.sumOfActiveSurvivorsMC + potentialEntrant.MC
        expEqPrice = (1 / (len(self.industry.activeSurvivorsOfPreviousPeriod) + 1)) * (Parameters.DemandIntercept + sumOfMC)
        self.logger.trace("Firm {:d} expects an equilibrium price of {:.2f}. Active survivors of previous period: {:d}; Sum of MC of active survivores {:.2f}; MC of potential entrant: {:.2f}.".format(potentialEntrant.firmId, expEqPrice, len(self.industry.activeSurvivorsOfPreviousPeriod), self.industry.sumOfActiveSurvivorsMC, potentialEntrant.MC))
        return expEqPrice