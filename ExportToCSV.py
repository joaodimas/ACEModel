import csv
import os
from Logger import Logger
from Parameters import Parameters

class ExportToCSV:

    @classmethod
    def export(cls, data):
        flatData = data.getFlatData()
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(THIS_FOLDER, "./data/ACEModel."+Logger.timestamp.strftime("%Y-%m-%dT%Hh%Mm%Ss")+".csv"), "w", newline='') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerows(flatData)

        with open(os.path.join(THIS_FOLDER, "./data/ACEModel.LATEST.csv"), "w", newline='') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerows(flatData)
