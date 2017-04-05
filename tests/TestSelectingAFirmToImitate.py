import unittest, datetime
from model.Firm import Firm
from model.Industry import Industry
from model.Technology import Technology
from model.util.Logger import Logger

class TestSelectingAFirmToImitate(unittest.TestCase):

    def test_if_right_competitor_is_selected_to_be_imitated(self):
        # Parameters
        numberOfOtherCompetitors = 41

        industry = Industry(1)
        industry.profitableFirmsPrevPeriod = []
        sumOfProfits = 0
        for firmId in range(1, numberOfOtherCompetitors + 1):
            firm = Firm(firmId, industry, Technology.generateRandomTechnology())
            firm.profits = firmId * 100
            sumOfProfits += firm.profits
            # sumOfProfits is 1*100 + 2*100 + 3*100 + ... + numberOfFirms*100
            # Or: 100 * (numberOfFirms + 1) * numberOFFirms / 2. In case of 41 firms, sumOfProfits = 86,100
            # Expected point in CDF after each loop:
            # 1) 100/86100 = .00116144
            # 2) 100/86100 + 200/86100 = 300/86100 = .003484321
            # ...
            # 11) 6600/86100 = .076655052 
            # ...
            # 21) 23100/86100 = .268292683
            # ...
            # 30) 46500/86100 = .540069686
            # 31) 49600/86100 = .576074332 <----- Selected competitor
            # ...
            # 41) 86100/86100 = 1

            industry.profitableFirmsPrevPeriod.append(firm)

        firmA = Firm(numberOfOtherCompetitors+1, industry, Technology.generateRandomTechnology())
        industry.profitableFirmsPrevPeriod.append(firmA)

        for competitorToBeSelected in range(1, numberOfOtherCompetitors+1):
            pointInCDFBefore = 100 * (competitorToBeSelected) * (competitorToBeSelected - 1) / 2 / sumOfProfits
            pointInCDFAfter = 100 * (competitorToBeSelected + 1) * competitorToBeSelected / 2 / sumOfProfits
            middlePoint = (pointInCDFAfter + pointInCDFBefore) / 2
            firmB = firmA.selectCompetitorFromRouletteWheel(middlePoint)
            self.assertIsNotNone(firmB)
            self.assertEqual(firmB.firmId, competitorToBeSelected)

    def setUp(self):
        timestamp = datetime.datetime.now()
        Logger.initialize(timestamp)