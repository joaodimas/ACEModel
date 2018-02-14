"""
Agent-based model based in Chang (2015), "Computational Industrial Economics: A generative approach to dynamic analysis in industrial organization". Additional features are described in my master thesis for Panthéon-Sorbonne MSc in Economics.

Author: João Dimas (joaohenriqueavila@gmail.com)
Supervisor: Prof. Angelo Secchi (Paris 1, PSE)

"""

class Math:

    @classmethod
    def isEquivalent(cls, a, b, precision=5):
        maxDiff = (10 ** -(precision)) - 10 ** -(precision+1)
        diff = abs(a-b)
        return diff < maxDiff