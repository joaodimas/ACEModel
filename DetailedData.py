from Parameters import Parameters
from Firm import FirmStatus
import json

class DetailedData:

    def __init__(self):
        self.parameters = Parameters.getParameters()
        self.periods = []

    def addPeriod(self, industry):
        self.periods.append(PeriodData(industry)) 

    def toJSON(self):
        return ("{"
                    "\"parameters\": " + json.dumps(self.parameters) + ", "
                    "\"periods\": "+ self.serializePeriods(self.periods) + "}"
                )

    def serializePeriods(self, periods):
        str = "["
        for i, p in enumerate(periods):
            str += p.toJSON()
            if i < len(periods) - 1:
                str += ","
        str += "]"
        return str

class PeriodData:

    def __init__(self, industry):
        self.period = industry.currentPeriod
        self.sumOfMC = industry.currentSumOfMC
        self.marketSize = industry.demand.marketSize
        self.activeIncumbentFirms = []
        self.inactiveIncumbentFirms = []
        self.enteringFirms = []
        self.exitingFirms = []

        
        for firm in industry.incumbentFirms:
            firmData = FirmData(firm)

            if firm.status == FirmStatus.ACTIVE_INCUMBENT:
                self.activeIncumbentFirms.append(firmData)
            if firm.status == FirmStatus.INACTIVE_INCUMBENT:
                self.inactiveIncumbentFirms.append(firmData)
            if firm.entering:
                self.enteringFirms.append(firmData)
            if firm.exiting:
                self.exitingFirms.append(firmData)

        self.nmbActiveIncumbentFirms = len(self.activeIncumbentFirms)
        self.nmbInactiveIncumbentFirms = len(self.inactiveIncumbentFirms)
        self.nmbEnteringFirms = len(self.enteringFirms)
        self.nmbExitingFirms = len(self.exitingFirms)
    
    def toJSON(self):
        return ("{"
                    "\"period\": " + str(self.period) + ", "
                    "\"sumOfMC\": " + str(self.currentActiveSumOfMC) + ", "
                    "\"marketSize\": " + str(self.marketSize) + ", "
                    "\"nmbActiveIncumbentFirms\": " + str(self.nmbActiveIncumbentFirms) + ", "
                    "\"nmbInactiveIncumbentFirms\": " + str(self.nmbInactiveIncumbentFirms) + ", "
                    "\"nmbEnteringFirms\": " + str(self.nmbEnteringFirms) + ", "
                    "\"nmbExitingFirms\": " + str(self.nmbExitingFirms) + ", "
                    "\"activeIncumbentFirms\": " + self.serializeFirms(self.activeIncumbentFirms) + ", "
                    "\"inactiveIncumbentFirms\": " + self.serializeFirms(self.inactiveIncumbentFirms) + ", "
                    "\"enteringFirms\": " + self.serializeFirms(self.enteringFirms) + ", "
                    "\"exitingFirms\": " + self.serializeFirms(self.exitingFirms) + ", "
                )

    def serializeFirms(self, firms):
        str = "["
        for i, f in enumerate(firms):
            str += f.toJSON()
            if i < len(firms) - 1:
                str += ","
        str += "]"
        return str

class FirmData:

    def __init__(self, firm):
        self.firmId = firm.firmId
        self.status = firm.status
        self.wealthAfter = firm.wealth
        self.wealthBefore = firm.prevWealth
        self.techDistToOptimal = firm.techDistToOptimal 
        self.MC = firm.MC
        self.output = firm.output
        self.profits = firm.profits
        self.expProfits = firm.expProfits
        self.expWealthAfter = firm.prevWealth + firm.expProfits
        self.entering = firm.entering
        self.exiting = firm.exiting

    def toJSON(self):
        return ("{"
                    "\"firmId\": " + str(self.firmId) + ", "
                    "\"status\": \"" + self.status.name + "\", "
                    "\"wealthAfter\": " + str(self.wealthAfter) + ", "
                    "\"wealthBefore\": " + str(self.wealthBefore) + ", "
                    "\"techDistToOptimal\": \"" + str(self.techDistToOptimal) + "\", "
                    "\"MC\": " + str(self.MC) + ", "
                    "\"output\": \"" + str(self.output) + "\", "
                    "\"profits\": " + str(self.profits) + ", "
                    "\"expProfits\": \"" + str(self.expProfits) + "\", "
                    "\"expWealthAfter\": \"" + str(self.expWealthAfter) + "\", "
                    "\"entering\": \"" + str(self.entering) + "\", "
                    "\"exiting\": \"" + str(self.exiting) + "\"}"
                )