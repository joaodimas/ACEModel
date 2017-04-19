from model.util.random import Random
from model.util.logger import Logger
from model.parameters import Parameters
from model.technology import Technology
from model.business_cycles import BusinessCycles

class Shocks:

    @classmethod
    def processShocks(cls, industry):
        Logger.trace("External shocks: Processing...", industry=industry)
        # Technological shock: Every period the optimal technology changes with a probability = Parameters.RateOfChangeInTechEnv.
        # The new optimal will have a maximum hamming distance from previous optimum = Parameters.MaxMagnituteOfChangeInTechEnv.
        if(Parameters.PeriodStartOfTechChange is not None and industry.currentPeriod >= Parameters.PeriodStartOfTechChange):
            if(Random.random() < Parameters.RateOfChangeInTechEnv):
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
        if(Parameters.TypeOfCycle is not None and industry.currentPeriod > Parameters.PeriodsOfConstantDemand):
            if(Parameters.TypeOfCycle == Parameters.STOCHASTIC):
                BusinessCycles.generateStochasticCycle(industry)
            elif(Parameters.TypeOfCycle == Parameters.DETERMINISTIC):
                BusinessCycles.generateDeterministicCycle(industry)


        Logger.trace("External shocks: OK!", industry=industry)

