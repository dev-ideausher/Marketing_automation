from google_play_scraper import app, Sort, reviews_all
from app_store_scraper import AppStore
import pandas as pd
import numpy as np


# Google Play Store Reviews
g_reviews = reviews_all(
    "com.hshah965.sortmysceneapp",
    sleep_milliseconds=0, 
    lang='en', 
    country='in',  
    sort=Sort.NEWEST,  
)

# App Store Reviews
a_reviews = AppStore('in', 'sort-my-scene', '1575427755')
a_reviews.review()
# print(a_reviews.reviews_count)

g_df = pd.DataFrame(g_reviews)
a_df = pd.DataFrame(a_reviews.reviews)

g_df = g_df[['userName', 'score', 'content']]
a_df = a_df[['userName', 'rating', 'review']]

g_df.rename(columns={'userName': 'user_name', 'score': 'rating', 'content': 'review_description'}, inplace=True)
a_df.rename(columns={'rating': 'rating', 'review': 'review_description'}, inplace=True)


g_df['source'] = 'Google Play'
a_df['source'] = 'App Store'


result = pd.concat([g_df, a_df], ignore_index=True)
result['combined_username'] = result.apply(lambda row: row['user_name'] if pd.notna(row['user_name']) else row['userName'], axis=1)
result.drop(columns=['user_name', 'userName'], inplace=True)

result = result[['combined_username', 'rating', 'review_description', 'source']]

result.to_csv('app_reviews_combined.csv', index=False)

print(f"Number of Google Play Store reviews fetched: {len(g_df)}")
print(f"Number of App Store reviews fetched: {len(a_df)}")
