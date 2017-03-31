from Parameters import Parameters    

class Description:
    @classmethod
    def describeAggregate(cls, industry):
        desc = (
                    "\n[SIMULATION {:d}][PERIOD {:d}]\n"
                    "INDUSTRY RESULTS\n"
                    "Survivors from previous period: {:d}\n"
                    "New entrants in this period: {:d}\n"
                    "Firms in the market: {:d}\n"
                    "Age of oldest firm: {:d}\n"
                    "Age of youngest firm: {:d}\n"
                    "Average age: {:.1f}\n"
                    "Active firms: {:d}\n"
                    "Inactive firms: {:d}\n"
                    "Exiting firms after this period: {:d}\n"
                    "Survivors from this period: {:d}\n"
                    "Weighted marginal cost: {:.2f}\n"
                    "Average proximity to optimal tech: {:.2%}\n"
                    "DIV: {:.2f}\n"
                    "Price: {:.2f}\n"
                    "Total investment in R&D: {:.2f}\n"
                    "Total investment in Innovation: {:.2f}\n"
                    "Total investment in Imitation: {:.2f}\n"
                    "Cost share of innovation: {:.2%}\n"
                    "Profitable firms: {:d}\n"
                    "Avg PCM: {:.2f}\n"
                    "Market size: {:.2f}\n"
                    "Industry output: {:.2f}\n"
                    "Average output: {:.2f}\n"
                ).format(
                            industry.simulation,
                            industry.currentPeriod, 
                            len(industry.survivorsOfPreviousPeriod), 
                            industry.nmbEnteringFirms, 
                            len(industry.incumbentFirms), 
                            industry.oldestAge, 
                            industry.youngestAge, 
                            industry.averageAge, 
                            len(industry.activeIncumbentFirms), 
                            len(industry.incumbentFirms) - len(industry.activeIncumbentFirms), 
                            industry.nmbExitingFirms, 
                            len(industry.incumbentFirms) - industry.nmbExitingFirms, 
                            industry.weightedMC, 
                            1 - (industry.currentActiveSumOfMC / len(industry.activeIncumbentFirms) / 100) if len(industry.activeIncumbentFirms) != 0 else 0, 
                            industry.degreeOfTechDiv,
                            industry.demand.eqPrice, 
                            industry.totalInvestmentInResearch,
                            industry.totalInvestmentInInnovation,
                            industry.totalInvestmentInImitation,
                            (industry.totalInvestmentInInnovation / industry.totalInvestmentInResearch) if industry.totalInvestmentInResearch > 0 else 0,
                            industry.nmbProfitableFirms,
                            industry.PCM,
                            industry.demand.marketSize,
                            industry.industryOutput, 
                            industry.industryOutput / len(industry.activeIncumbentFirms) if len(industry.activeIncumbentFirms) != 0 else 0
                        )

        return desc

    @classmethod
    def describeIncumbentFirms(cls, industry):
        desc = ""
        desc += cls.describeActiveIncumbentFirms(industry)
        desc += cls.describeInactiveIncumbentFirms(industry)
        return desc

    @classmethod
    def describeActiveIncumbentFirms(cls, industry):
        desc = "---------------------\nACTIVE FIRMS IN PERIOD {:d}:\n".format(industry.currentPeriod)
        for firm in sorted(industry.activeIncumbentFirms, key=lambda firm: firm.wealth, reverse= True):
            desc += cls.describeFirm(firm)
        return desc

    @classmethod
    def describeInactiveIncumbentFirms(cls, industry):
        desc = "---------------------\nINACTIVE FIRMS IN PERIOD {:d}:\n".format(industry.currentPeriod)
        for firm in sorted(industry.inactiveIncumbentFirms, key=lambda firm: firm.wealth, reverse= True):
            desc += cls.describeFirm(firm)
        return desc    

    @classmethod
    def describeFirm(cls, firm):
        desc = ("[SIMULATION {:d}][PERIOD{:d}]\n"
                "FIRM {:d}\n"
                "Age: {:d}\n"
                "Status after this period: {}\n"
                "Wealth before this period: {:.2f}\n"
                "Wealth after this period: {:.2f}\n"
                "Hamming dist. to optimal: {:d}\n"
                "Proximity to optimal: {:.2%}\n"
                "MC: {:.2f}\n"
                "Output: {:.2f}\n"
                "Market share: {:.2%}\n"
                "Investment in R&D: {:.2f}\n"
                "Realized profits: {:.2f}\n"
                "Expected profits in this period: {:.2f}\n"
                "Expected wealth after this period: {:.2f}\n"
                ).format(firm.industry.simulation, firm.industry.currentPeriod, firm.firmId, firm.age, firm.status.name, firm.prevWealth, firm.wealth, firm.techDistToOptimal, 1 - (firm.techDistToOptimal / Parameters.NumberOfTasks), firm.MC, firm.output, firm.marketShare, firm.investmentInResearch, firm.profits, firm.expProfits, firm.prevWealth + firm.expProfits)
        return desc
