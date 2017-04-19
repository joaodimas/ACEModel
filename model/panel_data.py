from model.parameters import Parameters


class PanelData:

    def __init__(self, industry):
        self.firms = None
        self.periods = []
        self.industry = industry

    def storeCurrentPeriod(self):

        if Parameters.PeriodRangeToSavePanelData is not None and len(Parameters.PeriodRangeToSavePanelData) == 2 and Parameters.PeriodRangeToSavePanelData[0] <= self.industry.currentPeriod <= Parameters.PeriodRangeToSavePanelData[1]:

            if self.firms is None:
                self.firms = []
                for firm in self.industry.incumbentFirms:
                    self.firms.append(firm.firmId)

            periodData = []
            for firm in self.industry.incumbentFirms:
                if firm.firmId not in self.firms:
                    continue

                periodData.append([
                    firm.firmId,
                    self.industry.currentPeriod,
                    firm.age,
                    firm.status.value,
                    self.industry.demand.eqPrice,
                    1 - (firm.techDistToOptimal / Parameters.NumberOfTasks),
                    firm.MC,
                    firm.marketShare,
                    firm.investmentInResearch,
                    1 if firm.innovating or firm.imitating else 0,
                    1 if firm.innovating else 0,
                    1 if firm.imitating else 0,
                    firm.attractionForResearch,
                    firm.attractionForNoResearch,
                    firm.attractionForInnovation,
                    firm.attractionForImitation,
                    firm.wealth,
                    firm.prevWealth,
                    firm.profits,
                    firm.prevProfits,
                    (firm.profits / firm.prevProfits - 1) if firm.prevProfits > 0 and firm.profits > 0 else 0,
                    firm.output,
                    firm.prevOutput,
                    (firm.output / firm.prevOutput - 1) if firm.prevOutput > 0 else 0,
                    firm.revenues,
                    firm.prevRevenues,
                    (firm.revenues / firm.prevRevenues - 1) if firm.prevRevenues > 0 else 0,
                    (firm.industry.demand.eqPrice - firm.MC) / firm.industry.demand.eqPrice
                ])

            self.periods.append(periodData)

    def getFlatData(self):
        if self.periods is None:
            return None

        flatData = [self.getHeader()]
        lastPeriod = self.periods[-1]

        for firmA in sorted(lastPeriod, key=lambda firm: firm[0]):
            for periodData in self.periods:
                firmData = [firmB for firmB in periodData if firmB[0] == firmA[0]]
                flatData.extend(firmData)

        return flatData

    def getHeader(self):
        return [
            "firm_id",
            "period",
            "age",
            "status",
            "price",
            "prox_opt_tech",
            "mc",
            "mkt_share",
            "inv_res",
            "researching",
            "innovating",
            "imitating",
            "attraction_res",
            "attraction_no_res",
            "attraction_inn",
            "attraction_imi",
            "wealth",
            "previous_wealth",
            "profits",
            "previous_profits",
            "profits_growthrate",
            "output",
            "previous_output",
            "output_growthrate",
            "revenues",
            "previous_revenues",
            "revenues_growthrate",
            "pcm"
        ]

