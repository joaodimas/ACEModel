"""
Agent-based model based in Chang (2015), "Computational Industrial Economics: A generative approach to dynamic analysis in industrial organization". Additional features are described in my master thesis for Panthéon-Sorbonne MSc in Economics.

Author: João Dimas (joaohenriqueavila@gmail.com)
Supervisor: Prof. Angelo Secchi (Paris 1, PSE)

"""

from model.cycle_type import CycleType

class Parameters:

    @classmethod
    def setInitialParameters(cls):
        
        # MODEL PARAMETERS
        cls.NumberOfIndependentReplications = 100 # Number of independent replications. A dataset with the means for each period and variable will be saved.
        cls.PeriodsToSaveCrossSectionalData = [1000, 2000, 5000]
        cls.PeriodRangeToSavePanelData = [4950, 5000]


        # ---------------- CHAPTER 4 of Chang's book -----------------------
        # 
        # cls.NumberOfTasks = 96
        # cls.NumberOfPotentialEntrants = 40
        # cls.StartupWealth = 0
        # cls.ThresholdNetWealthForSurvival = 0 
        # cls.DemandIntercept = 300
        # cls.FixedProductionCost = 200
        # cls.FixedCostOfInnovation = 100
        # cls.FixedCostOfImitation = 50
        # cls.InitialAttractionToResearch = 10
        # cls.InitialAttractionToNotResearch = 10
        # cls.InitialAttractionToInnovate = 10
        # cls.InitialAttractionToImitate = 10
        # cls.TimeHorizon = 5000
        # cls.MeanMarketSize = 4
        # cls.RateOfChangeInTechEnv = 0.1
        # cls.PeriodStartOfTechnologicalShocks = 0
        # cls.MaxMagnituteOfChangeInTechEnv = 8
        # cls.TypeOfCycle = None  # <----------- NO BUSINESS CYCLES
        # cls.PeriodStartOfCycles = 2001 # Ignored
        # cls.MinMarketSize = 0.1 # Ignored
        # cls.RateOfPersistenceInDemand = 0.95 # Ignored
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
        cls.TimeHorizon = 5000
        cls.MeanMarketSize = 4
        cls.RateOfChangeInTechEnv = 0.1
        cls.PeriodStartOfTechnologicalShocks = 0
        cls.MaxMagnituteOfChangeInTechEnv = 8
        cls.TypeOfCycle = CycleType.STOCHASTIC  # <----------- STOCHASTIC BUSINESS CYCLES
        cls.PeriodStartOfCycles = 2001
        cls.MinMarketSize = 0.1
        cls.RateOfPersistenceInDemand = 0.95
        cls.CycleWhiteNoise = 0.5
        # # 
        # # ------------------------------------------------------------------

        # # Config of deterministic business cycles. Only used if TypeOfCycle = DETERMINISTIC
        cls.WaveAmplitude = 2
        cls.PeriodOfHalfTurn = 500
