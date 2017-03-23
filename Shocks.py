import random
from Logger import Logger
from Parameters import Parameters
from Firm import Firm
from Technology import Technology

class Shocks:

    @classmethod
    def processShocks(cls, industry):
        Logger.trace("External shocks: Processing...")
        # Technological shock: Every period the optimal technology changes with a probability = Parameters.RateOfTechChange.
        # The new optimal will have a maximum hamming distance from previous optimum = Parameters.MaxMagnituteOfTechChange.
        if(Parameters.RateOfTechChange > 0 and industry.currentPeriod >= Parameters.PeriodStartOfTechChange):
            if(random.random() < Parameters.RateOfTechChange):
                Logger.trace("HIT BY A TECHNOLOGICAL SHOCK!")
                previousOptimal = Technology(industry.currentOptimalTech.tasks)
                industry.currentOptimalTech.transformRandomlyWithMaxDistance(Parameters.MaxMagnituteOfTechChange)
                assert previousOptimal.calculateHammingDistance(industry.currentOptimalTech) == industry.currentOptimalTech.magnitudeOfChange
                Logger.trace("Magnitude of change: {:d}".format(industry.currentOptimalTech.magnitudeOfChange))
            else:
                Logger.trace("NO TECHNOLOGICAL SHOCK.")


        # Average market size growths at a constant rate
        Parameters.MeanMarketSize *= (1 + Parameters.RateOfMeanMarketSizeGrowth)

        # Demand shock: every period there is a change in the market size
        if(industry.currentPeriod >= Parameters.PeriodStartOfDemandCycles):
            Logger.trace("HIT BY A DEMAND SHOCK!")
            prevMktSize = industry.demand.marketSize
            industry.demand.marketSize = max(Parameters.MinMarketSize, (1 - Parameters.RateOfPersistenceInDemand) * Parameters.MeanMarketSize + Parameters.RateOfPersistenceInDemand * industry.demand.marketSize + random.uniform(-0.5, 0.5))
            Logger.trace("Previous market size: {:.2f}; New market size: {:.2f}".format(prevMktSize, industry.demand.marketSize))
        else:
            industry.demand.marketSize = Parameters.MeanMarketSize


        # Shock 2: No potential entrants after period 100.
        # if(industry.currentPeriod >= 100):
        #     industry.potentialEntrants = []


        # Shock 3: At period 50, all potential entrants have technology with distance 40 from the optimal
        # if(industry.currentPeriod >= 100):
        #     Logger.trace("HIT BY EFFICIENT NEW ENTRANTS!")
        #     industry.potentialEntrants = []
        #     for x in range(Parameters.NumberOfPotentialEntrants):
        #         industry.potentialEntrants.append(Firm(industry.newFirmId(), industry, industry.currentOptimalTech.generateRandomWithMaxDistance(40)))
        Logger.trace("External shocks: OK!")