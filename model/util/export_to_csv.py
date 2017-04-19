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
    