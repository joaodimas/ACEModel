import functools, itertools
import operator as op
from model.util.Random import Random


class Combinatorics:


    # 
    # Explanation:
    # 'd' is the number of elements drawn from a population of size = 'popSize'.
    # 'Cd' is the number of possible combinations when drawing 'd' elements.
    # 'T' is the sum of 'Cd' when 'd'  goes from 'minDrawings' to 'maxDrawings'.
    # 'Pd' = Cd/T, for each 'd'
    # 
    # Then, this method will return a list 'probs' of (d, Pd), for all d from minDrawings to maxDrawings.
    # 
    # Example:
    # popSize = 10
    # minDrawings = 0
    # maxDrawings = 3
    # T = 176
    # 
    # d = 3
    # Cd = 10! / ((10 - 3)! * 3!) = 120 
    # Pd = 120/176 = 0.681
    # 
    # d = 2 
    # Cd = 10! / ((10 - 2)! * 2!) = 45
    # Pd = 45/176 = 0.255
    # 
    # d = 1 
    # Cd = 10! / ((10 - 1)! * 1!) = 10
    # Pd = 10/176 = 0.056
    # 
    # d = 0
    # Cd = 10! / ((10 - 0)! * 0!) = 1
    # Pd = 1/176 = 0.005
    # 
    # Result: [(3, 0.681), (2, 0.255), (1, 0.056), (0, 0.005)]
    # 
    # * Somebody help me with a better method name ;)
    # 
    @classmethod
    def getProbabilitiesOfDrawingSize(cls, popSize, minDrawings, maxDrawings):
        #print('getProbabilitiesOfDrawingSize')
        T = 0
        l = []
        for d in range(minDrawings, maxDrawings+1):
            Cd = cls.nCr(popSize, d)
            l.append((d, Cd))
            T += Cd

        probs = []
        for d, Cd in l:
            Pd = Cd / T
            probs.append((d, Pd))
            #print('(d, Pd) = ({:d}, {:.50f})'.format(d, Pd))

        return probs

    # Returns the number of combinations when drawing 'r' elements from a population of size 'n'.
    @classmethod
    def nCr(cls, n, r):
        r = min(r, n-r)
        if r == 0: return 1
        numer = functools.reduce(op.mul, range(n, n-r, -1))
        denom = functools.reduce(op.mul, range(1, r+1))
        return numer//denom

    @classmethod
    def random_combination(cls, iterable, r):
        pool = tuple(iterable)
        n = len(pool)
        indices = sorted(Random.sample(range(n), r))
        return tuple(pool[i] for i in indices)

    @classmethod
    def all_combinations(cls, iterable, minR, maxR):
        allCombinations = []
        for r in range(minR, maxR+1):
            # print("Obtaining combinations for magnitude {:d}".format(r))
            combinations = itertools.combinations(iterable, r)
            # print("Obtained. Transforming to list and appending to aggregate list.")
            allCombinations.extend(combinations)

        return allCombinations

    @classmethod
    def select_weighted_choice(choices):
       total = sum(w for c, w in choices)
       r = Random.uniform(0, total)
       upto = 0
       for c, w in choices:
          if upto + w >= r:
             return c
          upto += w
       assert False, "Shouldn't get here"