class Parameters:

    # Model parameters
    NumberOfTasks = 94
    FixedCost = 200
    DemandIntercept = 300
    MeanMarketSize = 20
    RateOfMeanMarketSizeGrowth = 0
    RateOfPersistenceInDemand = 0.97
    PeriodStartOfDemandCycles = 5000000
    MinMarketSize = 0.1
    StartupWealth = 0
    MinimumWealthForSurvival = 0 
    NumberOfPotentialEntrants = 40
    NumberOfPeriods = 10000
    MaxMagnituteOfTechChange = 8
    RateOfTechChange = 0.1
    PeriodStartOfTechChange = 2000
    InnovationCost = 100.0
    ImitationCost = 50.0
    InitialAttractionForResearch = 10
    InitialAttractionForNoResearch = 10
    InitialAttractionForInnovation = 10
    InitialAttractionForImitation = 10


    # System parameters
    LogLevel = {"Console": ["INFO"], "File": ["INFO", "DEBUG","TRACE"]}
    EnableProfiling = False


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