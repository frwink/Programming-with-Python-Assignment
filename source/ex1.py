import csv

with open("../Daten/train.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    print(row)