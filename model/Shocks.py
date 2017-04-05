from model.util.Random import Random
from model.util.Logger import Logger
from model.Parameters import Parameters
from model.Technology import Technology
from model.BusinessCycles import BusinessCycles

class Shocks:

    @classmethod
    def processShocks(cls, industry):
        Logger.trace("External shocks: Processing...", industry=industry)
        # Technological shock: Every period the optimal technology changes with a probability = Parameters.RateOfChangeInTechEnv.
        # The new optimal will have a maximum hamming distance from previous optimum = Parameters.MaxMagnituteOfChangeInTechEnv.
        if(Parameters.RateOfChangeInTechEnv > 0 and industry.currentPeriod >= Parameters.PeriodStartOfTechChange):
            if(Random.random() < Parameters.RateOfChangeInTechEnv):
                Logger.trace("HIT BY A TECHNOLOGICAL SHOCK!", industry=industry)
                previousOptimal = Technology(industry.currentOptimalTech.tasks)
                Logger.trace("Previous technology:{:0{:d}b}", (previousOptimal.tasks, Parameters.NumberOfTasks), industry=industry)
                industry.currentOptimalTech.changeRandomly()
                Logger.trace("New technology:{:0{:d}b}", (industry.currentOptimalTech.tasks, Parameters.NumberOfTasks), industry=industry)
                assert previousOptimal.calculateHammingDistance(industry.currentOptimalTech) == industry.currentOptimalTech.magnitudeOfChange
                Logger.trace("Magnitude of change: {:d}", (industry.currentOptimalTech.magnitudeOfChange), industry=industry)
            else:
                Logger.trace("NO TECHNOLOGICAL SHOCK.", industry=industry)


        # Average market size growths at a constant rate
        # Parameters.MeanMarketSize *= (1 + Parameters.RateOfMeanMarketSizeGrowth)

        # Demand shock: every period there is a change in the market size
        if(industry.currentPeriod > Parameters.PeriodsOfConstantDemand):
            if(Parameters.TypeOfCycle == Parameters.STOCHASTIC):
                BusinessCycles.generateStochasticCycle(industry)
            if(Parameters.TypeOfCycle == Parameters.DETERMINISTIC):
                BusinessCycles.generateDeterministicCycle(industry)

        # else:
            # industry.demand.marketSize = Parameters.MeanMarketSize


        # Shock 2: No potential entrants after period 100.
        # if(industry.currentPeriod >= 100):
        #     industry.potentialEntrants = []


        # Shock 3: At period 50, all potential entrants have technology with distance 40 from the optimal
        # if(industry.currentPeriod >= 100):
        #     Logger.trace("[SIM {:d}]HIT BY EFFICIENT NEW ENTRANTS!")
        #     industry.potentialEntrants = []
        #     for x in range(Parameters.NumberOfPotentialEntrants):
        #         industry.potentialEntrants.append(Firm(industry.newFirmId(), industry, industry.currentOptimalTech.generateRandomWithMaxDistance(40)))
        Logger.trace("External shocks: OK!", industry=industry)

