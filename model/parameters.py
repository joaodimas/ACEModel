class Parameters:

    # ------ SYSTEM CONFIG - BEGIN
    LogLevel = {"Console": ["INFO"]}
    EnableProfiling = False
    NumberOfParallelProcesses = 72 # Set this to 3x the number of CPUs. Parallelism is only used if multiple simulations are performed (NumberOfSimulations > 1). Otherwise, only 1 process will be started.
    STOCHASTIC = 0
    DETERMINISTIC = 1
    # ------ SYSTEM CONFIG - END
    

    # MODEL PARAMETERS
    NumberOfSimulations = 1 # Number of independent replications. A dataset with the means for each period and variable will be saved.
    PeriodsToSaveCrossSectionalData = [5000]
    PeriodRangeToSavePanelData = [4961, 5000]


    # ---------------- CHAPTER 4 of Chang's book -----------------------
    # 
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
    # PeriodStartOfTechChange = 0
    # MaxMagnituteOfChangeInTechEnv = 8
    # TypeOfCycle = None  # <----------- NO BUSINESS CYCLES
    # 
    # ------------------------------------------------------------------



    # ---------------- CHAPTER 5 of Chang's book -----------------------
    # 
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
    # PeriodStartOfTechChange = None    # <----------- NO TECH CHANGE
    # TypeOfCycle = None  # <----------- NO BUSINESS CYCLES
    # 
    # ------------------------------------------------------------------



    # ---------------- CHAPTER 8 of Chang's book -----------------------
    # 
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
    MeanMarketSize = 32
    RateOfChangeInTechEnv = 0.1
    PeriodStartOfTechChange = 0
    MaxMagnituteOfChangeInTechEnv = 8
    TypeOfCycle = STOCHASTIC  # <----------- STOCHASTIC BUSINESS CYCLES
    PeriodsOfConstantDemand = 2000
    MinMarketSize = 0.1
    RateOfPersistenceInDemand = 0.95
    # 
    # ------------------------------------------------------------------

    # Config of deterministic business cycles. Only used if TypeOfCycle = DETERMINISTIC
    # WaveAmplitude = 2
    # PeriodOfHalfTurn = 500
    
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