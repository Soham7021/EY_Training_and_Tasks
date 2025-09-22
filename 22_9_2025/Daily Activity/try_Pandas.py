import pandas as pd
import numpy as np
data = {
    "Name": ["Rahul", "Priya", "Arjun", "Neha", "Vikram"],
    "Age": [21, 22, 20, 23, 21],
    "Course": ["AI", "ML", "Data Science", "AI", "ML"],
    "Marks": [85, 90, 78, 88, 95]
}

df = pd.DataFrame(data)
print(df)
print(" ")
#selecting data

print(df["Name"])
print(" ")
print(df[["Name", "Marks"]]) # Multiple COlumns
print(" ")
print(df.iloc[0]) #first row
print(" ")
print(df.loc[2,"Marks"]) #value at row 2 column Marks

print(" ")
#Filer data
high_scorers = df[df["Marks"] > 80]
print(high_scorers)

#Where clause

df["Result"] = np.where(df["Marks"] >= 80, "Pass","Fail")

df.loc[df["Name"]=="Neha", "Marks"] = 92

print(df)