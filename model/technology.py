from model.util.combinatorics import Combinatorics
from model.parameters import Parameters



class Technology:

    def __init__(self, industry, tasks=None, techId=None):
        self.industry = industry
        self.techId = techId
        self.tasks = tasks
        self.magnitudeOfChange = 0

    def generateRandomTasks(self):
        self.tasks = self.industry.random.getrandbits(Parameters.NumberOfTasks)

        return self

    def calculateHammingDistance(self, otherTechnology):
        return bin(self.tasks ^ otherTechnology.tasks).count('1')

    def getTasksStr(self):
        return format(self.tasks, '0' + str(Parameters.NumberOfTasks) + 'b')

    def changeRandomly(self):
        selectionPoint = self.industry.random.random()
        self.magnitudeOfChange = self.selectMagnitudeFromUniformDist(selectionPoint)

        if self.magnitudeOfChange == 0:
            return self

        # Put all tasks in a list to be sorted out randomly
        allTasks = range(1,Parameters.NumberOfTasks)
        for taskToFlip in self.industry.random.sample(allTasks, self.magnitudeOfChange):
            self.flipTask(taskToFlip)

        return self

    def selectMagnitudeFromUniformDist(self, selectionPoint):
        probs = Combinatorics.getProbabilitiesOfDrawingSize(Parameters.NumberOfTasks, 0, Parameters.MaxMagnituteOfChangeInTechEnv)
        cumulative = 0
        while True:
            r, prob = probs.pop(0)
            cumulative += prob
            if cumulative > selectionPoint:
                return r

    def flipRandomTask(self):
        taskToFlip = self.industry.random.randint(1, Parameters.NumberOfTasks)
        self.flipTask(taskToFlip)

        return self

    def flipTask(self, task):
       #assert task <= Parameters.NumberOfTasks
        
        # bitToFlip = Parameters.NumberOfTasks - task
        mask = 2 ** (task - 1)
        newTasks = self.tasks ^ mask

        self.tasks = newTasks
        self.taskChanged = task

        return self

    def copyOneRandomTask(self, otherTech):
        assert(self.tasks is not None)
        assert(otherTech.tasks is not None)
        taskToCopy = self.industry.random.randint(1, Parameters.NumberOfTasks)
        self.copyTask(otherTech, taskToCopy)

        return self

    def copyTask(self, otherTech, task):
       #assert task <= Parameters.NumberOfTasks

        # bitToCopy = Parameters.NumberOfTasks - task
        mask = 2 ** (task - 1)
        
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

        return self
