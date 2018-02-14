"""
Agent-based model based in Chang (2015), "Computational Industrial Economics: A generative approach to dynamic analysis in industrial organization". Additional features are described in my master thesis for Panthéon-Sorbonne MSc in Economics.

Author: João Dimas (joaohenriqueavila@gmail.com)
Supervisor: Prof. Angelo Secchi (Paris 1, PSE)

"""

from model.parameters import Parameters
from model.util.logger import Logger

class Description:

    @classmethod
    def describe(cls, industry):
        cls.describeAggregate(industry)
        cls.describeActiveIncumbentFirms(industry)
        cls.describeInactiveFirms(industry)

    @classmethod
    def describeAggregate(cls, industry):
        Logger.trace("", industry=industry)
        Logger.debug("--------------------- PERIOD RESULTS ---------------------", industry=industry)
        Logger.debug("Survivors from previous period: {:d}", (len(industry.survivorsOfPreviousPeriod)), industry=industry)
        Logger.debug("New entrants in this period: {:d}", (industry.nmbEnteringFirms), industry=industry)
        Logger.debug("Firms in the market: {:d}", (len(industry.incumbentFirms)), industry=industry)
        Logger.debug("Age of oldest firm: {:d}", (industry.oldestAge), industry=industry)
        Logger.debug("Age of youngest firm: {:d}", (industry.youngestAge), industry=industry)
        Logger.debug("Average age: {:.1f}", (industry.averageAge), industry=industry)
        Logger.debug("Active firms: {:d}", (len(industry.activeFirms)), industry=industry)
        Logger.debug("Inactive firms: {:d}", (len(industry.incumbentFirms) - len(industry.activeFirms)), industry=industry)
        Logger.debug("Exiting firms after this period: {:d}", (industry.nmbExitingFirms), industry=industry)
        Logger.debug("Survivors after this period: {:d}", (len(industry.incumbentFirms) - industry.nmbExitingFirms), industry=industry)
        Logger.debug("Weighted marginal cost: {:.2f}", (industry.weightedMC), industry=industry)
        Logger.debug("Average proximity to optimal tech: {:.2%}", (industry.averageProximityToOptimalTech), industry=industry)
        Logger.debug("DIV: {:.3f}", (industry.degreeOfTechDiv), industry=industry)
        Logger.debug("Price: {:.2f}", (industry.demand.eqPrice), industry=industry)
        Logger.debug("Total investment in R&D: {:.2f}", (industry.totalInvestmentInResearch), industry=industry)
        Logger.debug("Total investment in Innovation: {:.2f}", (industry.totalInvestmentInInnovation), industry=industry)
        Logger.debug("Total investment in Imitation: {:.2f}", (industry.totalInvestmentInImitation), industry=industry)
        Logger.debug("Cost share of innovation: {:.2%}", ((industry.totalInvestmentInInnovation / industry.totalInvestmentInResearch) if industry.totalInvestmentInResearch > 0 else 0), industry=industry)
        Logger.debug("Profitable firms: {:d}", (industry.nmbProfitableFirms), industry=industry)
        Logger.debug("Avg PCM: {:.2f}", (industry.PCM), industry=industry)
        Logger.debug("Market size: {:.2f}", (industry.demand.marketSize), industry=industry)
        Logger.debug("Industry output: {:.2f}", (industry.industryOutput), industry=industry)
        Logger.debug("Average output: {:.2f}", (industry.industryOutput / len(industry.activeFirms) if len(industry.activeFirms) != 0 else 0), industry=industry)
        Logger.debug("Average magnitude of technological shock: {:.2f}", (sum([tech.magnitudeOfChange for tech in industry.currentOptimalTechs]) / len(industry.currentOptimalTechs)), industry=industry)
        Logger.debug("Number of optimal technologies: {:d}", (len(industry.currentOptimalTechs)), industry=industry)
        for tech in industry.currentOptimalTechs:
            Logger.debug("Magnitude of shock in Tech {:d}: {:d}", (tech.techId, tech.magnitudeOfChange), industry=industry)

    @classmethod
    def describeActiveIncumbentFirms(cls, industry):
        Logger.trace("", industry=industry)
        Logger.trace("------- Begin: ACTIVE FIRMS -------", industry=industry)
        for firm in sorted(industry.activeFirms, key=lambda firm: firm.wealth, reverse= True):
            cls.describeFirm(firm)
        Logger.trace("", industry=industry)
        Logger.trace("------- End: ACTIVE FIRMS -------", industry=industry)

    @classmethod
    def describeInactiveFirms(cls, industry):
        Logger.trace("", industry=industry)
        Logger.trace("------- Begin: INACTIVE FIRMS -------", industry=industry)
        for firm in sorted(industry.inactiveFirms, key=lambda firm: firm.wealth, reverse= True):
            cls.describeFirm(firm)
        Logger.trace("", industry=industry)            
        Logger.trace("------- End: INACTIVE FIRMS -------", industry=industry)

    @classmethod
    def describeFirm(cls, firm):
        Logger.trace("", industry=firm.industry)
        Logger.trace("FIRM {:d}", (firm.firmId), industry=firm.industry)
        Logger.trace("Age: {:d}", (firm.age), industry=firm.industry)
        Logger.trace("Status after this period: {}", (firm.status.name), industry=firm.industry)
        Logger.trace("Wealth before this period: {:.2f}", (firm.prevWealth), industry=firm.industry)
        Logger.trace("Wealth after this period: {:.2f}", (firm.wealth), industry=firm.industry)
        Logger.trace("Closest opt. tech.: {:d}", (firm.closestTech.techId), industry=firm.industry)
        Logger.trace("Tasks of closest tech: {:0{:d}b}", (firm.closestTech.tasks, Parameters.NumberOfTasks), industry=firm.industry)
        Logger.trace("Firm's tasks:          {:0{:d}b}", (firm.technology.tasks, Parameters.NumberOfTasks), industry=firm.industry)
        Logger.trace("Hamming dist. to optimal: {:d}", (firm.techDistToOptimal), industry=firm.industry)
        Logger.trace("Proximity to optimal: {:.2%}", (1 - (firm.techDistToOptimal / Parameters.NumberOfTasks)), industry=firm.industry)
        Logger.trace("MC: {:.2f}", (firm.MC), industry=firm.industry)
        Logger.trace("Output: {:.2f}", (firm.output), industry=firm.industry)
        Logger.trace("Market share: {:.2%}", (firm.marketShare), industry=firm.industry)
        Logger.trace("Investment in R&D: {:.2f}", (firm.investmentInResearch), industry=firm.industry)
        Logger.trace("Realized profits: {:.2f}", (firm.profits), industry=firm.industry)
        Logger.trace("PCM: {:.2f}", ((firm.industry.demand.eqPrice - firm.MC) / firm.industry.demand.eqPrice), industry=firm.industry)
        Logger.trace("Expected profits in this period: {:.2f}", (firm.expProfits), industry=firm.industry)
        Logger.trace("Expected wealth after this period: {:.2f}", (firm.prevWealth + firm.expProfits), industry=firm.industry)
        Logger.trace("Attraction to research: {:d}", (firm.attractionToResearch), industry=firm.industry)
        Logger.trace("Attraction to not research: {:d}", (firm.attractionToNotResearch), industry=firm.industry)
        Logger.trace("Attraction to innovate: {:d}", (firm.attractionToInnovate), industry=firm.industry)
        Logger.trace("Attraction to imitate: {:d}", (firm.attractionToImitate), industry=firm.industry)