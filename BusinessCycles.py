import random, math
from Logger import Logger
from Parameters import Parameters

class BusinessCycles:

    @classmethod
    def generateStochasticCycle(cls, industry):
        Logger.trace("[PERIOD {:d}] STOCHASTIC BUSINESS CYCLE", industry.currentPeriod)
        prevMktSize = industry.demand.marketSize
        industry.demand.marketSize = max(Parameters.MinMarketSize, (1 - Parameters.RateOfPersistenceInDemand) * Parameters.MeanMarketSize + Parameters.RateOfPersistenceInDemand * industry.demand.marketSize + random.uniform(-0.5, 0.5))
        Logger.trace("[PERIOD {:d}] Previous market size: {:.2f}; New market size: {:.2f}", (industry.currentPeriod, prevMktSize, industry.demand.marketSize))

    @classmethod
    def generateDeterministicCycle(cls, industry):
        Logger.trace("[PERIOD {:d}] DETERMINISTIC BUSINESS CYCLE", industry.currentPeriod)
        prevMktSize = industry.demand.marketSize
        industry.demand.marketSize = Parameters.MeanMarketSize + Parameters.WaveAmplitude * math.sin(math.pi / Parameters.PeriodOfHalfTurn * industry.currentPeriod)
        Logger.trace("[PERIOD {:d}] Previous market size: {:.2f}; New market size: {:.2f}", (industry.currentPeriod, prevMktSize, industry.demand.marketSize))

