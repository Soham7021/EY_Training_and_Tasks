import pandas as pd

data = {
    "name":["Soham","Sahil","Rahul"],
    "age":[22,19,37],
    "course":["AIML","MBBS","Law"],
    "skills":["AI","ML","Python"],
    "marks":[50,70,45]
}

df = pd.DataFrame(data)
print(df)