class Parameters:

    # SYSTEM CONFIG
    # LogLevel = {"Console": [], "File": ["INFO"]}
    LogLevel = {"Console": ["INFO", "DEBUG", "TRACE"], "File": ["INFO", "DEBUG", "TRACE"]}
    EnableProfiling = False
    NumberOfWorkers = 72
    STOCHASTIC = 0
    DETERMINISTIC = 1
    

    # MODEL PARAMETERS
    NumberOfSimulations = 1

    # Basic
    NumberOfTasks = 96
    NumberOfPotentialEntrants = 1
    StartupWealth = 0
    ThresholdNetWealthForSurvival = 0 
    DemandIntercept = 300
    FixedProductionCost = 200
    FixedCostOfInnovation = 100
    FixedCostOfImitation = 50
    InitialAttractionForResearch = 10
    InitialAttractionForNoResearch = 10
    InitialAttractionForInnovation = 10
    InitialAttractionForImitation = 10
    TimeHorizon = 100
    MeanMarketSize = 4
    RateOfChangeInTechEnv = 0.1
    MaxMagnituteOfChangeInTechEnv = 8


    PeriodStartOfTechChange = 0
    RateOfMeanMarketSizeGrowth = 0

    # Business Cycles
    TypeOfCycle = None  # Options: None, DETERMINISTIC, STOCHASTIC. None implies a constant Market Size
    PeriodsOfConstantDemand = 2000

    # Business Cycles - STOCHASTIC
    MinMarketSize = 0.1
    RateOfPersistenceInDemand = 0.97

    # Business Cycles - DETERMINISTIC
    WaveAmplitude = 2
    PeriodOfHalfTurn = 500
    

    # BASELINE PARAMETERS - Chapter 4 of Chang's book
    # NumberOfTasks = 96
    # NumberOfPotentialEntrants = 40
    # StartupWealth = 0
    # ThresholdNetWealthForSurvival = 0 
    # DemandIntercept = 300
    # FixedProductionCost = 200
    # FixedCostOfInnovation = 100
    # FixedCostOfImitation = 50
    # InitialAttractionForResearch = 10
    # InitialAttractionForNoResearch = 10
    # InitialAttractionForInnovation = 10
    # InitialAttractionForImitation = 10
    # TimeHorizon = 5000
    # MeanMarketSize = 4
    # RateOfChangeInTechEnv = 0.1
    # MaxMagnituteOfChangeInTechEnv = 8


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
                    "FixedProductionCost: " + self.FixedProductionCost + ", "
                    "DemandIntercept: " + self.DemandIntercept + ", "
                    "MeanMarketSize: " + self.MeanMarketSize + ", "
                    "ThresholdNetWealthForSurvival: " + self.ThresholdNetWealthForSurvival + ", "
                    "NumberOfFirms: " + self.NumberOfFirms + ", "
                    "TimeHorizon: " + self.TimeHorizon + "}"                   
               )
