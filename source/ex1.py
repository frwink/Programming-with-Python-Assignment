import csv
import math
from itertools import islice


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


# max Deviation between a point in train data and any of the 4 selected ideal functions
def findN(train_data, ideal_data, ordered_ideals):
    N = 10.0
    numpoints = len(train_data)
    for idealFnIdx in ordered_ideals:
        for j in range(0, 4):
            for p in range(0, points):
                err = math.fabs(train_data[p][j] - ideal_data[p][idealFnIdx])
                if err > N:
                    # print(f'found  new max for ideal function {idealFnIdx} at location {p} = {err}')
                    N = err
    return N


# calculate the max error between a particular ideal function idealFnIdx and the test data
# test data is a list of lists [[x,y]]
# test data is not ordered by x so this is why i need to find the matching x from test data into the ideal function data
def findM(test_data, ideal_data, idealFnIdx):
    M = 0.0
    pointstest = len(test_data)
    pointideal = len(ideal_data)
    for p in range(0, pointstest):
        for pi in range(0, pointideal):
            if test_data[p][0] == ideal_data[pi][0]:
                err = math.fabs(test_data[p][1] - ideal_data[pi][idealFnIdx])
                if err > M:
                    M = err
                # print(f'findM: found  new max for ideal function {idealFnIdx} at location {p} = {err}')
    return M


def read_data(filepath):
    counter = 0
    with open(filepath, 'r') as file:
        csvreader = csv.reader(file)
        data = []
        for row in csvreader:
            if counter > 0:
                for i in range(0, len(row)):
                    row[i] = float(row[i])
                data.append(row)
            counter = counter + 1
        return data


train_data = read_data("../Daten/train.csv")

ideal_data = read_data("../Daten/ideal.csv")

ordered_ideals = dict()
points = len(train_data)
for i in range(0, 50):
    ssr = 0
    for j in range(0, 4):
        for p in range(0, points):
            ssr = ssr + (train_data[p][j + 1] - ideal_data[p][i + 1]) ** 2
    ordered_ideals[i + 1] = ssr

ordered_ideals = dict(sorted(ordered_ideals.items(), key=lambda item: item[1]))

test_data = read_data("../Daten/test.csv")

ordered_ideals = list(ordered_ideals)[0:4]

N = findN(train_data, ideal_data, ordered_ideals)
for idealFnIdx in ordered_ideals:
    M = findM(test_data, ideal_data, idealFnIdx)
    print(f'{idealFnIdx} ----> N = {N}, M = {M}')
    if M >= math.sqrt(2) * N:
        raise Exception(f'the ideal function {idealFnIdx} is not confirmed by the test data')

# if we get here then the ideal function selected are confirmed to be good

# 33,31,45,3
print(ordered_ideals)
print(ideal_data[1][33])




