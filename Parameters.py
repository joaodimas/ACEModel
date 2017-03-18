class Parameters:

    # Model parameters
    NumberOfTasks = 96
    FixedCost = 200
    DemandIntercept = 300
    InitialMarketSize = 4
    StartupWealth = 0
    MinimumWealthForSurvival = 0 
    NumberOfPotentialEntrants = 40
    NumberOfPeriods = 100
    MaxMagnituteOfTechChange = 8
    RateOfTechChange = 0.1
    PeriodStartOfTechChange = 3000

    # System parameters
    DataPath = "/Users/jdimas/GitHub/ACEModel/data"

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
                    "InitialMarketSize: " + self.InitialMarketSize + ", "
                    "MinimumWealthForSurvival: " + self.MinimumWealthForSurvival + ", "
                    "NumberOfFirms: " + self.NumberOfFirms + ", "
                    "NumberOfPeriods: " + self.NumberOfPeriods + "}"                   
               )