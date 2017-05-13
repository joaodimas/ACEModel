import random

class Random:
 
    # Used for testing
    fakeRandom = None
    fakeRandInt = None
    fakeGetRandBits = None
    fakeSample = None
    fakeUniform = None

    @classmethod
    def random(cls):
        if cls.fakeRandom is not None and len(cls.fakeRandom) > 0:
            return cls.fakeRandom.pop(0)

        return random.random()

    @classmethod
    def randint(cls, min, max):
        if cls.fakeRandInt is not None and len(cls.fakeRandInt) > 0:
            return cls.fakeRandInt.pop(0)

        return random.randint(min, max)

    @classmethod
    def getrandbits(cls, bits):
        if cls.fakeGetRandBits is not None and len(cls.fakeGetRandBits) > 0:
            return cls.fakeGetRandBits.pop(0)

        return random.getrandbits(bits)

    @classmethod
    def sample(cls, population, k):
        if cls.fakeSample is not None and len(cls.fakeSample) > 0:
            return cls.fakeSample.pop(0)
        
        return random.sample(population, k)

    @classmethod
    def uniform(cls, a, b):
        if cls.fakeUniform is not None and len(cls.fakeUniform) > 0:
            return cls.fakeUniform.pop(0)

        return random.uniform(a, b)

    @classmethod
    def appendFakeRandom(cls, number):
        if(cls.fakeRandom is None):
            cls.fakeRandom = []
        cls.fakeRandom.append(number)

    @classmethod
    def appendFakeRandInt(cls, number):
        if(cls.fakeRandInt is None):
            cls.fakeRandInt = []
        cls.fakeRandInt.append(number)

    @classmethod
    def appendFakeGetRandBits(cls, number):
        if(cls.fakeGetRandBits is None):
            cls.fakeGetRandBits = []
        cls.fakeGetRandBits.append(number)

    @classmethod
    def appendFakeSample(cls, numbers):
        if(cls.fakeSample is None):
            cls.fakeSample = []
        cls.fakeSample.append(list(numbers))

    @classmethod
    def appendFakeUniform(cls, number):
        if(cls.fakeUniform is None):
            cls.fakeUniform = []
        cls.fakeUniform.append(number)

    @classmethod
    def noFakes(cls):
        return  ((cls.fakeRandom is None or len(cls.fakeRandom) == 0) and
                (cls.fakeRandInt is None or len(cls.fakeRandInt) == 0) and
                (cls.fakeGetRandBits is None or len(cls.fakeGetRandBits) == 0) and
                (cls.fakeSample is None or len(cls.fakeSample) == 0))

    @classmethod
    def clearAllFakes(cls):
        cls.fakeRandom = None
        cls.fakeRandInt = None
        cls.fakeGetRandBits = None
        cls.fakeSample = None
        cls.fakeUniform = None
