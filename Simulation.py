from Industry import Industry
from Parameters import Parameters
from Logger import Logger
from ExportToCSV import ExportToCSV
from Description import Description
import sys
import time

messages = ""
startTime = time.time()

Logger.info(sys.version_info)
Logger.info(Parameters.describe())
industry = Industry()

# Simulate
for x in range(Parameters.NumberOfPeriods):
    industry.nextPeriod()
    industry.processCurrentPeriod()
    Logger.debug(Description.describeAggregate(industry))
    Logger.trace(Description.describeIncumbentFirms(industry))

endTime = time.time()
Logger.info("Simulation completed in {:.2f} seconds".format(endTime - startTime))

# Save log
Logger.info("Saving log...")
Logger.saveLog()

# Save data
Logger.info("Saving data...")
ExportToCSV.export(industry.data)

