import csv
def read_data(filepath):
    counter = 0
    with open(filepath, 'r') as file:
        csvreader = csv.reader(file)
        data=[]
        for row in csvreader:
            if counter>0:
                data.append(row)
            counter=counter+1
        return data


train_data=read_data("../Daten/train.csv")
print(train_data)

ideal_data=read_data("../Daten/ideal.csv")
print(ideal_data)