import datetime
import os

class Logger:
    messages = ""
    timestamp = datetime.datetime.now()
    
    @classmethod
    def log(cls, message):
        cls.messages += "\n" + str(message)
        print(message)

    @classmethod
    def debug(cls, message):
        cls.messages
        print(message)

    @classmethod
    def saveLog(cls):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        text_file = open(os.path.join(THIS_FOLDER, "./data/ACEModel."+cls.timestamp.strftime("%Y-%m-%dT%Hh%Mm%Ss"))+".log", "w")
        text_file.write(cls.messages)
        text_file.close()