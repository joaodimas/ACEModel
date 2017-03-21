import sys, time, cProfile, io, pstats, os, datetime
from Logger import Logger
from Industry import Industry
from Parameters import Parameters
from ExportToCSV import ExportToCSV
from Description import Description
from Technology import Technology

pr = None
if(Parameters.EnableProfiling):
    pr = cProfile.Profile()
    pr.enable()

timestamp = datetime.datetime.now()
startTime = time.time()

Logger.initialize(timestamp)
Logger.info(sys.version_info)
Logger.info(Parameters.describe())

# for i in range(1,94):
#     techA = Technology(0b0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000)
#     techB = Technology(0b1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111)
#     techA.copyTask(techB, i)


try:
    industry = Industry()

    # Simulate
    for x in range(Parameters.NumberOfPeriods):
        industry.processPeriod()
        Logger.debug(Description.describeAggregate(industry))
        Logger.trace(Description.describeIncumbentFirms(industry))

    endTime = time.time()

    Logger.info("Simulation completed in {:.2f} seconds".format(endTime - startTime))

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

