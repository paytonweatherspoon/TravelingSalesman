import math
import random
import copy
import itertools
import time



def calcDistance(city1,city2):

    return math.sqrt((city2[0] - city1[0])**2 + (city2[1]-city1[1])**2)

# A = [-1,1]
# B = [3,4]
#
# print(distance(A,B))

map = [[0.430796749,0.660341257],[0.869607109,0.145710154],[0.272249997,0.281035268],[0.310050105,0.717362826],[0.847481151,0.505130257],
       [0.054921944,0.597324847],[0.565507064,0.578311901],[0.72633401,0.636552793],[0.170565332,0.160881561],[0.800726237,0.384045138],
       [0.622627218,0.957622127],[0.608021461,0.736718151],[0.628737267,0.622146623],[0.665929436,0.720342005]]

order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

def randomTrip(order):
    usedNums = []
    for i in range(14):
        val = random.randint(0, 13)
        while val in usedNums:
            val = random.randint(0, 13)

        usedNums.append(val)

        order[i] = val

        # print(i)
        # print(val)

        # map[i] = map[val]

    # print(order)
    # return(map)
    # for i in range(len(map)):
    #     map[i] = map[order[i]]

    return order

def tripDistance(order):

    distance = 0

    for i in range(len(order)-1):

        distance += calcDistance(map[order[i]],map[order[i+1]])

    distance += calcDistance(map[order[13]],map[order[0]])

    return distance


def createGenePool(size):
    pool = []
    path = randomTrip(order)

    for i in range(size):
        pool.append(path)
        path = copy.deepcopy(randomTrip(path))

    return pool


def findParents(pool):

    sums = 0
    sqSums = 0
    costList = []

    for i in range(len(pool)):

        cost = tripDistance(pool[i])

        sums += cost
        sqSums += (cost ** 2)

        costList.append(cost)


    poolSTDev = math.sqrt((sqSums - (sums**2/len(pool)))/len(pool))

    mu = sums / len(pool)

    # print(costList)
    # print("mu", mu)
    #
    # print("sigma",poolSTDev)

    for i in range(len(costList)):

        costList[i] = (costList[i] - mu) / poolSTDev

    # print(costList, "z scores")

    parent1Ind = random.randint(0,len(pool)-1)

    # print(costList[parent1Ind])

    count = 0

    while costList[parent1Ind] > -.75:
        # print("Not a good parent")
        # print(costList[parent1Ind])
        count += 1
        parent1Ind = random.randint(0,len(pool)-1)

        if count == 8:
            break

    # print(costList[parent1Ind])

    count = 0

    while True:

        parent2Ind = random.randint(0,len(pool)-1)

        while parent1Ind == parent2Ind:
            parent2Ind = random.randint(0,len(pool)-1)

        if costList[parent2Ind] > -0.75:
            count += 1
            if count == 5:
                break
            continue

        else:
            break

    # print(costList[parent1Ind], "parent 2: ", costList[parent2Ind])

    parents = [pool[parent1Ind],pool[parent2Ind]]

    # print(tripDistance(pool[parent1Ind]), "cost 2: ", tripDistance(pool[parent2Ind]))
    # print(costList[parent1Ind], "SD of 2: " ,costList[parent2Ind])


    return parents

def crossover(parent1, parent2):

    if len(parent1) != len(parent2):
        print("These are not the same size")

    count = 1

    offspring = []

    while len(offspring) != len(parent1):

        for i in range(len(parent1)):
            if parent1[i] in offspring:
                continue
            else:
                offspring.append(parent1[i])
                if len(offspring) == count * 2:
                    break
        count += 1

        for j in range(len(parent2)):
            if parent2[j] in offspring:
                continue
            else:
                offspring.append(parent2[j])
                if len(offspring) == count * 2:
                    break

        # this is for an odd length of the parent it randomly will take the last value from the parent and add it in
        if len(offspring) == len(parent1) -1:
            for i in parent1:
                if i in offspring:
                    continue
                else:
                    offspring.append(i)

        count += 1

    mutation = random.randint(1,101)

    # print(mutation)


    rand1 = random.randint(0,len(parent1)-1)
    rand2 = random.randint(0,len(parent2)-1)

    if mutation >= 80:
        # print("before mutation", offspring)

        changedGene = copy.deepcopy(offspring[rand1])
        offspring[rand1] = offspring[rand2]
        offspring[rand2] = changedGene

        # print("after mutation", offspring)

    return offspring


#exhaustive search

rest = order[1:]

paths = itertools.permutations(rest,13)

cheapestTrip = 5
cheapestPath = []
expensiveTrip = 5
expensivePath = []
sums = 0
sqsums = 0

start = time.time()

for i in paths:

    path = list(i)

    path = [0] + path

    print(tripDistance(path))

    sums += tripDistance(path)

    sqsums += tripDistance(path)**2

    if tripDistance(path) < cheapestTrip:

        cheapestTrip = tripDistance(path)

        cheapestPath = copy.deepcopy(path)

    if tripDistance(path) > expensiveTrip:

        expensiveTrip = tripDistance(path)

        expensivePath = copy.deepcopy(path)

end = time.time()

print("time elapsed", (end-start))


print("cheapest trip", cheapestTrip)
print("cheapest path", cheapestPath)

print("Expensive trip", expensiveTrip)
print("Expensive path", expensivePath)

