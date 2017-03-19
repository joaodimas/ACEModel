import csv, os

class ExportToCSV:

    @classmethod
    def export(cls, data, timestamp):
        flatData = data.getFlatData()
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(THIS_FOLDER, "./data/ACEModel."+timestamp.strftime("%Y-%m-%dT%Hh%Mm%Ss")+".csv"), "w", newline='') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerows(flatData)

        with open(os.path.join(THIS_FOLDER, "./data/ACEModel.LATEST.csv"), "w", newline='') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerows(flatData)
