import logging, os
import numbers
from Parameters import Parameters

class Logger:

    logger = None

    @classmethod
    def info(cls, message, args=None, industry=None):
        if(cls.logger.isEnabledFor(logging.INFO)):
            cls.logger.info(cls.format(message, args, industry))

    @classmethod   
    def debug(cls, message, args=None, industry=None):
        if(cls.logger.isEnabledFor(logging.DEBUG)):
            cls.logger.debug(cls.format(message, args, industry))

    @classmethod
    def trace(cls, message, args=None, industry=None):
        if(cls.logger.isEnabledFor(logging.TRACE)):
            cls.logger.trace(cls.format(message, args, industry))

    @classmethod
    def isEnabledForTrace(cls):
        return cls.logger.isEnabledFor(logging.TRACE)

    @classmethod
    def isEnabledForDebug(cls):
        return cls.logger.isEnabledFor(logging.DEBUG)

    @classmethod
    def format(cls, message, args, industry):
        if(industry != None):
            message = "[SIM {:d}][PERIOD {:d}] " + message
            if(isinstance(args, tuple)):
                args = (industry.simulation, industry.currentPeriod) + args
            elif(args != None):
                args = (industry.simulation, industry.currentPeriod, args)
            else:
                args = (industry.simulation, industry.currentPeriod)
        if(isinstance(args, tuple)):
            message = message.format(*args)
        elif(isinstance(args, numbers.Number)):
            message = message.format(args)

        return message

    @classmethod
    def initialize(cls, timestamp):

        #Add custom level TRACE
        logging.TRACE = 9 
        logging.addLevelName(logging.TRACE, "TRACE")
        def trace(self, message, *args, **kws):
            if self.isEnabledFor(logging.TRACE):
                self._log(logging.TRACE, message, args, **kws) 
        logging.Logger.trace = trace


        cls.logger = logging.getLogger("ACEModel")
        if("TRACE" in Parameters.LogLevel["Console"] or "TRACE" in Parameters.LogLevel["File"]):
            cls.logger.setLevel(logging.TRACE)
        elif("DEBUG" in Parameters.LogLevel["Console"] or "DEBUG" in Parameters.LogLevel["File"]):
            cls.logger.setLevel(logging.DEBUG)
        elif("INFO" in Parameters.LogLevel["Console"] or "INFO" in Parameters.LogLevel["File"]):
            cls.logger.setLevel(logging.INFO)
        else:
            cls.logger.setLevel(logging.WARNING)

        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

        # create a logging format
        formatter = logging.Formatter('%(message)s')

        if len(Parameters.LogLevel["Console"]) > 0:
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            cls.logger.addHandler(handler)
            # create a TRACE console handler
            if"TRACE" in Parameters.LogLevel["Console"]:
                handler.setLevel(logging.TRACE)
            elif "DEBUG" in Parameters.LogLevel["Console"]:
                handler.setLevel(logging.DEBUG)
            elif "INFO" in Parameters.LogLevel["Console"]:
                handler.setLevel(logging.INFO)
            else:
                handler.setLevel(logging.WARNING)

        # create an INFO file handler
        if("INFO" in Parameters.LogLevel["File"]):
            handler = logging.FileHandler(os.path.join(THIS_FOLDER, "./data/ACEModel."+timestamp.strftime("%Y-%m-%dT%Hh%Mm%Ss")+".INFO.log"))
            handler.setLevel(logging.INFO)
            handler.setFormatter(formatter)
            cls.logger.addHandler(handler)

        # create a DEBUG file handler
        if("DEBUG" in Parameters.LogLevel["File"]):
            handler = logging.FileHandler(os.path.join(THIS_FOLDER, "./data/ACEModel."+timestamp.strftime("%Y-%m-%dT%Hh%Mm%Ss")+".DEBUG.log"))
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(formatter)
            cls.logger.addHandler(handler)

        # create a TRACE file handler
        if("TRACE" in Parameters.LogLevel["File"]):
            handler = logging.FileHandler(os.path.join(THIS_FOLDER, "./data/ACEModel."+timestamp.strftime("%Y-%m-%dT%Hh%Mm%Ss")+".TRACE.log"))
            handler.setLevel(logging.TRACE)
            handler.setFormatter(formatter)
            cls.logger.addHandler(handler)