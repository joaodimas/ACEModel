import math
from model.util.random import Random
from model.util.logger import Logger
from model.parameters import Parameters

class BusinessCycles:

    @classmethod
    def generateStochasticCycle(cls, industry):
        Logger.trace("STOCHASTIC BUSINESS CYCLE", (industry.simulation, industry.currentPeriod))
        prevMktSize = industry.demand.marketSize
        industry.demand.marketSize = max(Parameters.MinMarketSize, (1 - Parameters.RateOfPersistenceInDemand) * Parameters.MeanMarketSize + Parameters.RateOfPersistenceInDemand * industry.demand.marketSize + Random.uniform(-0.5, 0.5))
        Logger.trace("Previous market size: {:.2f}; New market size: {:.2f}", (industry.simulation, industry.currentPeriod, prevMktSize, industry.demand.marketSize))

    @classmethod
    def generateDeterministicCycle(cls, industry):
        Logger.trace("DETERMINISTIC BUSINESS CYCLE", (industry.simulation, industry.currentPeriod))
        prevMktSize = industry.demand.marketSize
        industry.demand.marketSize = Parameters.MeanMarketSize + Parameters.WaveAmplitude * math.sin(math.pi / Parameters.PeriodOfHalfTurn * industry.currentPeriod)
        Logger.trace("Previous market size: {:.2f}; New market size: {:.2f}", (industry.simulation, industry.currentPeriod, prevMktSize, industry.demand.marketSize))

