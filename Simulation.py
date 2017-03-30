#!/usr/bin/env python3

import sys, time, cProfile, io, pstats, datetime, multiprocessing
from Logger import Logger
from Industry import Industry
from Parameters import Parameters
from ExportToCSV import ExportToCSV
from Description import Description
from AggregateData import MultiAggregateData

class IndustrySimulation:

    @classmethod
    def simulate(cls, timestamp, number, child_conn):
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
        child_conn.send(industry.data.flatData)

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
    pipes = []
    for x in range(Parameters.NumberOfSimulations):
        parent_conn, child_conn = multiprocessing.Pipe()
        pipes.append(parent_conn)
        threads.append(multiprocessing.Process(target=IndustrySimulation.simulate, args=(timestamp, x + 1, child_conn)))

    for t in threads:
        t.start()

    for parent_conn in pipes:
        multiAggregateData.addFlatData(parent_conn.recv())

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
      

