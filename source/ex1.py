import csv
import math
from itertools import islice
import sqlalchemy  # This might need to be installed
import pandas as pd
import matplotlib.pyplot as plt


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
def findM(test_data, ideal_data, idealFnIdx, diffData):
    M = 0.0
    pointstest = len(test_data)
    pointideal = len(ideal_data)
    for p in range(0, pointstest):
        for pi in range(0, pointideal):
            if test_data[p][0] == ideal_data[pi][0]:
                err = math.fabs(test_data[p][1] - ideal_data[pi][idealFnIdx])
                diffData.append([test_data[p][0], test_data[p][1], err, ideal_data[pi][idealFnIdx]])
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


def save_csv_to_sqlite(table_name, filepath, engine):
    with open(filepath, 'r') as file:
        data_df = pd.read_csv(file)
        data_df.to_sql(table_name, con=engine, index=True, index_label='id', if_exists='replace')


def write_table3_to_db(table_name, diffData, idlFnIdx, engine):
    connection = engine.connect()
    metadata = sqlalchemy.MetaData()

    emp = sqlalchemy.Table(table_name, metadata,
                           sqlalchemy.Column('X', sqlalchemy.Integer()),
                           sqlalchemy.Column('Y1', sqlalchemy.Float()),
                           sqlalchemy.Column('DeltaY', sqlalchemy.Float()),
                           sqlalchemy.Column(f'Funk{idlFnIdx}', sqlalchemy.Float())
                           )
    metadata.create_all(engine)
    # Inserting record one by one
    for line in diffData:
        dict = {'X': line[0], 'Y1': line[1], 'DeltaY': line[2], f'Funk{idlFnIdx}': line[3]}
        query = sqlalchemy.insert(emp).values(dict)
        ResultProxy = connection.execute(query)

    results = connection.execute(sqlalchemy.select([emp])).fetchall()
    df = pd.DataFrame(results)
    df.columns = results[0].keys()
    df.head(4)


def plotTestData(data):
    X = [x for [x, y] in data]
    Y = [y for [x, y] in data]
    plt.scatter(X, Y)


def plotSelectedFn(ideal_data, ordered_ideals):
    X = [row[0] for row in ideal_data]
    for idx in ordered_ideals:
        Y = [row[idx] for row in ideal_data]
        plt.plot(X, Y)


def plotTrainData(train_data):
    X = [row[0] for row in train_data]
    for idx in range(1, 5):
        Y = [row[idx] for row in train_data]
        plt.plot(X, Y)


# main starting point of the script
train_data_filepath = "../Daten/train.csv"
ideal_data_filepath = "../Daten/ideal.csv"

engine = sqlalchemy.create_engine(f'sqlite:///data.db')
save_csv_to_sqlite('train', train_data_filepath, engine)
save_csv_to_sqlite('ideal', ideal_data_filepath, engine)

train_data = read_data(train_data_filepath)
ideal_data = read_data(ideal_data_filepath)

# start 1
ordered_ideals = dict()
points = len(train_data)
for i in range(0, 50):
    ssr = 0
    for j in range(0, 4):
        for p in range(0, points):
            ssr = ssr + (train_data[p][j + 1] - ideal_data[p][i + 1]) ** 2
    ordered_ideals[i + 1] = ssr

ordered_ideals = dict(sorted(ordered_ideals.items(), key=lambda item: item[1]))

# start 2a
test_data = read_data("../Daten/test.csv")

ordered_ideals = list(ordered_ideals)[0:4]

N = findN(train_data, ideal_data, ordered_ideals)
for idealFnIdx in ordered_ideals:
    # find M fills diffData used to write table 3 in the DB.
    # for each of the confirmed function we are going now to create a 4 column table
    # x,y,y-idealy (squared), ideally
    diffData = []
    M = findM(test_data, ideal_data, idealFnIdx, diffData)
    print(diffData)
    print(f'{idealFnIdx} ----> N = {N}, M = {M}')
    if M >= math.sqrt(2) * N:
        raise Exception(f'the ideal function {idealFnIdx} is not confirmed by the test data')

    write_table3_to_db(f'table3_idealFn_{idealFnIdx}', diffData, idealFnIdx, engine)

# if we get here then the ideal function selected are confirmed to be good


# visualization
plt.figure(0)
plotTestData(test_data)
plotSelectedFn(ideal_data, ordered_ideals)

plt.figure(1)
plotTestData(test_data)
plotTrainData(train_data)
plotSelectedFn(ideal_data, ordered_ideals)

plt.show()





