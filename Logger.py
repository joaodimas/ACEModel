import datetime
import os
from Parameters import Parameters

class Logger:
    messagesInfo = ""
    messagesDebug = ""
    messagesTrace = ""
    timestamp = datetime.datetime.now()
    
    @classmethod
    def info(cls, message):
        if("INFO" in Parameters.LogLevel["File"]):
            cls.messagesInfo += "\n" + str(message)
        if("DEBUG" in Parameters.LogLevel["File"]): 
            cls.messagesDebug += "\n" + str(message)
        if("TRACE" in Parameters.LogLevel["File"]):
            cls.messagesTrace += "\n" + str(message)
        if("INFO" in Parameters.LogLevel["Console"]):
            print(message)

    @classmethod
    def debug(cls, message):
        if("DEBUG" in Parameters.LogLevel["File"]): 
            cls.messagesDebug += "\n" + str(message)
        if("TRACE" in Parameters.LogLevel["File"]):
            cls.messagesTrace += "\n" + str(message)
        if("DEBUG" in Parameters.LogLevel["Console"]):
            print(message)

    @classmethod
    def trace(cls, message):
        cls.messagesTrace += "\n" + str(message)
        if("TRACE" in Parameters.LogLevel["Console"]):
            print(message)


    @classmethod
    def saveLog(cls):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        if("INFO" in Parameters.LogLevel["File"]):
            with open(os.path.join(THIS_FOLDER, "./data/ACEModel."+cls.timestamp.strftime("%Y-%m-%dT%Hh%Mm%Ss"))+".INFO.log", "w") as f:
                f.write(cls.messagesInfo)

        if("DEBUG" in Parameters.LogLevel["File"]):
            with open(os.path.join(THIS_FOLDER, "./data/ACEModel."+cls.timestamp.strftime("%Y-%m-%dT%Hh%Mm%Ss"))+".DEBUG.log", "w") as f:
                f.write(cls.messagesDebug)

        if("TRACE" in Parameters.LogLevel["File"]):
            with open(os.path.join(THIS_FOLDER, "./data/ACEModel."+cls.timestamp.strftime("%Y-%m-%dT%Hh%Mm%Ss"))+".TRACE.log", "w") as f:
                f.write(cls.messagesTrace)