"""
Agent-based model based in Chang (2015), "Computational Industrial Economics: A generative approach to dynamic analysis in industrial organization". Additional features are described in my master thesis for Panthéon-Sorbonne MSc in Economics.

Author: João Dimas (joaohenriqueavila@gmail.com)
Supervisor: Prof. Angelo Secchi (Paris 1, PSE)

"""

import csv, os

class ExportToCSV:

    @classmethod
    def exportTimeSeriesData(cls, data, timestamp, simulation = None):
        flatData = data.getFlatData()

        if flatData is None:
            return

        suffix = "[{:d}]".format(simulation) if simulation != None else "[MEAN]"
        suffix += "[TIMESERIES]"

        cls.writeFile(flatData, suffix, timestamp)

    @classmethod
    def exportCrosssectionalData(cls, data, timestamp, simulation = None, period = None):
        flatData = data.getFlatData()

        if flatData is None:
            return

        suffix = "[{:d}]".format(simulation) if simulation != None else "[MEAN]"
        suffix += "[CROSSSECTIONAL][{:d}]".format(period)

        cls.writeFile(flatData, suffix, timestamp)

    @classmethod
    def exportPanelData(cls, data, timestamp, simulation = None):
        flatData = data.getFlatData()

        if flatData is None:
            return

        suffix = "[{:d}]".format(simulation) if simulation != None else "[MEAN]"
        suffix += "[PANEL]"

        cls.writeFile(flatData, suffix, timestamp)

    @classmethod
    def writeFile(cls, flatData, suffix, timestamp):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(THIS_FOLDER, "../../data/ACEModel."+timestamp.strftime("%Y-%m-%dT%Hh%Mm%Ss")+suffix+".csv"), "w", newline='') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerows(flatData)

        with open(os.path.join(THIS_FOLDER, "../../data/ACEModel.[LATEST]"+suffix+".csv"), "w", newline='') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerows(flatData)
    