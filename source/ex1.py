import csv
def read_data(filepath):
    counter = 0
    with open(filepath, 'r') as file:
        csvreader = csv.reader(file)
        data=[]
        for row in csvreader:
            if counter>0:
                for i in range(0, len(row)):
                    row[i] = float(row[i])
                data.append(row)
            counter=counter+1
        return data


train_data=read_data("../Daten/train.csv")

ideal_data=read_data("../Daten/ideal.csv")
print(train_data)

ordered_ideals = dict()
points = len(train_data)
for i in range(0,50):
    ssr = 0
    for j in range(0,4):
        for p in range(0,points):
            ssr = ssr + (train_data[p][j+1]-ideal_data[p][i+1])**2
    ordered_ideals[i+1]=ssr

ordered_ideals=dict(sorted(ordered_ideals.items(), key=lambda item: item[1]))

print(ordered_ideals)

