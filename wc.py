#!/usr/bin/python 
import itertools
import copy
import sys

from operator    import mul   
from fractions   import Fraction
from collections import defaultdict


class Country:
    
    def __init__(self, name, region):
        self.name   = name
        self.region = region
        self.points = 11111
        
    def __str__(self) :
        return '{0:20} {1:14} {2:4d}'.format(self.name, self.region, int(self.points))

    def __radd__(self, other):
        return other + int(self.points)
    
    def populate(self, points) : 
        self.points = points

#
# A group of 4 countries.
# Includes the sum of the points of the 
# countries.
#
class Group:
    testDict = dict(AFC      = 1,    
                    CONCACAF = 1,
                    CONMEBOL = 1,
                    CAF      = 1,
                    UEFA     = 2)

    def __init__(self, subSeq):
        self.subSeq = subSeq

    def __radd__(self, other):
        return other + self.getPoints()
        
    def __str__(self) :
        return '\n'.join(map(str,self.subSeq)) + '{0:10} {1:11d}'.format(" ", self.getPoints()) + '\n'

    def getPoints(self) :
        return sum(self.subSeq)    

    def validate(self):

        # TestDict has our max count.  Increment each
        # region.  Fail if it goes past our max.
        regionDict = defaultdict(int)
        for country in self.subSeq:
            regionDict[country.region] += 1
            if regionDict[country.region] > Group.testDict[country.region]:
                return False
        return True



# 
# A set of 8 groups.
#
class Field:
    best = float("inf")
    avg  = None
    
    def __init__(self, gList):
        self.groupList = gList
        
    def __str__(self) :
        return '\n'.join(map(str,self.groupList)) + '\n\n-----------------------'

    def addGroup(self, group):
        self.groupList.append(group)

    def updateIfBest(self):
        stdDev = self.getStdDeviation()
        if stdDev < Field.best:
            Field.best = stdDev
            print stdDev
            print self

    def getStdDeviation(self):
        diffSum = 0
        for group in self.groupList:
            diff = group.getPoints() - self.getAvg()
            diffSum += diff * diff
            
        return diffSum    

    def getAvg(self):
        if self.avg == None:
            self.avg = sum(self.groupList) / len(self.groupList)

        return self.avg


# Print things to stdout on one line dynamically
class Printer():

    def __init__(self,data):
        sys.stdout.write("\r\x1b[K"+data.__str__())
        sys.stdout.flush()

def initCounties(fileName):

    f = open(fileName, 'r');
    countryList = []

    for line in f:
        countryArr = line.split();
        country = Country(countryArr[0],countryArr[1]);
        countryList.append(country)

    f.close()
    return countryList



def updateCountries(cList, paths):

    for path in paths:
        f = open(path, 'r');

        for line in f:
            countryArr = line.split();
            name   = countryArr[0]
            points = countryArr[1]
    
            for country in cList:
                if country.name == name:
                    country.populate(points)

        f.close()


def formGroups(cList, groupList):
    global count
    global total 
    global bestR

    combs = itertools.combinations(cList,4)
        
    for combGroup in combs:
        count += 1
        group = Group(combGroup)
        if not group.validate():  
            continue
        
        biggerGroupList = copy.copy(groupList)
        biggerGroupList.append(group)
        
        
        remainder = [x for x in cList if x not in combGroup]

        if (count % 100000) == 0:
            bestR = min(bestR, len(remainder))    
            Printer('stdDev{0:7} Depth {1:4}  Count {2:30} %{3:.12f} {4:30}'.format(Field.best, bestR, count, count/float(total), total))


        if len(remainder) == 0:
            field = Field(biggerGroupList)
            field.updateIfBest()
            
        else:
            formGroups(remainder, biggerGroupList) 

# n Choose k (n|K)
def nCk(n,k): 
    return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1) )

# 32|4 * 28|4 * 24|4 ... 4|4.   E.g.
def nCCk(n):
    return reduce(mul, [nCk(x,4) for x in range(n,0,-4)])


countryList = initCounties('countries-small-12.txt')
countryList = initCounties('countries-small-16.txt')
countryList = initCounties('countries.txt')

path = 'ranking/nateSilver'
path = 'ranking/elo'
path = 'ranking/fifa'

updateCountries(countryList, [path + '/euro.txt', 
                              path + '/afc.txt',
                              path + '/caf.txt',
                              path + '/concacaf.txt',
                              path + '/conmebol.txt'])

count = 0
bestR = 33
total = nCCk(len(countryList))

formGroups(countryList, [])
