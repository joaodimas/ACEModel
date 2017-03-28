import random
from Logger import Logger
from Parameters import Parameters


class Technology:

    def __init__(self, tasks):
        self.tasks = tasks
        self.magnitudeOfChange = 0

    @classmethod
    def generateRandomTechnology(cls):
        tasks = random.getrandbits(Parameters.NumberOfTasks)
        return Technology(tasks)

    def calculateHammingDistance(self, otherTechnology):
        return bin(self.tasks ^ otherTechnology.tasks).count('1')

    def getTasksStr(self):
        return format(self.tasks, '0' + str(Parameters.NumberOfTasks) + 'b')
    
    def transformRandomlyWithMaxDistance(self, maxDistance):
        # From 0 to the distance, choose randomly the magnitude of change (hamming distance between the current and the next technology)
        magnitudeOfChange = random.randint(0, maxDistance)
        # Put all tasks in a list to be sorted out randomly
        allTasks = range(1,Parameters.NumberOfTasks)
        for taskToFlip in random.sample(allTasks, magnitudeOfChange):
            self.flipTask(taskToFlip)
            # Logger.trace("[SIM {:d}]Task changed: {:d}".format(taskToFlip))

        self.magnitudeOfChange = magnitudeOfChange

    def flipRandomTask(self):
        taskToFlip = random.randint(1, Parameters.NumberOfTasks)
        self.flipTask(taskToFlip)

    def flipTask(self, task):
        bitToFlip = Parameters.NumberOfTasks - task
        mask = 2 ** bitToFlip
        newTasks = self.tasks ^ mask

        self.tasks = newTasks
        self.taskChanged = task

    def copyOneRandomTask(self, otherTech):
        taskToCopy = random.randint(1, Parameters.NumberOfTasks)
        self.copyTask(otherTech, taskToCopy)

    # TODO: inconsitent
    def copyTask(self, otherTech, task):
        bitToCopy = Parameters.NumberOfTasks - task
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
            self.taskChanged = task
        else:
            self.taskChanged = 0
