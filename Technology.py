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
        Logger.trace("Previous technology:\n{0:0{1}b}".format(self.tasks, Parameters.NumberOfTasks))

        # From 0 to the distance, choose randomly the magnitude of change (hamming distance between the current and the next technology)
        magnitudeOfChange = random.randint(0, maxDistance)
        # Put all tasks in a list to be sorted out randomly
        allTasks = range(1,Parameters.NumberOfTasks)
        for taskToFlip in random.sample(allTasks, magnitudeOfChange):
            self.flipTask(taskToFlip)
            # Logger.trace("Task changed: {:d}".format(taskToFlip))

        self.magnitudeOfChange = magnitudeOfChange

        Logger.trace("New technology:\n{0:0{1}b}".format(self.tasks, Parameters.NumberOfTasks))

    # TODO: inconsitent
    def flipRandomTask(self):
        taskToFlip = random.randint(1, Parameters.NumberOfTasks)
        self.flipTask(taskToFlip)

    def flipTask(self, task):
        bitToFlip = Parameters.NumberOfTasks - task
        mask = 2 ** bitToFlip
        newTasks = self.tasks ^ mask

        Logger.trace("Modifying task {:d}".format(task))
        # Logger.trace("Bit to flip: {:d}".format(bitToFlip))
        # Logger.trace("Number of Tasks: {:d}".format(Parameters.NumberOfTasks))
        Logger.trace("Before:\n{0:0{1}b}".format(self.tasks, Parameters.NumberOfTasks))
        Logger.trace("After: \n{0:0{1}b}".format(newTasks, Parameters.NumberOfTasks))
        # assert("{0:0{1}b}".format(newTasks, Parameters.NumberOfTasks)[task-1] != "{0:0{1}b}".format(self.tasks, Parameters.NumberOfTasks)[task-1])
        self.tasks = newTasks


    def copyOneRandomTask(self, otherTech):
        taskToCopy = random.randint(1, Parameters.NumberOfTasks)
        self.copyTask(otherTech, taskToCopy)

    # TODO: inconsitent
    def copyTask(self, otherTech, task):
        bitToCopy = Parameters.NumberOfTasks - task
        Logger.trace("Task to copy: {:d}".format(task))
        Logger.trace("Technology to imitate:\n{0:0{1}b}".format(otherTech.tasks, Parameters.NumberOfTasks))
        Logger.trace("Current technology:\n{0:0{1}b}".format(self.tasks, Parameters.NumberOfTasks))
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
            Logger.trace("Task {:d} is the same in both firms. No change.".format(task))

        Logger.trace("New technology:\n{0:0{1}b}".format(self.tasks, Parameters.NumberOfTasks))
