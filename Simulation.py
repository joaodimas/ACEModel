#!/usr/bin/env python3

import sys, time, cProfile, io, pstats, datetime, multiprocessing
from Logger import Logger
from Industry import Industry
from Parameters import Parameters
from ExportToCSV import ExportToCSV
from Description import Description
from AggregateData import MultiAggregateData


def worker(resultQueue, timestamp, number):
    Logger.info("[SIM {:d}] STARTING SIMULATION", number)
    simulationStartTime = time.time()

    industry = Industry(number)

    # Simulate
    for p in range(Parameters.TimeHorizon):
        industry.processPeriod()
        if(Logger.isEnabledForDebug()):
            Logger.debug(Description.describeAggregate(industry))
        if(Logger.isEnabledForTrace()):
            Logger.trace(Description.describeIncumbentFirms(industry))  
    
    simulationEndTime = time.time()

    Logger.info("[SIM {:d}] Simulation completed in {:.2f} seconds", (number, simulationEndTime - simulationStartTime))
    Logger.info("[SIM {:d}] Saving...", number)
    ExportToCSV.export(industry.data, timestamp, number)
    resultQueue.put((number, industry.data.flatData))
    Logger.info("[SIM {:d}] Result sent to pipe.\n", number)

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
    
    processes = []
    resultQueue = multiprocessing.Queue()
    for x in range(Parameters.NumberOfSimulations):
        process = multiprocessing.Process(target=worker, args=(resultQueue, timestamp, x + 1))
        processes.append(process)
        process.start()

    for x in range(Parameters.NumberOfSimulations):
        result = resultQueue.get()
        Logger.info("[SIM {:d}] Result received from queue by main process.", result[0])
        multiAggregateData.addFlatData(result[1])

    for p in processes:
        p.join()

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
      

