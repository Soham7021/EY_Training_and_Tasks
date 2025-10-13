import pandas as pd

# Extract
def run_pipeline():
    df = pd.read_csv('customers.csv')

    # Transform

    for i in df['Age']:
        if i <= 30:
            df['Agegroup'] = 'Young'
        elif i>30 and i < 50:
            df['Agegroup'] = 'Adult'
        else:
            df['Agegroup'] = 'Senior'

    # Load
    df = df[df['Age'] >= 20]
    df.to_csv("filtered_customers.csv", index=False)

if __name__ == "__main__":
    run_pipeline()