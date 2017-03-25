from enum import Enum

class CycleType(Enum):
    STOCHASTIC = 0
    SINUSOIDAL = 1

class Parameters:

    # SYSTEM CONFIG
    LogLevel = {"Console": ["INFO"], "File": ["INFO", "DEBUG"]}
    EnableProfiling = False
    STOCHASTIC = 0
    SINUSOIDAL = 1

    # MODEL PARAMETERS

    # Basic
    NumberOfPeriods = 10000
    FixedCost = 200
    DemandIntercept = 300
    MeanMarketSize = 4

    # Growth
    RateOfMeanMarketSizeGrowth = 0

    # Business Cycles
    TypeOfCycle = STOCHASTIC  # Other: SINUSOIDAL
    MinMarketSize = 0.1
    RateOfPersistenceInDemand = 0.97
    PeriodsOfConstantDemand = 2000

    # Firms
    StartupWealth = 0
    MinimumWealthForSurvival = 0 
    NumberOfPotentialEntrants = 40

    # Optimal Technology
    NumberOfTasks = 94
    MaxMagnituteOfTechChange = 8
    RateOfTechChange = 0.1
    PeriodStartOfTechChange = 0

    # R&D
    InnovationCost = 100.0
    ImitationCost = 50.0
    InitialAttractionForResearch = 10
    InitialAttractionForNoResearch = 10
    InitialAttractionForInnovation = 10
    InitialAttractionForImitation = 10


    @classmethod
    def describe(cls):
        desc = "----- PARAMETERS -----\n"
        for key, value in Parameters.getParameters().items():
            desc += key + ": " + str(value) + "\n"

        return desc

    @classmethod
    def getParameters(cls):
        parameters = {}
        obj = Parameters()
        members = [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__")]
        for member in members:
            parameters[member] = getattr(obj, member)
        return parameters

    def toJSON(self):
        return ("{"
                    "NumberOfTasks: " + self.NumberOfTasks + ", "
                    "FixedCost: " + self.FixedCost + ", "
                    "DemandIntercept: " + self.DemandIntercept + ", "
                    "MeanMarketSize: " + self.MeanMarketSize + ", "
                    "MinimumWealthForSurvival: " + self.MinimumWealthForSurvival + ", "
                    "NumberOfFirms: " + self.NumberOfFirms + ", "
                    "NumberOfPeriods: " + self.NumberOfPeriods + "}"                   
               )
