class Parameters:

    # SYSTEM CONFIG
    LogLevel = {"Console": [], "File": ["INFO"]}
    #LogLevel = {"Console": ["INFO"], "File": ["INFO"]}
    EnableProfiling = False
    NumberOfParallelProcesses = 72 # Set this to 3x the number of CPUs. Parallelism is only used if multiple simulations are performaed (NumberOfSimulations > 1). Otherwise, only 1 process will be started.
    STOCHASTIC = 0
    DETERMINISTIC = 1
    

    # MODEL PARAMETERS
    NumberOfSimulations = 500 # Number of independent replications. A dataset with the means for each period and variable will be saved.

    # Basic
    NumberOfTasks = 96
    NumberOfPotentialEntrants = 40
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
    TimeHorizon = 5000
    MeanMarketSize = 4
    RateOfChangeInTechEnv = 0.1
    MaxMagnituteOfChangeInTechEnv = 8 # Don't try a number too close to NumberOfTasks because there is not enough decimal precision to handle the shocks.


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
