"""
Agent-based model based in Chang (2015), "Computational Industrial Economics: A generative approach to dynamic analysis in industrial organization". Additional features are described in my master thesis for Panthéon-Sorbonne MSc in Economics.

Author: João Dimas (joaohenriqueavila@gmail.com)
Supervisor: Prof. Angelo Secchi (Paris 1, PSE)

"""

from model.parameters import Parameters
from model.util.logger import Logger
from model.util.math import Math

class CrossSectionalData:

    def __init__(self, industry):
        self.industry = industry
        self.period = industry.currentPeriod
        self.addData()

    @classmethod
    def getFirmFlatData(cls, firm):
        return [
                    firm.firmId,
                    firm.industry.currentPeriod,
                    firm.age,
                    firm.status.value,
                    firm.industry.demand.eqPrice,
                    firm.closestTech.techId,
                    1 - (firm.techDistToOptimal / Parameters.NumberOfTasks),
                    firm.MC,
                    firm.marketShare,
                    firm.investmentInResearch,
                    1 if firm.innovating or firm.imitating else 0,
                    1 if firm.innovating else 0,
                    1 if firm.imitating else 0,
                    firm.attractionToResearch,
                    firm.attractionToNotResearch,
                    firm.attractionToInnovate,
                    firm.attractionToImitate,
                    firm.wealth,
                    firm.prevWealth,
                    firm.profits,
                    firm.prevProfits,
                    firm.output,
                    firm.prevOutput,
                    firm.revenues,
                    firm.prevRevenues,
                    firm.technology.tasks,
                    sum([tech.magnitudeOfChange for tech in firm.industry.currentOptimalTechs]) / len(firm.industry.currentOptimalTechs),
                    firm.industry.degreeOfTechDiv,
                    firm.industry.demand.marketSize,
                    firm.industry.demand.meanMarketSize
                ]

    def addData(self):
            self.data = [CrossSectionalData.getHeader()]

            for firm in sorted(self.industry.incumbentFirms, key=lambda firm: firm.firmId):
                assert Math.isEquivalent(firm.profits, firm.wealth - firm.prevWealth)
                self.data.append(CrossSectionalData.getFirmFlatData(firm))

            assert len(self.data) == len(self.industry.incumbentFirms) + 1

    @classmethod
    def getHeader(cls):
        return [
            "firm_id",
            "period",
            "age",
            "status",
            "price",
            "closer_tech",
            "prox_opt_tech",
            "mc",
            "mkt_share",
            "inv_res",
            "researching",
            "innovating",
            "imitating",
            "attraction_res",
            "attraction_not_res",
            "attraction_inn",
            "attraction_imi",
            "wealth",
            "previous_wealth",
            "profits",
            "previous_profits",
            "output",
            "previous_output",
            "revenues",
            "previous_revenues",
            "technology",
            "mag_tech_shock",
            "deg_tech_div",
            "mkt_size",
            "mean_mkt_size"
        ]

    def getFlatData(self):
        return self.data

class MultiCrossSectionalData:

    def __init__(self, industry):
        self.periods = []
        self.industry = industry

    def storeCurrentPeriod(self):
        if self.industry.currentPeriod in Parameters.PeriodsToSaveCrossSectionalData:
            Logger.debug("Storing current period {:d}. Incumbent firms: {:d}", (self.industry.currentPeriod, len(self.industry.incumbentFirms)), self.industry)
            self.periods.append(CrossSectionalData(self.industry))


