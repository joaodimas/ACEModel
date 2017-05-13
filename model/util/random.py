import random

class Random:

    def __init__(self):
        # Used for testing
        self.fakeRandom = None
        self.fakeRandInt = None
        self.fakeGetRandBits = None
        self.fakeSample = None
        self.fakeUniform = None

    def random(self):
        if self.fakeRandom is not None and len(self.fakeRandom) > 0:
            return self.fakeRandom.pop(0)

        return random.random()

    def randint(self, min, max):
        if self.fakeRandInt is not None and len(self.fakeRandInt) > 0:
            return self.fakeRandInt.pop(0)

        return random.randint(min, max)

    def getrandbits(self, bits):
        if self.fakeGetRandBits is not None and len(self.fakeGetRandBits) > 0:
            return self.fakeGetRandBits.pop(0)

        return random.getrandbits(bits)

    def sample(self, population, k):
        if self.fakeSample is not None and len(self.fakeSample) > 0:
            return self.fakeSample.pop(0)
        
        return random.sample(population, k)
    
    def uniform(self, a, b):
        if self.fakeUniform is not None and len(self.fakeUniform) > 0:
            return self.fakeUniform.pop(0)

        return random.uniform(a, b)

    def appendFakeRandom(self, number):
        if(self.fakeRandom is None):
            self.fakeRandom = []
        self.fakeRandom.append(number)
    
    def appendFakeRandInt(self, number):
        if(self.fakeRandInt is None):
            self.fakeRandInt = []
        self.fakeRandInt.append(number)

    def appendFakeGetRandBits(self, number):
        if(self.fakeGetRandBits is None):
            self.fakeGetRandBits = []
        self.fakeGetRandBits.append(number)

    def appendFakeSample(self, numbers):
        if(self.fakeSample is None):
            self.fakeSample = []
        self.fakeSample.append(list(numbers))

    def appendFakeUniform(self, number):
        if(self.fakeUniform is None):
            self.fakeUniform = []
        self.fakeUniform.append(number)

    def noFakes(self):
        return  ((self.fakeRandom is None or len(self.fakeRandom) == 0) and
                (self.fakeRandInt is None or len(self.fakeRandInt) == 0) and
                (self.fakeGetRandBits is None or len(self.fakeGetRandBits) == 0) and
                (self.fakeSample is None or len(self.fakeSample) == 0))

    
    def clearAllFakes(self):
        self.fakeRandom = None
        self.fakeRandInt = None
        self.fakeGetRandBits = None
        self.fakeSample = None
        self.fakeUniform = None
