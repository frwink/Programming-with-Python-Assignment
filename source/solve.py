from itertools import islice
import sqlalchemy  # This might need to be installed
import pandas as pd
import matplotlib.pyplot as plt
from helper import CsvReader, CsvToSql, Table3Dumper
from idealprocessor import IdealFunctionSumSquareValues, IdealFnValidatorSqrtN


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


csvreader = CsvReader()
# main starting point of the script
train_data_filepath = "../Daten/train.csv"
ideal_data_filepath = "../Daten/ideal.csv"

engine = sqlalchemy.create_engine(f'sqlite:///data.db')
sql_csvwriter = CsvToSql(engine)

sql_csvwriter.save_csv_to_sqlite('train', train_data_filepath)
sql_csvwriter.save_csv_to_sqlite('ideal', ideal_data_filepath)

train_data = csvreader.read_data(train_data_filepath)
ideal_data = csvreader.read_data(ideal_data_filepath)

# start 1
idealFnsProcessor = IdealFunctionSumSquareValues(train_data, ideal_data)
ordered_ideals = idealFnsProcessor.find_best_ideals(4)

# start 2a
test_data = csvreader.read_data("../Daten/test.csv")

idealFnsValidator = IdealFnValidatorSqrtN(test_data, ideal_data, train_data, ordered_ideals)
diffDataList = idealFnsValidator.validate()
if (len(diffDataList) != len(ordered_ideals)):
    raise Exception(f'Expecting validation diff data to be the same size as the best k ideal functions')

for i in range(0, len(ordered_ideals)):
    diffData = diffDataList[i]
    idealFnIdx = ordered_ideals[i]
    table_name = f'table3_idealFn_{idealFnIdx}'
    table3dumper = Table3Dumper(engine, table_name, diffData, idealFnIdx)
    table3dumper.write_table3_to_db()

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





