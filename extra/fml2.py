from google_play_scraper import Sort, reviews_all,reviews
from app_store_scraper import AppStore
import pandas as pd
import numpy as np
import multiprocessing

# Function to scrape Google Play Store reviews
def scrape_play_store_reviews(app_id):
    g_reviews,continuation_token= reviews(
        app_id,
        # sleep_milliseconds=0, 
        lang='en', 
        country='in',  
        sort=Sort.NEWEST,  
    )
    return g_reviews

# Function to scrape App Store reviews
def scrape_app_store_reviews(app_id):
    a_reviews = AppStore('in', app_id, '1575427755')
    a_reviews.review()
    return a_reviews.reviews

if __name__ == "__main__":
    app_ids = ["com.hshah965.sortmysceneapp", "sort-my-scene"]
    
    with multiprocessing.Pool(processes=2) as pool:
        g_reviews = pool.map(scrape_play_store_reviews, app_ids)
        a_reviews = pool.map(scrape_app_store_reviews, app_ids)
    
    g_df = pd.concat([pd.DataFrame(g) for g in g_reviews], ignore_index=True)
    a_df = pd.concat([pd.DataFrame(a) for a in a_reviews], ignore_index=True)

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


