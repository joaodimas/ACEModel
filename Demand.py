from Parameters import Parameters

class Demand:

    def __init__(self, industry):
        self.marketSize = Parameters.InitialMarketSize
        self.industry = industry
        self.eqPrice = 0

	# TODO: Check if this is necessary
    def getPrice(self, totalQuantity):
        return Parameters.DemandIntercept - totalQuantity / self.marketSize

	# Obtained from the first order condition for each firm.
    def updateEqPrice(self):
        self.eqPrice = (1 / (len(self.industry.activeIncumbentFirms) + 1)) * (Parameters.DemandIntercept + self.industry.currentActiveSumOfMC)

    def getExpEqPrice(self, potentialEntrant):
        sumOfMC = self.industry.sumOfActiveSurvivorsMC
        # Remove this after testing. This is only to check consistency in case a previous incumbent is calculating expected profits.
        if potentialEntrant not in self.industry.activeSurvivorsOfPreviousPeriod:
            sumOfMC += potentialEntrant.MC

        return (1 / (len(self.industry.activeSurvivorsOfPreviousPeriod) + 1)) * (Parameters.DemandIntercept + sumOfMC)