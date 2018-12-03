
import pandas as pd
import glob
import os
import sys
import gcl
import datetime
import time 

start_time = time.time()
df = pd.read_csv('news/BTC.csv')
df = df.drop('Unnamed: 0', axis = 1)
df=df.iloc[4981:100003, :]
df['published_on'] = pd.to_datetime(df['published_on'])
df['date'] = df['published_on'].apply(lambda x: x.date())
grouped=df.groupby('date')
concat_body=pd.DataFrame(grouped['body'].apply(lambda x: ' '.join(x)))
concat_title=pd.DataFrame(grouped['title'].apply(lambda x: ' '.join(x)))
concat_df=concat_body.join(concat_title)
concat_df['body_sentiment'], concat_df['body_magnitude'] = gcl.sentiment_columns(concat_df.body)
concat_df['title_sentiment'], concat_df['title_magnitude'] = gcl.sentiment_columns(concat_df.title)
concat_df.to_csv('news/aggregated_sentiment_BTC.csv')

'''new_df=pd.DataFrame(concat_df['body_sentiment'].mean())
aggregate_body_magnitude=concat_df['body_magnitude'].mean()
aggregate_title_sentiment=concat_df['title_sentiment'].mean()
aggregate_title_magnitude=concat_df['title_magnitude'].mean()
final_results=new_df.join([aggregate_body_magnitude,aggregate_title_sentiment,aggregate_title_magnitude])

elapsed_time = time.time() - start_time
print(elapsed_time)'''