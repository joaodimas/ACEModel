#!/usr/bin/env python3

import os, sys, time, cProfile, io, pstats, datetime, multiprocessing, functools
from model.timeseries_data import MultiTimeSeriesData
from model.industry import Industry
from model.description import Description
from model.parameters import Parameters
from model.util.logger import Logger
from model.util.export_to_csv import ExportToCSV


class SystemConfig:
    LogLevel = {"Console": ["INFO"]}
    EnableProfilingMainThread = False
    EnableProfilingWorker = False
    NumberOfParallelProcesses = 72 # Set this to 3x the number of CPUs. Parallelism is only used if multiple simulations are performed (NumberOfIndependentReplications > 1). Otherwise, only 1 process will be started.


def runSimulation(index, timestamp):
    try:

        pr = None
        if(SystemConfig.EnableProfilingWorker):
            pr = cProfile.Profile()
            pr.enable()

        number = index + 1
        Logger.info("[SIM {:03d}] STARTING SIMULATION", number)
        simulationStartTime = time.time()

        industry = Industry(number)

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

        if(SystemConfig.EnableProfilingWorker):
            pr.disable()
            with io.StringIO() as s:
                ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
                ps.print_stats()
                Logger.info(s.getvalue())

        return industry.timeSeriesData.getFlatData()
    except Exception as e:
        Logger.logger.exception("Error")
        raise e


def describeModelParameters():
    parameters = {}
    obj = Parameters()
    members = [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__")]
    for member in members:
        parameters[member] = getattr(obj, member)

    desc = ""
    for key, value in parameters.items():
        desc += key + ": " + str(value) + "\n"

    return desc


if __name__ == '__main__':

    pr = None
    if(SystemConfig.EnableProfilingMainThread):
        pr = cProfile.Profile()
        pr.enable()

    timestamp = datetime.datetime.now()
    aggregateStartTime = time.time()
    Logger.initialize(timestamp, SystemConfig.LogLevel)
    Logger.info(sys.version_info)
    Parameters.setInitialParameters()
    parameters = describeModelParameters()
    Logger.info(parameters)
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(THIS_FOLDER, "./data/ACEModel."+timestamp.strftime("%Y-%m-%dT%Hh%Mm%Ss")+".params.txt"), "w", newline='') as f:
        print(parameters, file=f)

    try:
        multiTimeSeriesData = MultiTimeSeriesData()
        Logger.info("Executing {:d} simulations\n", Parameters.NumberOfIndependentReplications)
        
        if(SystemConfig.NumberOfParallelProcesses > Parameters.NumberOfIndependentReplications):
            SystemConfig.NumberOfParallelProcesses = Parameters.NumberOfIndependentReplications

        processes = []
        pool = multiprocessing.Pool(SystemConfig.NumberOfParallelProcesses)
        partial_runSimulation = functools.partial(runSimulation, timestamp=timestamp) # Run simulations
        listOfResults = pool.imap_unordered(partial_runSimulation, range(Parameters.NumberOfIndependentReplications)) # Obtain results

        multiTimeSeriesData.addListOfResults(listOfResults) # Add result to the aggregate list (this will be used to calculate the means)
 
        aggregateEndTime = time.time()
        Logger.info("All {:d} simulations completed in {:.2f} seconds", (Parameters.NumberOfIndependentReplications, aggregateEndTime - aggregateStartTime))
        # Save data
        Logger.info("Saving data...")
        if(Parameters.NumberOfIndependentReplications > 1):
            ExportToCSV.export(multiTimeSeriesData, timestamp)
        Logger.info("ALL PROCESSES FINISHED!")

    except Exception as e:
        Logger.logger.exception("Error")
        raise e

    if(SystemConfig.EnableProfilingMainThread):
        pr.disable()
        with io.StringIO() as s:
            ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
            ps.print_stats()
            Logger.info(s.getvalue())
