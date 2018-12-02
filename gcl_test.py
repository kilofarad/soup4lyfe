import gcl
import pandas as pd

df = pd.read_csv('news/BTC.csv')
df = df.drop('Unnamed: 0', axis = 1)

df = df.head(25)

df['body_sentiment'], df['body_magnitude'] = gcl.sentiment_columns(df.body)
df['title_sentiment'], df['title_magnitude'] = gcl.sentiment_columns(df.title)

df.to_csv('news/BTC with sentiment.csv')
