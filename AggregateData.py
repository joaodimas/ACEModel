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
                    ["period", "entries", "exits", "surviv", "entryrate", "exitrate", "survivrate", "firms", "hindex", "div", "maxage", "minage", "avgage", "actfirms", "inactfirms", "wmc", "avgproxopt", "price", "totoutput", "avgoutput", "magtechshock"]
                 ]
        for period in self.periods:
            result.append(period.getFlatData())

        return result

class PeriodData:

    def __init__(self, industry):
        self.period = industry.currentPeriod
        self.entries = industry.nmbEnteringFirms
        self.exits = industry.nmbExitingFirms   
        self.survivorsFromThisPeriod = len(industry.incumbentFirms) - industry.nmbExitingFirms
        self.entryRate = industry.entryRate
        self.exitRate = industry.exitRate
        self.survivRate = 1 - industry.exitRate
        self.incumbents = len(industry.incumbentFirms)
        self.hIndex = industry.hIndex
        self.div = industry.degreeOfTechDiv
        self.oldestAge = industry.oldestAge
        self.youngestAge = industry.youngestAge
        self.averageAge = industry.averageAge
        self.activeIncumbents = len(industry.activeIncumbentFirms)
        self.inactiveIncumbents = len(industry.inactiveIncumbentFirms)
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
                    self.survivorsFromThisPeriod,
                    self.entryRate,
                    self.exitRate,
                    self.survivRate,
                    self.incumbents,
                    self.hIndex,
                    self.div,
                    self.oldestAge,
                    self.youngestAge,
                    self.averageAge,
                    self.activeIncumbents,
                    self.inactiveIncumbents,
                    self.weightedMC,
                    self.averageProximityToOptimalTech,
                    self.price,
                    self.industryOutput,
                    self.averageOutput,
                    self.magtechshock
                 ]



