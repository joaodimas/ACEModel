import math
from model.util.random import Random
from model.util.logger import Logger
from model.parameters import Parameters
from model.technology import Technology
from model.cycle_type import CycleType

class Shocks:

    @classmethod
    def processShocks(cls, industry):
        Logger.trace("External shocks: Processing...", industry=industry)
        # Technological shock: Every period the optimal technology changes with a probability = Parameters.RateOfChangeInTechEnv.
        # The new optimal will have a maximum hamming distance from previous optimum = Parameters.MaxMagnituteOfChangeInTechEnv.
        if Parameters.PeriodStartOfTechnologicalShocks is not None and industry.currentPeriod >= Parameters.PeriodStartOfTechnologicalShocks:
            if Random.random() < Parameters.RateOfChangeInTechEnv:
                Logger.trace("HIT BY A TECHNOLOGICAL SHOCK!", industry=industry)
                previousOptimal = Technology(industry.currentOptimalTech.tasks)
                Logger.trace("Previous technology:{:0{:d}b}", (previousOptimal.tasks, Parameters.NumberOfTasks), industry=industry)
                industry.currentOptimalTech.changeRandomly()
                Logger.trace("New technology:{:0{:d}b}", (industry.currentOptimalTech.tasks, Parameters.NumberOfTasks), industry=industry)
               #assert previousOptimal.calculateHammingDistance(industry.currentOptimalTech) == industry.currentOptimalTech.magnitudeOfChange
                Logger.trace("Magnitude of change: {:d}", (industry.currentOptimalTech.magnitudeOfChange), industry=industry)
            else:
                Logger.trace("NO TECHNOLOGICAL SHOCK.", industry=industry)


        # Demand shock: every period starting at (Parameters.PeriodsOfConstantDemand + 1) there is a change in the market size
        if industry.currentPeriod > Parameters.PeriodsOfConstantDemand:
            if Parameters.TypeOfCycle == CycleType.STOCHASTIC:
                Logger.trace("STOCHASTIC BUSINESS CYCLE", (industry.simulation, industry.currentPeriod))
                prevMktSize = industry.demand.marketSize
                industry.demand.marketSize = max(Parameters.MinMarketSize, (1 - Parameters.RateOfPersistenceInDemand) * Parameters.MeanMarketSize + Parameters.RateOfPersistenceInDemand * industry.demand.marketSize + Random.uniform(-0.5, 0.5))
                Logger.trace("Previous market size: {:.2f}; New market size: {:.2f}", (industry.simulation, industry.currentPeriod, prevMktSize, industry.demand.marketSize))
            elif Parameters.TypeOfCycle == CycleType.DETERMINISTIC:
                Logger.trace("DETERMINISTIC BUSINESS CYCLE", (industry.simulation, industry.currentPeriod))
                prevMktSize = industry.demand.marketSize
                industry.demand.marketSize = Parameters.MeanMarketSize + Parameters.WaveAmplitude * math.sin(math.pi / Parameters.PeriodOfHalfTurn * industry.currentPeriod)
                Logger.trace("Previous market size: {:.2f}; New market size: {:.2f}", (industry.simulation, industry.currentPeriod, prevMktSize, industry.demand.marketSize))

        Logger.trace("External shocks: OK!", industry=industry)

