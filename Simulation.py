import sys, time, cProfile, io, pstats, logging, os, datetime
from Industry import Industry
from Parameters import Parameters
from ExportToCSV import ExportToCSV
from Description import Description

pr = None
if(Parameters.EnableProfiling):
    pr = cProfile.Profile()
    pr.enable()

timestamp = datetime.datetime.now()


#Add custom level TRACE
logging.TRACE = 9 
logging.addLevelName(logging.TRACE, "TRACE")
def trace(self, message, *args, **kws):
    if self.isEnabledFor(logging.TRACE):
        self._log(logging.TRACE, message, args, **kws) 
logging.Logger.trace = trace


logger = logging.getLogger("ACEModel")
logger.setLevel(logging.TRACE)
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# create a logging format
formatter = logging.Formatter('%(message)s')

# create an INFO console handler
if("INFO" in Parameters.LogLevel["Console"]):
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# create a DEBUG console handler
if("DEBUG" in Parameters.LogLevel["Console"]):
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# create a TRACE console handler
if("TRACE" in Parameters.LogLevel["Console"]):
    handler = logging.StreamHandler()
    handler.setLevel(logging.TRACE)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# create an INFO file handler
if("INFO" in Parameters.LogLevel["File"]):
    handler = logging.FileHandler(os.path.join(THIS_FOLDER, "./data/ACEModel."+timestamp.strftime("%Y-%m-%dT%Hh%Mm%Ss")+".INFO.log"))
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# create a DEBUG file handler
if("DEBUG" in Parameters.LogLevel["File"]):
    handler = logging.FileHandler(os.path.join(THIS_FOLDER, "./data/ACEModel."+timestamp.strftime("%Y-%m-%dT%Hh%Mm%Ss")+".AGGREGATE.log"))
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# create a TRACE file handler
if("TRACE" in Parameters.LogLevel["File"]):
    handler = logging.FileHandler(os.path.join(THIS_FOLDER, "./data/ACEModel."+timestamp.strftime("%Y-%m-%dT%Hh%Mm%Ss")+".DETAILED.log"))
    handler.setLevel(logging.TRACE)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


startTime = time.time()

logger.info(sys.version_info)
logger.info(Parameters.describe())
industry = Industry()

# Simulate
for x in range(Parameters.NumberOfPeriods):
    industry.nextPeriod()
    industry.processCurrentPeriod()
    logger.debug(Description.describeAggregate(industry))
    logger.trace(Description.describeIncumbentFirms(industry))

endTime = time.time()
logger.info("Simulation completed in {:.2f} seconds".format(endTime - startTime))

# Save data
logger.info("Saving data...")
ExportToCSV.export(industry.data, timestamp)

if(Parameters.EnableProfiling):
    pr.disable()
    with io.StringIO() as s:
        ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
        ps.print_stats()
        print(s.getvalue())

