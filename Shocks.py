import random
from Logger import Logger
from Parameters import Parameters
from Firm import Firm
from Technology import Technology
from BusinessCycles import BusinessCycles

class Shocks:

    @classmethod
    def processShocks(cls, industry):
        Logger.trace("[SIM {:d}][PERIOD {:d}] External shocks: Processing...", (industry.simulation, industry.currentPeriod))
        # Technological shock: Every period the optimal technology changes with a probability = Parameters.RateOfChangeInTechEnv.
        # The new optimal will have a maximum hamming distance from previous optimum = Parameters.MaxMagnituteOfChangeInTechEnv.
        if(Parameters.RateOfChangeInTechEnv > 0 and industry.currentPeriod >= Parameters.PeriodStartOfTechChange):
            if(random.random() < Parameters.RateOfChangeInTechEnv):
                Logger.trace("[SIM {:d}][PERIOD {:d}] HIT BY A TECHNOLOGICAL SHOCK!", (industry.simulation, industry.currentPeriod))
                previousOptimal = Technology(industry.currentOptimalTech.tasks)
                Logger.trace("[SIM {:d}][PERIOD {0:0d}] Previous technology:{1:0{2}b}", (industry.simulation, industry.currentPeriod, previousOptimal.tasks, Parameters.NumberOfTasks))
                industry.currentOptimalTech.transformRandomlyWithMaxDistance(Parameters.MaxMagnituteOfChangeInTechEnv)
                Logger.trace("[SIM {:d}][PERIOD {0:0d}] New technology:{1:0{2}b}", (industry.simulation, industry.currentPeriod, industry.currentOptimalTech.tasks, Parameters.NumberOfTasks))
                assert previousOptimal.calculateHammingDistance(industry.currentOptimalTech) == industry.currentOptimalTech.magnitudeOfChange
                Logger.trace("[SIM {:d}][PERIOD {:d}] Magnitude of change: {:d}", (industry.simulation, industry.currentPeriod, industry.currentOptimalTech.magnitudeOfChange))
            else:
                Logger.trace("[SIM {:d}][PERIOD {:d}] NO TECHNOLOGICAL SHOCK.", (industry.simulation, industry.currentPeriod))


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
        Logger.trace("[SIM {:d}][PERIOD {:d}] External shocks: OK!", (industry.simulation, industry.currentPeriod))