from Logger import Logger
from Parameters import Parameters

class Demand:

    def __init__(self, industry):
        self.marketSize = Parameters.MeanMarketSize
        self.industry = industry
        self.eqPrice = 0
	# Obtained from the first order condition for each firm.
    def updateEqPrice(self):
        self.eqPrice = (1 / (len(self.industry.activeIncumbentFirms) + 1)) * (Parameters.DemandIntercept + self.industry.currentActiveSumOfMC)

    def getExpEqPrice(self, potentialEntrant):
        sumOfMC = self.industry.sumOfActiveSurvivorsMC + potentialEntrant.MC
        expEqPrice = (1 / (len(self.industry.activeSurvivorsOfPreviousPeriod) + 1)) * (Parameters.DemandIntercept + sumOfMC)
        return expEqPrice