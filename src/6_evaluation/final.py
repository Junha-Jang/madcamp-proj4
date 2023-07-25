import pandas as pd

from tqdm import tqdm

def input_csv():
    return pd.read_csv('data/raw_data/rss_part5.csv', sep=';', keep_default_na=False)

def output_csv(df):
    df.to_csv('data/processed_data/database.csv', sep=';', index=False)

if __name__ == '__main__':
    print("Step 6: Final... ")

    df = input_csv()

    df_filtered = df.query("summary != ''")

    df_filtered = df_filtered.drop([
        'link',
        'redirect',
        'articleBody',
        'keywords0',
        'keywords1',
        'keywords2',
        'keywords3',
        'keywords4',
        'keywords5',
        'summaryKeywords1',
        'summaryKeywords2',
        'summaryKeywords3',
        'summaryKeywords4',
    ], axis=1)

    df_filtered = df_filtered.rename(
        columns={
            'published': 'date',
            'redirectLink': 'url',
            'articleImage': 'image',
            'summaryKeywords0': 'totalKeywords',
            'summaryKeywords5': 'topKeywords'
        }
    )

    output_csv(df_filtered)

    print("Complete!!!\n")