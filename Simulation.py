import sys, time, cProfile, io, pstats, datetime
from Logger import Logger
from Industry import Industry
from Parameters import Parameters
from ExportToCSV import ExportToCSV
from Description import Description

pr = None
if(Parameters.EnableProfiling):
    pr = cProfile.Profile()
    pr.enable()

timestamp = datetime.datetime.now()
startTime = time.time()

Logger.initialize(timestamp)
Logger.info(sys.version_info)
Logger.info(Parameters.describe())

try:
    industry = Industry()

    # Simulate
    for x in range(Parameters.NumberOfPeriods):
        industry.processPeriod()
        if(Logger.isEnabledForDebug()):
            Logger.debug(Description.describeAggregate(industry))
        if(Logger.isEnabledForTrace()):
            Logger.trace(Description.describeIncumbentFirms(industry))

    endTime = time.time()

    Logger.info("Simulation completed in {:.2f} seconds", endTime - startTime)

    # Save data
    Logger.info("Saving data...")
    ExportToCSV.export(industry.data, timestamp)

except:
    Logger.logger.exception("Error")

if(Parameters.EnableProfiling):
    pr.disable()
    with io.StringIO() as s:
        ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
        ps.print_stats()
        Logger.info(s.getvalue())

