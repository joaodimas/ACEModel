import random, logging
from Parameters import Parameters


class Technology:

    def __init__(self, tasks):
        self.tasks = tasks
        self.magnitudeOfChange = 0
        self.logger = logging.getLogger("ACEModel")

    @classmethod
    def generateRandomTechnology(cls):
        tasks = random.getrandbits(Parameters.NumberOfTasks)
        return Technology(tasks)

    def calculateHammingDistance(self, otherTechnology):
        return bin(self.tasks ^ otherTechnology.tasks).count('1')

    def getTasksStr(self):
        return format(self.tasks, '0' + str(Parameters.NumberOfTasks) + 'b')
    
    def generateRandomWithMaxDistance(self, distance):
        newTasks = self.tasks

        # From 0 to the distance, choose randomly the magnitude of change (hamming distance between the current and the next technology)
        magnitudeOfChange = random.randint(0,distance)
        # Put all tasks in a list to be sorted out randomly
        allTasks = range(0,Parameters.NumberOfTasks - 1)
        for bitToFlip in random.sample(allTasks, magnitudeOfChange):
            self.logger.trace("Task changed: {:d}".format(Parameters.NumberOfPeriods - bitToFlip))
            newTasks = self.flipBit(newTasks, bitToFlip)

        newTech = Technology(newTasks)
        newTech.magnitudeOfChange = magnitudeOfChange

        self.logger.trace("Previous technology:\n{:b}".format(self.tasks))
        self.logger.trace("New technology:\n{:b}".format(newTasks))

        return newTech

    def flipBit(self, binary, bitToFlip):
        mask = 2 ** bitToFlip
        return binary ^ mask

    def flipRandomTask(self):
        bitToFlip = random.randint(0, Parameters.NumberOfTasks - 1)
        self.logger.trace("Task to change: {:d}".format(Parameters.NumberOfTasks - bitToFlip))
        self.logger.trace("Current technology:\n{:b}".format(self.tasks))
        self.tasks = self.flipBit(self.tasks, bitToFlip)
        self.logger.trace("New technology:\n{:b}".format(self.tasks))

    def copyOneRandomTask(self, otherTech):
        bitToCopy = random.randint(0, Parameters.NumberOfTasks - 1)
        self.logger.trace("Task to copy: {:d}".format(Parameters.NumberOfTasks - bitToCopy))
        self.logger.trace("Technology to imitate:\n{:b}".format(otherTech.tasks))
        self.logger.trace("Current technology:\n{:b}".format(self.tasks))
        mask = 2 ** bitToCopy
        
        # Example: bitToCopy = 2
        # Mask 1: 00000100
        
        # Case 1: A is 1, B is 0
        # A:      10001110
        # B:      01101001
        # mask & self.tasks: 00000100
        # mask & otherTech.tasks: 00000000
        # self.tasks ^ mask: 10001010

        # Case 2: A is 0, B is 1
        # A:      10001010
        # B:      01101101
        # mask & self.tasks: 00000000
        # mask & otherTech.tasks: 00000100
        # self.tasks ^ mask: 10001110

        # Case 3: A is 0, B is 0
        # A:      10001010
        # B:      01101001
        # mask & self.tasks: 00000000
        # mask & otherTech.tasks: 00000000

        # Case 4: A is 1, B is 1
        # A:      10001110
        # B:      01101101
        # mask & self.tasks: 00000100
        # mask & otherTech.tasks: 00000100

        if(mask & self.tasks != mask & otherTech.tasks):
            self.tasks = self.tasks ^ mask
        else:
            self.logger.trace("Task {:d} is the same in both firms. No change.".format(Parameters.NumberOfTasks - bitToCopy))

        self.logger.trace("New technology:\n{:b}".format(self.tasks))

