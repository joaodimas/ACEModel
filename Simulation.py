#!/usr/bin/env python3

import sys, time, cProfile, io, pstats, datetime, threading
from Logger import Logger
from Industry import Industry
from Parameters import Parameters
from ExportToCSV import ExportToCSV
from Description import Description
from AggregateData import MultiAggregateData

class IndustrySimulation:

    @classmethod
    def simulate(cls, number):
        global multiAggregateData
        global timestamp
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
        Logger.info("[SIM {:d}] Saving...\n", number)
        ExportToCSV.export(industry.data, timestamp, number)
        multiAggregateData.addData(industry.data)

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
    
    threads = []
    for x in range(Parameters.NumberOfSimulations):
        threads.append(threading.Thread(target=IndustrySimulation.simulate, args=[x + 1]))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

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
      

