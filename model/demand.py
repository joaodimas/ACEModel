"""
Agent-based model based in Chang (2015), "Computational Industrial Economics: A generative approach to dynamic analysis in industrial organization". Additional features are described in my master thesis for Panthéon-Sorbonne MSc in Economics.

Author: João Dimas (joaohenriqueavila@gmail.com)
Supervisor: Prof. Angelo Secchi (Paris 1, PSE)

"""

from model.parameters import Parameters

class Demand:

    def __init__(self, industry):
        self.meanMarketSize = Parameters.MeanMarketSize
        self.marketSize = self.meanMarketSize
        if hasattr(Parameters, "TypeOfCycle") and Parameters.TypeOfCycle is not None:
            self.minMarketSize = Parameters.MinMarketSize
            self.cycleWhiteNoise = Parameters.CycleWhiteNoise
        self.industry = industry
        self.eqPrice = 0
        
	# Obtained from the first order condition for each firm.
    def updateEqPrice(self):
        sumOfMC = self.industry.sumOfActiveFirmsMC
        competitors = len(self.industry.activeFirms)
        self.eqPrice = (1 / (competitors + 1)) * (Parameters.DemandIntercept + sumOfMC)
        return self.eqPrice

    def getExpEqPrice(self, potentialEntrant):
        sumOfMC = self.industry.sumOfActiveSurvivorsMC + potentialEntrant.MC
        competitors = len(self.industry.activeSurvivorsOfPreviousPeriod) + 1
        expEqPrice = (1 / (competitors + 1)) * (Parameters.DemandIntercept + sumOfMC)
        return expEqPrice

    @classmethod
    def calculatePrice(cls, nmbOfFirms, demandIntercept, sumOfMC):
        return 1 / (nmbOfFirms + 1) * (demandIntercept + sumOfMC)

    @classmethod
    def calculateFirmOutput(cls, marketSize, nmbFirms, demandIntercept, sumOfMC, firmMC):
        return marketSize * (1 / (nmbFirms + 1) * (demandIntercept + sumOfMC) - firmMC)

    @classmethod
    def calculateAggregateOutput(cls, marketSize, nmbFirms, demandIntercept, sumOfMC):
        return 1 / (nmbFirms + 1) * (nmbFirms * marketSize * demandIntercept - marketSize * sumOfMC)