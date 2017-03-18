import csv
import os
from Logger import Logger
from Parameters import Parameters

class ExportToCSV:

    @classmethod
    def export(cls, data):
        flatData = data.getFlatData()
        with open(os.path.join(Parameters.DataPath, "ACEModel."+Logger.timestamp.strftime("%Y-%m-%dT%Hh%Mm%Ss")+".csv"), "w", newline='') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerows(flatData)

        with open(os.path.join(Parameters.DataPath, "ACEModel.LATEST.csv"), "w", newline='') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerows(flatData)
