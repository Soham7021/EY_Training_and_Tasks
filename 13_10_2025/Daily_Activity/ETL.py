import pandas as pd

df = pd.read_csv('students.csv')

df.dropna(inplace=True)
df["Marks"] = df['Marks'].astype(int)
df['Result'] = df['Marks'].apply(lambda x: "Pass" if x >= 50 else "Fail")

df.to_csv("cleaned_data.csv", index=False)

print(df.head())