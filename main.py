from copy import deepcopy
from renewalRent import OptionRent
import itertools, sys
import csv

'''
    Function: checkOptionCondition
    ==============================
    Return false if the option expands. Otherwise return true.
'''
def checkOptionCondition(x):
    for i in xrange(len(x) - 1):
        if x[i+1] < x[i]: return False
    return True

'''
    Function: splitData
    ===================
    Input: list of data
    Output: Return of a list of list where each list is a possibilities to split data
    into group based on adjacent positions
'''
def splitData(x):
    if len(x) == 0: return [[[]]]
    result = [[[x[0]]]]
    for i in xrange(1, len(x)):
        tempResult = []
        for d in result:
            temp1 = deepcopy(d)
            temp1[-1].append(x[i])
            tempResult.append(temp1)

            temp2 = deepcopy(d)
            temp2.append([x[i]])
            tempResult.append(temp2)
        result = deepcopy(tempResult)
    return result

'''
    Function: seekPossibilities
    ===========================
    This function returns all the possibilities of UCB for five five-year renewal options.
    The output of this function will be list of list where the inside list implies the option
    the consecutive options that USB wants to select.
'''
def seekPossibilities(numPeriod=5):
    options = ['A', 'B', 'C', 'D']
    result = []
    for i in xrange(numPeriod + 1):
        possibilities = map(list, list(itertools.product(options, repeat=i)))
        possibilities = filter(checkOptionCondition, possibilities)
        for d in possibilities:
            result += splitData(d)
    return result

'''
    Function: readPossibilities
    ===========================
    Write all USC actions on five-year renewal plan in the file.
    Each line in the file will contains a string such as

                            A BB CD

    This means USC takes option A from 2020 - 2025,
                         option B from 2025 - 2035,
                         option C from 2035 - 2040,
                         option D from 2040 - 2045

    The space indicates the time break that the new agreement would be made.
'''
def readPossibilities():
    data = seekPossibilities(5);
    with open('options.txt', 'w') as f:
        for d in data:
            f.write(' '.join(map(lambda x: ''.join(x), d)) + '\n')

'''
    Function: computeRentPSF
    ========================
    Compute the rent per square feet given the option.

    INPUT: A list of list e.g. [['A'],['B','B'], ['C', 'D']]
    OUTPUT: A list containing 4 sublists.
            sublist[0] represents floor 26 - 31
            sublist[1] represents floor 15 - 25
            sublist[2] represents floor 8 - 14
            sublist[3] represents floor 1 - 7

        Each element in sublist represents the rent per square feet
        where the first element is rent for year 2016
'''
def computeRentPSF(options):
    calc = OptionRent()
    result = [[calc.getRentByYear("D", year) for year in xrange(2016, 2046)] for _ in xrange(4)]
    binaryMap = [[1 for _  in xrange(5)] + [0.9 for _ in xrange(25)] for _ in xrange(4)]
    if sum(map(len, options)) == 0:
        return result, binaryMap

    index = 0
    for optionSet in options:
        price = calc.getRent(optionSet[0], index)
        for i, option in enumerate(optionSet):
            numChange = 4 - (ord(option) - ord('A'))
            for j in xrange(3, 3 - numChange, -1):
                result[j][5+5*(index + i): 5+5*(index+1+i)] = [price]*5
                binaryMap[j][5+5*(index + i): 5+5*(index+1+i)] = [1]*5
        index += len(optionSet)

    return result, binaryMap

'''
    Function: getRentRSF
    ====================
    Compute all possible renewal options and return a dict mapping from
    option (in text) to list of list (result from computeRentPSF).
'''
def getRentRSF():
    possibilities = seekPossibilities()
    result = {}
    binaryMap = {}
    for i, pos in enumerate(possibilities):
        inp = ' '.join(map(lambda x: ''.join(x), pos))
        outp, bm = computeRentPSF(pos)
        result[inp] = outp
        binaryMap[inp] = bm

    return result, binaryMap

def getRentalIncome(RSF, occupancyRate):
    totalNRA = {0: 145000, 1: 275000, 2: 240000, 3: 240000}
    rentalIncome = [[0 for i in xrange(30)] for j in xrange(5)]
    for i in xrange(len(RSF)):
        for j in range(len(RSF[0])):
            income = totalNRA[i]*RSF[i][j]*occupancyRate[i][j]
            rentalIncome[i][j] = income
            rentalIncome[-1][j] += income

    return rentalIncome

def getAllRentalIncome(allRSF, allOccupancyRate):
    totalRentalIncome = {}
    for k in allRSF:
        totalRentalIncome[k] = getRentalIncome(allRSF[k], allOccupancyRate[k])
    return totalRentalIncome
