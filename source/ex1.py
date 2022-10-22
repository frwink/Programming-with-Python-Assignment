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

ideal_data=read_data("../Daten/ideal.csv")



import numpy as np
import pandas as pd
import statsmodels.api as sm

# load statsmodels as alias ``sm``import statsmodels.api as sm
# load the longley dataset into a pandas data frame - first column (year) used as row labels
df = pd.read_csv('../Daten/train.csv', index_col=0)

df_ideal = pd.read_csv('../Daten/ideal.csv',index_col=0)
ordered_ideals = dict()
for i in range(1,50):
    ystr = "y"+str(i)
    print(ystr)
    x=df_ideal.get(ystr)

    X = sm.add_constant(x)  # Adds a constant term to the predictor

    print("-----------X----------------")
    print(X)

    sum = 0
    for y in [df[["y1"]]]:
        print("-----------Y ----------------")
        print(y)
        est=sm.OLS( y,X).fit()


        summary=est.summary()
        print(summary)
        print(est.ssr)
        sum=sum+est.ssr
    ordered_ideals[ystr]=sum
    print(f"-----------SUM----------{sum}")

ordered_ideals=dict(sorted(ordered_ideals.items(), key=lambda item: item[1]))
print(ordered_ideals)

# import packages
import pandas as pd
import numpy as np
import statsmodels.api as sm

# reading csv file as pandas dataframe
data = pd.read_csv('../Daten/train.csv')

# independent variable
x = data['Head Size(cm^3)']

# output variable (dependent)
y = data['Brain Weight(grams)']

# adding constant
x = sm.add_constant(x)

# fit linear regression model
model = sm.OLS(y, x).fit()

# display model summary
print(model.summary())

# residual sum of squares
print(model.ssr)