import random, logging
from Parameters import Parameters
from Firm import Firm

class Shocks:

    logger = logging.getLogger("ACEModel")

    @classmethod
    def processShocks(cls, industry):
        cls.logger.trace("External shocks: Processing...")
        # Technological shock: Every period the optimal technology changes with a probability = Parameters.RateOfTechChange.
        # The new optimal will have a maximum hamming distance from previous optimum = Parameters.MaxMagnituteOfTechChange.
        if(Parameters.RateOfTechChange > 0 and industry.currentPeriod >= Parameters.PeriodStartOfTechChange):
            if(random.random() < Parameters.RateOfTechChange):
                cls.logger.trace("HIT BY A TECHNOLOGICAL SHOCK!")
                previousOptimal = industry.currentOptimalTech
                industry.currentOptimalTech = industry.currentOptimalTech.generateRandomWithMaxDistance(Parameters.MaxMagnituteOfTechChange)
                assert previousOptimal.calculateHammingDistance(industry.currentOptimalTech) == industry.currentOptimalTech.magnitudeOfChange
                cls.logger.trace("Magnitude of change: {:d}".format(industry.currentOptimalTech.magnitudeOfChange))
            else:
                cls.logger.trace("NO TECHNOLOGICAL SHOCK.")


        # Demand shock: every period there is a change in the market size
        if(industry.currentPeriod >= Parameters.PeriodStartOfDemandChange):
            cls.logger.trace("HIT BY A DEMAND SHOCK!")
            prevMktSize = industry.demand.marketSize
            industry.demand.marketSize = max(Parameters.MinMarketSize, (1 - Parameters.RateOfPersistenceInDemand) * Parameters.MeanMarketSize + Parameters.RateOfPersistenceInDemand * industry.demand.marketSize + random.uniform(-0.5, 0.5))
            cls.logger.trace("Previous market size: {:.2f}; New market size: {:.2f}".format(prevMktSize, industry.demand.marketSize))


        # Shock 2: No potential entrants after period 100.
        # if(industry.currentPeriod >= 100):
        #     industry.potentialEntrants = []


        # Shock 3: At period 50, all potential entrants have technology with distance 40 from the optimal
        # if(industry.currentPeriod >= 100):
        #     cls.logger.trace("HIT BY EFFICIENT NEW ENTRANTS!")
        #     industry.potentialEntrants = []
        #     for x in range(Parameters.NumberOfPotentialEntrants):
        #         industry.potentialEntrants.append(Firm(industry.newFirmId(), industry, industry.currentOptimalTech.generateRandomWithMaxDistance(40)))
        cls.logger.trace("External shocks: OK!")