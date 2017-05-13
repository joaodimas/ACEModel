import math
from model.util.random import Random
from model.util.logger import Logger
from model.parameters import Parameters
from model.cycle_type import CycleType

class ExogenousEffects:

    @classmethod
    def process(cls, industry):
        Logger.trace("External shocks: Processing...", industry=industry)

        cls.technologicalShock(industry)        

        cls.addNewOptimalTechnology(industry)

        cls.growth(industry)

        cls.businessCycle(industry)

        Logger.trace("External shocks: OK!", industry=industry)

    @classmethod
    def technologicalShock(cls, industry):
        # Technological shock: Every period the optimal technology changes with a probability = Parameters.RateOfChangeInTechEnv.
        # The new optimal will have a maximum hamming distance from previous optimum = Parameters.MaxMagnituteOfChangeInTechEnv.
        if Parameters.PeriodStartOfTechnologicalShocks is not None and industry.currentPeriod >= Parameters.PeriodStartOfTechnologicalShocks:
            if Random.random() < Parameters.RateOfChangeInTechEnv:
                Logger.trace("HIT BY A TECHNOLOGICAL SHOCK!", industry=industry)
                
                for tech in industry.currentOptimalTechs:
                    Logger.trace("Changing optimal technology {:d}", (tech.techId), industry=industry)
                    Logger.trace("Previous technology:{:0{:d}b}", (tech.tasks, Parameters.NumberOfTasks), industry=industry)
                    
                    tech.changeRandomly()
                    
                    Logger.trace("New technology:{:0{:d}b}", (tech.tasks, Parameters.NumberOfTasks), industry=industry)
                    Logger.trace("Magnitude of change: {:d}", (tech.magnitudeOfChange), industry=industry)

            else:
                Logger.trace("NO TECHNOLOGICAL SHOCK.", industry=industry)

    @classmethod
    def addNewOptimalTechnology(cls, industry):
        # Adding new optimal technology
        if hasattr(Parameters, 'IntervalBeforeAddingNewOptimal') and Parameters.IntervalBeforeAddingNewOptimal > 0 and industry.currentPeriod % Parameters.IntervalBeforeAddingNewOptimal == 1 and len(industry.currentOptimalTechs) < Parameters.MaximumOptimalTechnologies:
            industry.addNewOptimalTech()
            Logger.info("New optimal tech added to industry.", industry=industry)

    @classmethod
    def growth(cls, industry):
        # Constant growth in the mean market size
        if hasattr(Parameters, 'PeriodStartOfGrowth') and industry.currentPeriod >= Parameters.PeriodStartOfGrowth:
            oldMeanMarketSize = industry.demand.meanMarketSize
            industry.demand.meanMarketSize *= 1 + Parameters.RateOfGrowthInMeanMarketSize
            industry.demand.marketSize += industry.demand.meanMarketSize - oldMeanMarketSize
            industry.demand.minMarketSize *= 1 + Parameters.RateOfGrowthInMeanMarketSize
            industry.demand.whiteNoise *= 1 + Parameters.RateOfGrowthInMeanMarketSize

    @classmethod
    def businessCycle(cls, industry):
        # Demand shock: every period starting at (Parameters.PeriodStartOfCycles + 1) there is a change in the market size
        if industry.currentPeriod >= Parameters.PeriodStartOfCycles:
            if Parameters.TypeOfCycle == CycleType.STOCHASTIC:
                Logger.trace("STOCHASTIC BUSINESS CYCLE", (industry.simulationNumber, industry.currentPeriod))
                prevMktSize = industry.demand.marketSize
                industry.demand.marketSize = max(industry.demand.minMarketSize, (1 - Parameters.RateOfPersistenceInDemand) * industry.demand.meanMarketSize + Parameters.RateOfPersistenceInDemand * industry.demand.marketSize + Random.uniform(-industry.demand.whiteNoise, industry.demand.whiteNoise))
                Logger.trace("Previous market size: {:.2f}; New market size: {:.2f}", (industry.simulationNumber, industry.currentPeriod, prevMktSize, industry.demand.marketSize))
            elif Parameters.TypeOfCycle == CycleType.DETERMINISTIC:
                Logger.trace("DETERMINISTIC BUSINESS CYCLE", (industry.simulationNumber, industry.currentPeriod))
                prevMktSize = industry.demand.marketSize
                industry.demand.marketSize = industry.demand.meanMarketSize + Parameters.WaveAmplitude * math.sin(math.pi / Parameters.PeriodOfHalfTurn * industry.currentPeriod)
                Logger.trace("Previous market size: {:.2f}; New market size: {:.2f}", (industry.simulationNumber, industry.currentPeriod, prevMktSize, industry.demand.marketSize))