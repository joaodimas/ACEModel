import random, logging
from Parameters import Parameters
from Firm import Firm

class Shocks:

    logger = logging.getLogger("ACEModel")

    @classmethod
    def processShocks(cls, industry):
        cls.logger.trace("External shocks: Processing...")
        # Shock 1: Every period the optimal technology changes with a probability = Parameters.RateOfTechChange.
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