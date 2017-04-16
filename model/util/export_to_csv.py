import csv, os

class ExportToCSV:

    @classmethod
    def export(cls, data, timestamp, simulation = None, period = None):
        flatData = data.getFlatData()

        suffix = "[{:d}]".format(simulation) if simulation != None else "[MEAN]"

        if period != None:
            suffix += "[CROSSSECTIONAL][{:d}]".format(period)
        else:
            suffix += "[TIMESERIES]"


        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(THIS_FOLDER, "../../data/ACEModel."+timestamp.strftime("%Y-%m-%dT%Hh%Mm%Ss")+suffix+".csv"), "w", newline='') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerows(flatData)

        with open(os.path.join(THIS_FOLDER, "../../data/ACEModel.LATEST" + suffix + ".csv"), "w", newline='') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerows(flatData)
