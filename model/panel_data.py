"""
Agent-based model based in Chang (2015), "Computational Industrial Economics: A generative approach to dynamic analysis in industrial organization". Additional features are described in my master thesis for Panthéon-Sorbonne MSc in Economics.

Author: João Dimas (joaohenriqueavila@gmail.com)
Supervisor: Prof. Angelo Secchi (Paris 1, PSE)

"""

from model.parameters import Parameters
from model.crosssectional_data import CrossSectionalData


class PanelData:

    def __init__(self, industry):
        self.firms = None
        self.periods = None
        self.industry = industry

    def storeCurrentPeriod(self):

        if Parameters.PeriodRangeToSavePanelData is not None and len(Parameters.PeriodRangeToSavePanelData) == 2 and Parameters.PeriodRangeToSavePanelData[0] <= self.industry.currentPeriod <= Parameters.PeriodRangeToSavePanelData[1]:

            if self.firms is None:
                self.firms = []
                for firm in self.industry.incumbentFirms:
                    self.firms.append(firm.firmId)

            if self.periods is None:
                self.periods = []

            periodData = []
            for firm in self.industry.incumbentFirms:
                if firm.firmId not in self.firms:
                    continue

                periodData.append(CrossSectionalData.getFirmFlatData(firm))

            self.periods.append(periodData)

    def getFlatData(self):
        if self.periods is None:
            return None

        flatData = [CrossSectionalData.getHeader()]
        lastPeriod = self.periods[-1]

        for firmA in sorted(lastPeriod, key=lambda firm: firm[0]):
            for periodData in self.periods:
                firmData = [firmB for firmB in periodData if firmB[0] == firmA[0]]
                flatData.extend(firmData)

        return flatData

