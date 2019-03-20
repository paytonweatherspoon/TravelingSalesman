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


# creating table with the distance between each city to every other city

table = []

for i in range(len(map)):
    row = []
    for j in range(len(map)):
        row.append(calcDistance(map[i],map[j]))

    table.append(row)

print(table)

lowestCost = 5.0
highestCost = 5.0
randsum = 0
randsqsums = 0
#
min = calcDistance(map[11],map[13])
min = (min * 14)
max = 14 * math.sqrt(2)

print(min)
dx = (max-min)/100

print(dx)





#exhaustive search

# exhaustiveHist = [0] * 100
#
# rest = order[1:-1]
#
# print(rest)
# paths = itertools.permutations(rest)
#
#
# cheapestTrip = 5
# cheapestPath = []
# expensiveTrip = 5
# expensivePath = []
# sums = 0
# sqsums = 0
#
# start = time.time()
#
# for i in paths:
#     path = list(i)
#
#     distance = 0
#
#     for j in range(len(path)-1):
#
#         distance += table[path[j]][path[j+1]]
#     distance += table[path[-1]][12]
#     distance += table[12][path[0]]
#
#
#     sums += distance
#     sqsums += distance**2
#
#     exhaustiveHist[int((distance-min)/dx)] += 1
#
#     if distance < cheapestTrip:
#
#         cheapestTrip = distance
#
#         cheapestPath = copy.deepcopy(path)
#
#     if distance > expensiveTrip:
#
#         expensiveTrip = distance
#
#         expensivePath = copy.deepcopy(path)
#
# end = time.time()
#
# print("time elapsed", (end-start))
#
#
# print("cheapest trip", cheapestTrip)
# print("cheapest path", cheapestPath)
#
# print("Expensive trip", expensiveTrip)
# print("Expensive path", expensivePath)
#
#
#
# print("sqsums", sqsums)
# print("sums", sums)
#
# for i in exhaustiveHist:
#     print(i)



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
# hist = [0] * 100
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
#     hist[int((cost-min)/dx)] += 1
#     counter +=1
#
# print(counter)
#
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
#
# print(hist)
#
# print(len(hist))
#
# for i in hist:
#     print(i)


# ran this and this was my output

"""
3.385146205063552
[4, 9, 1, 8, 2, 5, 3, 0, 7, 13, 10, 11, 6, 12]

7.774279997471655
[1, 11, 2, 7, 0, 4, 3, 12, 8, 13, 5, 9, 6, 10]

random standard deviation 0.5442211141531119
random mu 6.133118141883306
"""

# genHist = [0] *100
# cheapestTrip = 5
# cheapestPath = []
# maxTrip = 3
# maxPath = []
#
# sum = 0
# sqsums = 0
#
# for i in range(75):
#
#     generations = 0
#     solution = 5
#     originalGen = createGenePool(50)
#
#     while generations < 100 or solution < 3 :
#
#         nextGen = []
#
#         while len(nextGen) != len(originalGen):
#             pair = findParents(originalGen)
#             child = crossover(pair[0],pair[1])
#
#
#             if tripDistance(child) < solution:
#                 solution = tripDistance(child)
#
#                 if solution < cheapestTrip:
#                     cheapestTrip = solution
#                     cheapestPath = copy.deepcopy(child)
#                 if tripDistance(child) > maxTrip:
#                     maxTrip = tripDistance(child)
#                     maxPath = copy.deepcopy(child)
#
#             nextGen.append(child)
#
#
#         originalGen = copy.deepcopy(nextGen)
#
#         generations += 1
#
#     sum += solution
#     sqsums += (solution**2)
#
#     genHist[int((solution-min)/dx)] += 1
#
# print(len(genHist))
#
# for i in genHist:
#     print(i)
#
# print(sum)
#
# print("mean", (sum/50))
#
# print("sqSums" , sqsums)
# print("sums",sum)
#
# print("max path", maxPath)
# print("max trip", maxTrip)
#
#
#
# print("cheapest path", cheapestPath)
# print("cheapest cost", cheapestTrip)


annealHist = [0] * 100

def simAnneal(path):

    temperature = 1000
    time = 1

    while temperature > .00001:

        # print(temperature)

        # this is the random change to the order
        randomchange = random.randint(0,len(order)-1)
        randomchange2 = random.randint(0,len(order)-1)

        while randomchange2 == randomchange:
            randomchange2 = random.randint(0, len(order) - 1)

        # print(randomchange,randomchange2)
        #
        # print("pre change path", path)

        originalPath = copy.deepcopy(path)

        beforeChangeCost = tripDistance(path)
        orgValue = copy.deepcopy(path[randomchange])
        path[randomchange] = path[randomchange2]
        path[randomchange2] = orgValue

        afterChangeCost = tripDistance(path)

        # print('changed path', path)

        if afterChangeCost < beforeChangeCost:
            path = path
            # print("keep change")
        else:

            while True:

                delta = afterChangeCost - beforeChangeCost

                keepChangeProb = 1 / (temperature * math.sqrt(2 * math.pi)) * math.exp((-(delta)**2)/(2*(temperature**2)))

                print(keepChangeProb)


                if keepChangeProb > random.random():
                    # print("we kept the change")
                    # print(path)
                    break

                else:
                    randomchange = random.randint(0, len(order) - 1)
                    randomchange2 = random.randint(0, len(order) - 1)

                    while randomchange2 == randomchange:
                        randomchange2 = random.randint(0, len(order) - 1)

                    beforeChangeCost = tripDistance(path)

                    orgValue = copy.deepcopy(path[randomchange])
                    path[randomchange] = path[randomchange2]
                    path[randomchange2] = orgValue

                    afterChangeCost = tripDistance(path)

                    continue

        # this is cooling the temp
        temperature = temperature / (1+ math.log(1 + time))

        time += 1



    return path


# path = order
# simsums = 0
# simsqsums = 0
#
# maxDistance = 5
# minDistance = 5
# maxpath = []
# minpath = []
#
# for i in range(100):
#
#     path = simAnneal(path)
#
#     simsums += tripDistance(path)
#     simsqsums += (tripDistance(path)**2)
#
#     annealHist[int((tripDistance(path)-min)/dx)] += 1
#
#     if tripDistance(path) > maxDistance:
#         maxDistance = tripDistance(path)
#         maxpath = copy.deepcopy(path)
#
#     if tripDistance(path) < minDistance:
#         minDistance = tripDistance(path)
#         minpath = copy.deepcopy(path)
# #
# for i in annealHist:
#     print(i)
#
# print(simsums / 100)
# print(math.sqrt(simsqsums - (simsums**2/100))/100)
#
# print(maxDistance)
# print(maxpath)
#
# print(minDistance)
# print(minpath)

