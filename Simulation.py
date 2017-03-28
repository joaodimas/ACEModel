import sys, time, cProfile, io, pstats, datetime
from Logger import Logger
from Industry import Industry
from Parameters import Parameters
from ExportToCSV import ExportToCSV
from Description import Description
from AggregateData import MultiAggregateData

pr = None
if(Parameters.EnableProfiling):
    pr = cProfile.Profile()
    pr.enable()

timestamp = datetime.datetime.now()
aggregateStartTime = time.time()
Logger.initialize(timestamp)
Logger.info(sys.version_info)
Logger.info(Parameters.describe())

try:
    multiAggregateData = MultiAggregateData()
    Logger.info("Executing {:d} simulations\n", Parameters.NumberOfSimulations)
    for x in range(Parameters.NumberOfSimulations):
        Logger.info("STARTING SIMULATION {:d}", x + 1)
        simulationStartTime = time.time()
        industry = Industry()

        # Simulate
        for p in range(Parameters.TimeHorizon):
            industry.processPeriod()
            if(Logger.isEnabledForDebug()):
                Logger.debug(Description.describeAggregate(industry))
            if(Logger.isEnabledForTrace()):
                Logger.trace(Description.describeIncumbentFirms(industry))

        simulationEndTime = time.time()

        Logger.info("Simulation {:d} completed in {:.2f} seconds", (x + 1, simulationEndTime - simulationStartTime))
        Logger.info("Saving...\n")
        ExportToCSV.export(industry.data, timestamp, x + 1)
        multiAggregateData.addData(industry.data)

    aggregateEndTime = time.time()
    Logger.info("All {:d} simulations completed in {:.2f} seconds", (x + 1, aggregateEndTime - aggregateStartTime))
    # Save data
    Logger.info("Saving data...")
    ExportToCSV.export(multiAggregateData, timestamp)

except:
    Logger.logger.exception("Error")

if(Parameters.EnableProfiling):
    pr.disable()
    with io.StringIO() as s:
        ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
        ps.print_stats()
        Logger.info(s.getvalue())

