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
                    [
                        "period",
                        "mktsize",
                        "entries",
                        "exits",
                        "surviv",
                        "entryrate",
                        "exitrate",
                        "survivrate",
                        "firms",
                        "totresinv",
                        "firmsres",
                        "firmsinn",
                        "firmsimi",
                        "hindex",
                        "div",
                        "gini",
                        "pcm",
                        "cs",
                        "totprofits",
                        "ts","maxage",
                        "minage",
                        "avgage",
                        "actfirms",
                        "inactfirms",
                        "profitablefirms",
                        "wmc",
                        "avgproxopt",
                        "price",
                        "totoutput",
                        "avgoutput",
                        "magtechshock"
                    ]
                 ]
        for period in self.periods:
            result.append(period.getFlatData())

        return result

class PeriodData:

    def __init__(self, industry):
        self.period = industry.currentPeriod
        self.mktsize = industry.demand.marketSize
        self.entries = industry.nmbEnteringFirms
        self.exits = industry.nmbExitingFirms  
        self.survivorsFromThisPeriod = len(industry.incumbentFirms) - industry.nmbExitingFirms
        self.entryRate = industry.entryRate
        self.exitRate = industry.exitRate
        self.survivRate = 1 - industry.exitRate
        self.incumbents = len(industry.incumbentFirms)
        self.totalResearchInvestment = industry.totalInvestmentInResearch
        self.firmsResearching = industry.nmbResearching
        self.firmsInnovating = industry.nmbInnovating
        self.firmsImitating = industry.nmbImitating
        self.HIndex = industry.HIndex
        self.div = industry.degreeOfTechDiv
        self.gini = industry.gini
        self.PCM = industry.PCM
        self.CS = industry.CS
        self.totalProfits = industry.totalProfits
        self.TS = industry.TS
        self.oldestAge = industry.oldestAge
        self.youngestAge = industry.youngestAge
        self.averageAge = industry.averageAge
        self.activeIncumbents = len(industry.activeIncumbentFirms)
        self.inactiveIncumbents = len(industry.inactiveIncumbentFirms)
        self.profitableFirms = industry.nmbProfitableFirms 
        self.weightedMC = industry.weightedMC
        self.averageProximityToOptimalTech = industry.averageProximityToOptimalTech
        self.price = industry.demand.eqPrice
        self.industryOutput = industry.industryOutput
        self.averageOutput = self.industryOutput / self.activeIncumbents if self.activeIncumbents != 0 else 0
        self.magtechshock = industry.currentOptimalTech.magnitudeOfChange

    def getFlatData(self):
        return [
                    self.period,
                    self.mktsize,
                    self.entries,
                    self.exits,
                    self.survivorsFromThisPeriod,
                    self.entryRate,
                    self.exitRate,
                    self.survivRate,
                    self.incumbents,
                    self.totalResearchInvestment,
                    self.firmsResearching,
                    self.firmsInnovating,
                    self.firmsImitating,
                    self.HIndex,
                    self.div,
                    self.gini,
                    self.PCM,
                    self.CS,
                    self.totalProfits,
                    self.TS,
                    self.oldestAge,
                    self.youngestAge,
                    self.averageAge,
                    self.activeIncumbents,
                    self.inactiveIncumbents,
                    self.profitableFirms,
                    self.weightedMC,
                    self.averageProximityToOptimalTech,
                    self.price,
                    self.industryOutput,
                    self.averageOutput,
                    self.magtechshock
                 ]