Stddev = math.sqrt((sqsums - (sums ** 2 / len(order))) / len(order))
exhaustiveMean = sums / len(order)
print("stdDev", Stddev)
print("mean", exhaustiveMean)



# originalPool = createGenePool(100)
#
# cheapestTrip = 5
# cheapestPath = []
# expensiveTrip = 5
# expensivePath = []
# mulist = []
#
# for j in range(100):
#     childList = []
#
#     # originalPool = createGenePool(50)
#
#     for i in range(len(originalPool)//2):
#
#         parents = findParents(originalPool)
#         child = crossover(parents[0],parents[1])
#         childList.append(child)
#
#     while len(childList) != len(originalPool):
#         childList.append(randomTrip(order))
#
#     originalPool = copy.deepcopy(childList)
#
#     sums = 0
#     sqSums = 0
#     costList = []
#
#     for i in range(len(originalPool)):
#         cost = tripDistance(originalPool[i])
#         sums += cost
#         sqSums += (cost ** 2)
#         costList.append(cost)
#
#     poolSTDev = math.sqrt((sqSums - (sums ** 2 / len(originalPool))) / len(originalPool))
#
#     mu = sums / len(originalPool)
#
#     for i in range(len(originalPool)):
#         tripCost = tripDistance(originalPool[i])
#
#         if tripCost < cheapestTrip:
#             cheapestPath = originalPool[i]
#             cheapestTrip = tripCost
#
#         if tripCost > expensiveTrip:
#             expensivePath = originalPool[i]
#             expensiveTrip = tripCost
#
#     mulist.append(mu)
#
# print(childList)
# print(originalPool)
#
# print(cheapestTrip, cheapestPath)
# print(expensiveTrip, expensivePath)

# for i in range(len(mulist)):
#     print(mulist[i])




#Random Trip Search

# lowestCost = 5.0
# highestCost = 5.0
# randsum = 0
# randsqsums = 0
# #
# min = calcDistance(map[11],map[13])
# min = (min * 14)
# max = 14 * math.sqrt(2)
#
#
# dx = (max-min)/100
#
# counter = 0
#
#
# hist = []
# for i in range(1000000):
#
#     trip = (randomTrip(order))
#     cost = (tripDistance(trip))
#
#     randsum += cost
#     randsqsums += (cost**2)
#
#     if lowestCost > tripDistance(order):
#         lowestCost = copy.deepcopy(cost)
#         lowestPath = copy.deepcopy(trip)
#
#     if highestCost < cost:
#         highestCost = copy.deepcopy(cost)
#         highestPath = copy.deepcopy(trip)
#
#
#
#     print(min + (int(((cost-min)/dx))) * dx)
#     counter +=1
#
# print(counter)

# print(lowestCost)
# print(lowestPath)
# print()
# print(highestCost)
# print(highestPath)
# print()
# randSD = math.sqrt((randsqsums - (randsum ** 2 / 1000000)) / 1000000)
# print("random standard deviation", randSD)
# randMu = randsum / 1000000
# print('random mu', randMu)


# ran this and this was my output

"""
3.385146205063552
[4, 9, 1, 8, 2, 5, 3, 0, 7, 13, 10, 11, 6, 12]

7.774279997471655
[1, 11, 2, 7, 0, 4, 3, 12, 8, 13, 5, 9, 6, 10]

random standard deviation 0.5442211141531119
random mu 6.133118141883306
"""

# mulist = []
#
# for i in range(75):
#
#
#     generations = 0
#     solution = 5
#     originalGen = createGenePool(50)
#
#     while generations < 100 or solution < 3 :
#
#         nextGen = []
#
#         sum = 0
#         sqsums = 0
#
#         while len(nextGen) != len(originalGen):
#             pair = findParents(originalGen)
#             child = crossover(pair[0],pair[1])
#
#             sum += tripDistance(child)
#             sqsums += tripDistance(child) **2
#
#             if tripDistance(child) < solution:
#                 solution = tripDistance(child)
#
#             nextGen.append(child)
#
#         mulist.append(sum / len(nextGen))
#
#         originalGen = copy.deepcopy(nextGen)
#
#         generations += 1
#
#     print(solution)
#
# print(mulist)
# print(order)


def simAnneal(order):

# this is the random change to the order

    time = 1
    temperature = 1000

    while temperature > .1:

        orgOrder = copy.deepcopy(order)


        print("old", order, "\t",tripDistance(order))


        val1 = random.randint(0,len(order)-1)
        val2 = random.randint(0,len(order)-1)

        originial1 = copy.deepcopy(order[val1])

        order[val1] = order[val2]
        order[val2] = originial1

        print("new", order,"\t",tripDistance(order))


        if tripDistance(order) < tripDistance(orgOrder):

            order = copy.deepcopy(order)


        else:

            deltaF = tripDistance(order) - tripDistance(orgOrder)

            boltzman = 1.38064852 * 10**-23

            keepProb = (1 / (boltzman*temperature)) * math.exp((-deltaF / (boltzman * temperature)))

            print(deltaF)
            print(1 / (boltzman * temperature) * math.exp((-deltaF)/(boltzman * temperature)))
            print(math.exp(-deltaF/(boltzman * temperature)))




            order = copy.deepcopy(orgOrder)

        time += 1

        temperature = temperature / (1 + math.log(1 + time))




    print("final order ", order)
    print(time)




    return True



