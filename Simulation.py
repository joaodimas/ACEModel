#!/usr/bin/env python3

import sys, time, cProfile, io, pstats, datetime, multiprocessing, functools
from model import MultiAggregateData, Industry, Description, Parameters
from model.util import Logger, ExportToCSV


def runSimulation(index, timestamp):
    try:
        number = index + 1
        Logger.info("[SIM {:d}] STARTING SIMULATION", number)
        simulationStartTime = time.time()

        industry = Industry(number)

        # Simulate
        for p in range(Parameters.TimeHorizon):
            industry.processPeriod()
            Description.describe(industry)
        
        simulationEndTime = time.time()

        Logger.info("[SIM {:d}] Simulation completed in {:.2f} seconds", (number, simulationEndTime - simulationStartTime))
        Logger.info("[SIM {:d}] Saving...", number)
        ExportToCSV.export(industry.data, timestamp, number)
        Logger.info("[SIM {:d}] Returning results to main thread...", number)
        return industry.data.getFlatData()
    except Exception as e:
        Logger.logger.exception("Error")
        raise e


if __name__ == '__main__':

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
        
        if(Parameters.NumberOfParallelProcesses > Parameters.NumberOfSimulations):
            Parameters.NumberOfParallelProcesses = Parameters.NumberOfSimulations

        processes = []
        pool = multiprocessing.Pool(Parameters.NumberOfParallelProcesses)
        partial_runSimulation = functools.partial(runSimulation, timestamp=timestamp) # Run simulations
        listOfResults = pool.imap_unordered(partial_runSimulation, range(Parameters.NumberOfSimulations)) # Obtain results

        multiAggregateData.addListOfResults(listOfResults) # Add result to the aggregate list (this will be used to calculate the means)
 
        aggregateEndTime = time.time()
        Logger.info("All {:d} simulations completed in {:.2f} seconds", (Parameters.NumberOfSimulations, aggregateEndTime - aggregateStartTime))
        # Save data
        Logger.info("Saving data...")
        ExportToCSV.export(multiAggregateData, timestamp)
        Logger.info("ALL PROCESSES FINISHED!")

    except Exception as e:
        Logger.logger.exception("Error")
        raise e

    if(Parameters.EnableProfiling):
        pr.disable()
        with io.StringIO() as s:
            ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
            ps.print_stats()
            Logger.info(s.getvalue())
      

