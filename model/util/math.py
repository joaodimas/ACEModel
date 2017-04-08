class Math:

    @classmethod
    def isEquivalent(cls, a, b, precision=5):
        # print("Precision: {:d}".format(precision))
        maxDiff = (10 ** -(precision)) - 10 ** -(precision+1)
        # print("MaxDiff: {:.100f}".format(maxDiff))
        diff = abs(a-b)
        # print("Diff:    {:.100f}".format(diff))
        return diff < maxDiff