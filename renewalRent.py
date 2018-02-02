"""
    Class: OptionRent
    =================
    This class acts as a calculator to compute the renewal option rent
    for different option. The default input is

        growthRate = 1%
        rent2000 = 15 Million

    Note that this class will compute faster for computer use.
"""
class OptionRent(object):
    def __init__(self, growthRate = 0.01, rent2000 = 15):
        self.growthRate = growthRate
        self.rent2000 = rent2000;
        self.rentByIndex = [rent2000*((1 + growthRate)**(20 + 5*i)) for i in xrange(5)]
        self.rentByYear = [rent2000*((1 + self.growthRate)**(20+i)) for i in xrange(25)]
        self.optionDict = {"A": 0.85, "B": 0.9, "C": 0.95, "D": 1.0}

    def getGrowthRate(self):
        return self.growthRate

    def getRent2000(self):
        return self.getRent2000

    def editGrowthRate(self, newGrowthRate):
        self.growhtRate = newGrowthRate
        self.rentByIndex = [self.rent2000 * ((1 + newGrowthRate)**(20 + 5*i)) for i in xrange(5)]
        self.rentByYear = [self.rent2000 * ((1 + newGrowthRate)**i) for i in xrange(20)]

    def editRent2000(self, newRent):
        self.rent2000 = newRent
        self.rentByIndex = [self.rent2000 * ((1 + newGrowthRate)**(20 + 5*i)) for i in xrange(5)]
        self.rentByYear = [self.rent2000 * ((1 + newGrowthRate)**i) for i in xrange(20)]

    def getRent(self, option, index):
        return self.rentByIndex[index]*self.optionDict[option]

    def getRentByYear(self, option, year):
        if (year <= 2020): return 15.0
        return self.rentByYear[year - 2021]*self.optionDict[option]
