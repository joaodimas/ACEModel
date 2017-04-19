#!/usr/bin/env python3

import sys, time, cProfile, io, pstats, datetime, multiprocessing, functools
from model.timeseries_data import MultiTimeSeriesData
from model.industry import Industry
from model.description import Description
from model.parameters import Parameters
from model.util.logger import Logger
from model.util.export_to_csv import ExportToCSV


def runSimulation(index, timestamp):
    try:
        number = index + 1
        Logger.info("[SIM {:03d}] STARTING SIMULATION", number)
        simulationStartTime = time.time()

        industry = Industry(number, timestamp)

        # Simulate
        for p in range(Parameters.TimeHorizon):
            industry.processPeriod()
            Description.describe(industry)
        
        simulationEndTime = time.time()

        Logger.info("[SIM {:03d}] Simulation completed in {:.2f} seconds", (number, simulationEndTime - simulationStartTime))
        Logger.info("[SIM {:03d}] Saving time-series...", number)
        ExportToCSV.exportTimeSeriesData(industry.timeSeriesData, timestamp, number)
        Logger.info("[SIM {:03d}] Saving panel data...", number)
        ExportToCSV.exportPanelData(industry.panelData, timestamp, number)

        for crossSectionalData in industry.crossSectionalData.periods:
            Logger.info("[SIM {:03d}] Saving cross-sectional data for period {:d}...", (number, crossSectionalData.period))
            ExportToCSV.exportCrosssectionalData(crossSectionalData, timestamp, number, crossSectionalData.period)

        Logger.info("[SIM {:03d}] Returning time-series to main thread...", number)
        return industry.timeSeriesData.getFlatData()
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
        multiTimeSeriesData = MultiTimeSeriesData()
        Logger.info("Executing {:d} simulations\n", Parameters.NumberOfSimulations)
        
        if(Parameters.NumberOfParallelProcesses > Parameters.NumberOfSimulations):
            Parameters.NumberOfParallelProcesses = Parameters.NumberOfSimulations

        processes = []
        pool = multiprocessing.Pool(Parameters.NumberOfParallelProcesses)
        partial_runSimulation = functools.partial(runSimulation, timestamp=timestamp) # Run simulations
        listOfResults = pool.imap_unordered(partial_runSimulation, range(Parameters.NumberOfSimulations)) # Obtain results

        multiTimeSeriesData.addListOfResults(listOfResults) # Add result to the aggregate list (this will be used to calculate the means)
 
        aggregateEndTime = time.time()
        Logger.info("All {:d} simulations completed in {:.2f} seconds", (Parameters.NumberOfSimulations, aggregateEndTime - aggregateStartTime))
        # Save data
        Logger.info("Saving data...")
        if(Parameters.NumberOfSimulations > 1):
            ExportToCSV.export(multiTimeSeriesData, timestamp)
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
      

