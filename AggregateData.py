from Parameters import Parameters

class AggregateData:
    def __init__(self, industry):
        self.parameters = Parameters.getParameters()
        self.periods = []
        self.industry = industry

    def storeCurrentPeriod(self):
        self.periods.append(PeriodData(self.industry)) 

    def getFlatData(self):
        result = [
                    # header
                    ["period", "entries", "exits", "firms", "maxage", "minage", "avgage", "actfirms", "inactfirms", "surviv", "wmc", "avgproxopt", "price", "totoutput", "avgoutput", "magtechshock"]
                 ]
        for period in self.periods:
            result.append(period.getFlatData())

        return result

class PeriodData:

    def __init__(self, industry):
        self.period = industry.currentPeriod
        self.entries = industry.nmbEnteringFirms
        self.exits = industry.nmbExitingFirms       
        self.incumbents = len(industry.incumbentFirms)
        self.oldestAge = industry.oldestAge
        self.youngestAge = industry.youngestAge
        self.averageAge = industry.averageAge
        self.activeIncumbents = len(industry.activeIncumbentFirms)
        self.inactiveIncumbents = len(industry.inactiveIncumbentFirms)
        self.survivorsFromThisPeriod = self.incumbents - industry.nmbExitingFirms
        self.weightedMC = industry.weightedMC
        self.averageProximityToOptimalTech = 1 - (industry.currentActiveSumOfMC / self.activeIncumbents / 100) if self.activeIncumbents != 0 else 0
        self.price = industry.demand.eqPrice
        self.industryOutput = industry.industryOutput
        self.averageOutput = self.industryOutput / self.activeIncumbents if self.activeIncumbents != 0 else 0
        self.magtechshock = industry.currentOptimalTech.magnitudeOfChange

    def getFlatData(self):
        return [
                    self.period,
                    self.entries,
                    self.exits,
                    self.incumbents,
                    self.oldestAge,
                    self.youngestAge,
                    self.averageAge,
                    self.activeIncumbents,
                    self.inactiveIncumbents,
                    self.survivorsFromThisPeriod,
                    self.weightedMC,
                    self.averageProximityToOptimalTech,
                    self.price,
                    self.industryOutput,
                    self.averageOutput,
                    self.magtechshock
                 ]



