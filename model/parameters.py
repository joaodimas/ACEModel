from model.cycle_type import CycleType

class Parameters:

    # MODEL PARAMETERS
    NumberOfIndependentReplications = 1 # Number of independent replications. A dataset with the means for each period and variable will be saved.
    PeriodsToSaveCrossSectionalData = [2920, 3000]
    PeriodRangeToSavePanelData = [2960, 3000]


    # ---------------- TESTS -----------------------
    # # 
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
    TimeHorizon = 3000
    MeanMarketSize = 4
    RateOfGrowthInMeanMarketSize = 0.03
    PeriodStartOfGrowth = 2921
    RateOfChangeInTechEnv = 0.1
    PeriodStartOfTechnologicalShocks = 0
    MaxMagnituteOfChangeInTechEnv = 8
    TypeOfCycle = CycleType.STOCHASTIC  # <----------- NO BUSINESS CYCLES
    PeriodStartOfCycles = 501
    MinMarketSize = 0.1
    RateOfPersistenceInDemand = 0.97
    WhiteNoise = 0.5
    # 
    # ------------------------------------------------------------------


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
    # PeriodStartOfTechnologicalShocks = 0
    # MaxMagnituteOfChangeInTechEnv = 8
    # TypeOfCycle = CycleType.NONE  # <----------- NO BUSINESS CYCLES
    # PeriodStartOfCycles = 2001 # Ignored
    # MinMarketSize = 0.1 # Ignored
    # RateOfPersistenceInDemand = 0.95 # Ignored
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
    # PeriodStartOfTechnologicalShocks = None    # <----------- NO TECH CHANGE
    # TypeOfCycle = Cycle.NONE  # <----------- NO BUSINESS CYCLES
    # 
    # ------------------------------------------------------------------



    # ---------------- CHAPTER 8 of Chang's book -----------------------
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
    # PeriodStartOfTechnologicalShocks = 0
    # MaxMagnituteOfChangeInTechEnv = 8
    # TypeOfCycle = CycleType.STOCHASTIC  # <----------- STOCHASTIC BUSINESS CYCLES
    # PeriodStartOfCycles = 2001
    # MinMarketSize = 0.1
    # RateOfPersistenceInDemand = 0.95
    # 
    # ------------------------------------------------------------------

    # Config of deterministic business cycles. Only used if TypeOfCycle = DETERMINISTIC
    # WaveAmplitude = 2
    # PeriodOfHalfTurn = 500
