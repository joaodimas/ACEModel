from Parameters import Parameters
import random
from Logger import Logger
from Firm import Firm

class Shocks:

    @classmethod
    def processShocks(cls, industry):
        Logger.debug("External shocks: Processing...")
        # Shock 1: Every period the optimal technology changes with a probability = Parameters.RateOfTechChange.
        # The new optimal will have a maximum hamming distance from previous optimum = Parameters.MaxMagnituteOfTechChange.
        if(Parameters.RateOfTechChange > 0 and industry.currentPeriod >= Parameters.PeriodStartOfTechChange):
            if(random.random() < Parameters.RateOfTechChange):
                Logger.log("HIT BY A TECHNOLOGICAL SHOCK!")
                previousOptimal = industry.currentOptimalTech
                industry.currentOptimalTech = industry.currentOptimalTech.generateRandomWithMaxDistance(Parameters.MaxMagnituteOfTechChange)
                assert previousOptimal.calculateHammingDistance(industry.currentOptimalTech) == industry.currentOptimalTech.magnitudeOfChange
                Logger.log("Magnitude of change: {:d}".format(industry.currentOptimalTech.magnitudeOfChange))
            else:
                Logger.log("NO TECHNOLOGICAL SHOCK.")



        # Shock 2: No potential entrants after period 100.
        # if(industry.currentPeriod >= 100):
        #     industry.potentialEntrants = []



        # Shock 3: At period 50, all potential entrants have technology with distance 40 from the optimal
        # if(industry.currentPeriod >= 100):
        #     Logger.log("HIT BY EFFICIENT NEW ENTRANTS!")
        #     industry.potentialEntrants = []
        #     for x in range(Parameters.NumberOfPotentialEntrants):
        #         industry.potentialEntrants.append(Firm(industry.newFirmId(), industry, industry.currentOptimalTech.generateRandomWithMaxDistance(40)))
        Logger.debug("External shocks: OK!")