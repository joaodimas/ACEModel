from model.cycle_type import CycleType

class Parameters:

    @classmethod
    def setInitialParameters(cls):
        
        # MODEL PARAMETERS
        cls.NumberOfIndependentReplications = 10 # Number of independent replications. A dataset with the means for each period and variable will be saved.
        cls.PeriodsToSaveCrossSectionalData = [100]
        cls.PeriodRangeToSavePanelData = [60, 100]


        # ---------------- TESTS -----------------------
        # # 
        cls.NumberOfTasks = 96
        cls.NumberOfPotentialEntrants = 40
        cls.StartupWealth = 0
        cls.ThresholdNetWealthForSurvival = 0 
        cls.DemandIntercept = 300
        cls.FixedProductionCost = 200
        cls.FixedCostOfInnovation = 100
        cls.FixedCostOfImitation = 50
        cls.InitialAttractionToResearch = 10
        cls.InitialAttractionToNotResearch = 10
        cls.InitialAttractionToInnovate = 10
        cls.InitialAttractionToImitate = 10
        cls.TimeHorizon = 100
        cls.MeanMarketSize = 4
        #RateOfGrowthInMeanMarketSize = 0
        #PeriodStartOfGrowth = 2921
        cls.RateOfChangeInTechEnv = 0.1
        cls.PeriodStartOfTechnologicalShocks = 0
        cls.MaxMagnituteOfChangeInTechEnv = 8
        cls.TypeOfCycle = None  # <----------- NO BUSINESS CYCLES
        # cls.PeriodStartOfCycles = 0
        # cls.MinMarketSize = 0.1
        # cls.RateOfPersistenceInDemand = 0.97
        # cls.CycleWhiteNoise = 0.5

        cls.MaximumOptimalTechnologies = 5
        cls.InitialOptimalTechnologies = 1
        cls.IntervalBeforeAddingNewOptimal = 1000
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
        # InitialAttractionToResearch = 10
        # InitialAttractionToNotResearch = 10
        # InitialAttractionToInnovate = 10
        # InitialAttractionToImitate = 10
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
        # InitialAttractionToResearch = 10
        # InitialAttractionToNotResearch = 10
        # InitialAttractionToInnovate = 10
        # InitialAttractionToImitate = 10
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
        # InitialAttractionToResearch = 10
        # InitialAttractionToNotResearch = 10
        # InitialAttractionToInnovate = 10
        # InitialAttractionToImitate = 10
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
