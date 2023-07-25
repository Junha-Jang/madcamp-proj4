import pandas as pd

df = pd.read_csv('data/raw_data/rss.csv', sep=';')

print(df)

df.to_csv('data/raw_data/df_rss.csv', sep=';', index=False)