import random
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
    
    def generateRandomWithMaxDistance(self, distance):
        newTasks = self.tasks

        # From 0 to the distance, choose randomly the magnitude of change (hamming distance between the current and the next technology)
        magnitudeOfChange = random.randint(0,distance)
        # Put all tasks in a list to be sorted out randomly
        allTasks = range(0,Parameters.NumberOfTasks - 1)
        for bitToFlip in random.sample(allTasks, magnitudeOfChange):
            newTasks = self.flipBit(newTasks, bitToFlip)

        newTech = Technology(newTasks)
        newTech.magnitudeOfChange = magnitudeOfChange

        return newTech

    def flipBit(self, binary, bitToFlip):
        mask = 2 ** bitToFlip
        return binary ^ mask
