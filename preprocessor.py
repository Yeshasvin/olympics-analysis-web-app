import pandas as pd

def preprocess(df, df_region):

    # Filtering for summer olympics
    df = df[df['Season'] == 'Summer']

    # Merging df_region for name of the country
    df = df.merge(df_region, on='NOC', how='left')

    # Removing the duplicates as it single team medal will be considered as the sum of medals of all the members
    df.drop_duplicates(inplace=True)

    # One hot encoding the medals
    df = pd.concat([df, pd.get_dummies(df['Medal'], dtype='int')], axis=1)
    return df


