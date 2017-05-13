import unittest, datetime
from model.util.logger import Logger
from model.industry import Industry
from model.util.combinatorics import Combinatorics
from model.technology import Technology
from model.parameters import Parameters
from simulation import SystemConfig

class TestTechnology(unittest.TestCase):


    def test_flipTask(self):
        Parameters.NumberOfTasks = 96

        for x in range(Parameters.NumberOfTasks):
            tech = Technology(Industry(1), 0)
            self.assertEqual(tech.tasks, 0)
            task = x+1
            tech.flipTask(task)
            # print("{:096b}".format(tech.tasks))
            self.assertEqual(tech.tasks, 2 ** x)

        tech = Technology(Industry(1), 0)
        for taskToFlip in range(1, Parameters.NumberOfTasks + 1):
            tech.flipTask(taskToFlip)
            # print("{:096b}".format(tech.tasks))

            self.assertEqual(tech.tasks, 2 ** (taskToFlip) - 1 )


    def test_copyTask(self):
        techA = Technology(Industry(1), 2 ** Parameters.NumberOfTasks - 1)
        for taskToCopy in range(1, Parameters.NumberOfTasks + 1):
            techB = Technology(Industry(1), 0)
            techB.copyTask(techA, taskToCopy)
            # print("{:096b}".format(techB.tasks))
            self.assertEqual(techB.tasks, 2 ** (taskToCopy-1))

        techB = Technology(Industry(1), 0)
        for taskToCopy in range(1, Parameters.NumberOfTasks + 1):
            
            techB.copyTask(techA, taskToCopy)
            # print("{:096b}".format(techB.tasks))
            self.assertEqual(techB.tasks, 2 ** (taskToCopy) - 1)

    def test_changeRandomly(self):
        # print('')
        industry = Industry(1)
        Parameters.MaxMagnituteOfChangeInTechEnv = 8
        maxMagnitude = Parameters.MaxMagnituteOfChangeInTechEnv
        
        pointsInCDF = {}

        totalCombinations = 0
        # print("OBTAINING COMBINATIONS")
        for r in range(0,maxMagnitude+1):
            combs = Combinatorics.nCr(Parameters.NumberOfTasks, r)
            totalCombinations += combs
            pointsInCDF[r] = combs
            # print("r: {:d}; combs: {:d}; totalCombinations: {:d}".format(r, combs, totalCombinations))

        cumulative = 0
        # print("OBTAINING POSITIONS IN CDF")
        for r, prob in pointsInCDF.items():
            cumulative += prob / totalCombinations
            pointsInCDF[r] = cumulative
            # print("r: {:d}; (prob/totalCombinations): {:.50f}".format(r, prob / totalCombinations))

        # print("PROCESSING TECH CHANGE")
        for mag in range(0,maxMagnitude+1):
            # print('PROCESSING MAGNITUDE {:d}'.format(mag))
            industry.random.clearAllFakes()
            tasks = 0
            technology = Technology(industry=industry, tasks=tasks)
            if(mag > 0):
                pointToSelectFromCDF = (pointsInCDF[mag] + pointsInCDF[mag - 1]) / 2
            else:
                pointToSelectFromCDF = pointsInCDF[mag] / 2
            industry.random.appendFakeRandom(pointToSelectFromCDF)
            # print("mag: {:d}; pointsInCDF[mag]: {:.50f}".format(mag, pointsInCDF[mag]))

            if mag > 0:
                industry.random.appendFakeSample(range(1, mag+1))

            #print("BEFORE: technology.tasks:\n{:b}".format(technology.tasks))
            technology.changeRandomly()
            #print("mag: {:d}".format(mag))
            #print("AFTER: technology.tasks:\n{:b}".format(technology.tasks))
            if mag == 0:
                self.assertEqual(technology.tasks, tasks)
            # elif mag == 1:
            #     self.assertEqual(bin(technology.tasks), bin(2 ** (Parameters.NumberOfTasks - mag)))
            # elif mag == 2:
            else:
                trueBin = 0
                for x in range(mag):
                    trueBin += 2 ** x
                #print("{:096b}".format(technology.tasks))
                self.assertEqual(bin(technology.tasks), bin(trueBin))

    def test_selectMagnitudeFromUniformDist(self):
        oldNumberOfTasks = Parameters.NumberOfTasks
        Parameters.NumberOfTasks = 10
        oldMaxMagnitudeOfTechChange = Parameters.MaxMagnituteOfChangeInTechEnv
        Parameters.MaxMagnituteOfChangeInTechEnv = 3

        technology = Technology(Industry(1)).generateRandomTasks()

        # Total = 176 combinations
        # 0 draws: 10! / ((10 - 0)! * 0!) = 1 (prob: 0.005; cumulative: 0.005)
        cumul0 = 1/176 # 0.005
        # 1 draw: 10! / ((10 - 1)! * 1!) = 10 (prob: 0.056; cumulative: 0.062)
        cumul1 = (1+10)/176 # 0.062
        # 2 draws: 10! / ((10 - 2)! * 2!) = 45 (prob: 0.255; cumulative: 0.318)
        cumul2 = (1+10+45)/176 # 0.318
        # 3 draws: 10! / ((10 - 3)! * 3!) = 120 (prob: 0.681; cumulative: 0.681)
        cumul3 = 1

        selectionPoint = cumul0 / 2
        selection = technology.selectMagnitudeFromUniformDist(selectionPoint)
        self.assertIsNotNone(selection)
        self.assertEqual(selection, 0)

        selectionPoint = (cumul1 - cumul0) / 2
        selection = technology.selectMagnitudeFromUniformDist(selectionPoint)
        self.assertIsNotNone(selection)
        self.assertEqual(selection, 1)
        
        selectionPoint = (cumul2 - cumul1) / 2
        selection = technology.selectMagnitudeFromUniformDist(selectionPoint)
        self.assertIsNotNone(selection)
        self.assertEqual(selection, 2)
       
        selectionPoint = (cumul3 - cumul2) / 2
        selection = technology.selectMagnitudeFromUniformDist(selectionPoint)
        self.assertIsNotNone(selection)
        self.assertEqual(selection, 3)

        Parameters.NumberOfTasks = oldNumberOfTasks
        Parameters.MaxMagnituteOfChangeInTechEnv = oldMaxMagnitudeOfTechChange

    def setUp(self):
        Logger.initialize(datetime.datetime.now(), SystemConfig.LogLevel)
        Parameters.setInitialParameters()