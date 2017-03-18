from Industry import Industry
from Parameters import Parameters
from Logger import Logger
from ExportToCSV import ExportToCSV
from Description import Description
import sys
import time

messages = ""
startTime = time.time()

Logger.log(sys.version_info)
Logger.log(Parameters.describe())
industry = Industry()

# Simulate
for x in range(Parameters.NumberOfPeriods):
    industry.nextPeriod()
    industry.processCurrentPeriod()
    Logger.log(Description.describeIndustry(industry))

endTime = time.time()
Logger.log("Simulation completed in {:.2f} seconds".format(endTime - startTime))

# Save log
Logger.debug("Saving log...")
Logger.saveLog()

# Save data
Logger.debug("Saving data...")
ExportToCSV.export(industry.data)

