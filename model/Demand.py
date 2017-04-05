from model.Parameters import Parameters

class Demand:

    def __init__(self, industry):
        self.marketSize = Parameters.MeanMarketSize
        self.industry = industry
        self.eqPrice = 0
        
	# Obtained from the first order condition for each firm.
    def updateEqPrice(self):
        sumOfMC = self.industry.currentActiveSumOfMC
        competitors = len(self.industry.activeIncumbentFirms)
        self.eqPrice = (1 / (competitors + 1)) * (Parameters.DemandIntercept + sumOfMC)

    def getExpEqPrice(self, potentialEntrant):
        sumOfMC = self.industry.sumOfActiveSurvivorsMC + potentialEntrant.MC
        competitors = len(self.industry.activeSurvivorsOfPreviousPeriod) + 1
        expEqPrice = (1 / (competitors + 1)) * (Parameters.DemandIntercept + sumOfMC)
        return expEqPrice