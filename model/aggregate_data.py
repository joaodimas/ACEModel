from model.parameters import Parameters

class AggregateData:
    def __init__(self, industry):
        self.parameters = Parameters.getParameters()
        self.periods = []
        self.industry = industry

    def storeCurrentPeriod(self):
        self.periods.append(PeriodData(self.industry)) 

    def getHeader(self):
        return [
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
                    "totinninv",
                    "totimiinv",
                    "costshareinn",
                    "firmsres",
                    "firmsinn",
                    "firmsimi",
                    "hindex",
                    "div",
                    "gini",
                    "pcm",
                    "cs",
                    "totprofits",
                    "ts",
                    "maxage",
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

    def getFlatData(self):
        if hasattr(self, "flatData") and len(self.flatData) > 0:
            return self.flatData

        result = []
        result.append(self.getHeader())
        for period in self.periods:
            result.append(period.getFlatData())

        self.flatData = result
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
        self.totalInnovationInvestment = industry.totalInvestmentInInnovation
        self.totalImitationInvestment = industry.totalInvestmentInImitation
        self.costShareOfInnovation = (industry.totalInvestmentInInnovation / industry.totalInvestmentInResearch) if industry.totalInvestmentInResearch > 0 else 0
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
        self.activeIncumbents = len(industry.activeFirms)
        self.inactiveIncumbents = len(industry.inactiveFirms)
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
                    self.totalInnovationInvestment,
                    self.totalImitationInvestment,
                    self.costShareOfInnovation,
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

class MultiAggregateData:
    def __init__(self):
        self.listOfSimulations = []
        self.nmbSimulations = 0

    def addListOfResults(self, listOfResults):
        for result in listOfResults:
            self.addFlatData(result)

    def addData(self, data):
        self.listOfSimulations.append(data.flatData)
        self.nmbSimulations += 1

    def addFlatData(self, flatData):
        self.listOfSimulations.append(flatData)
        self.nmbSimulations += 1

    def getFlatData(self):
        result = []
        header = self.listOfSimulations[0][0]
        nmbVariables = len(header)
        result.append(header)
        for p in range(1, Parameters.TimeHorizon + 1): # Periods
            period = []
            for v in range(nmbVariables): # Variables
                period.append(self.getAverage(p, v))
            result.append(period)

        return result

    def getAverage(self, period, variable):    
        sum = 0

        for simulation in self.listOfSimulations:
            sum += simulation[period][variable]

        return sum / self.nmbSimulations
        

