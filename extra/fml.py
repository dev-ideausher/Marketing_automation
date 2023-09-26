import requests
from bs4 import BeautifulSoup

#  # Function to scrape App Store reviews
# def scrape_app_store_reviews(app_name):
#     app_url = f'https://apps.apple.com/us/app/sort-my-scene/id1575427755'
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    
#     response = requests.get(app_url, headers=headers)
#     if response.status_code != 200:      
#         print(f"Error: Unable to fetch App Store reviews for {app_name}. Status code: {response.status_code}")
#         return
#     else:
#         print("Successfully fetched App Store reviews")

#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Extract reviews
#     reviews = soup.find_all('div', class_='we-customer-review')
#     for review in reviews:
#         rating = review.find('figure', class_='we-star-rating')
#         rating_span = review.find('span', class_='we-star-rating')
#         if rating:
#             rating = rating_span['aria-label']
#         else:             rating = "N/A"

#         review_text = review.find('blockquote', class_='we-truncate we-truncate--multi-line we-truncate--interactive we-truncate--truncated').get_text(strip=True)

#         print(f"Rating: {rating}")
#         print(f"Review: {review_text}\n")

# Function to scrape Google Play Store reviews
from urllib.parse import quote_plus

def scrape_play_store_reviews(app_name):
    # Encode the app name for the URL
    encoded_app_name = quote_plus(app_name)

    app_url = f'https://play.google.com/store/apps/details?id=com.hshah965.sortmysceneapp'
    
    response = requests.get(app_url)
    if response.status_code != 200:
        print(f"Error: Unable to fetch Play Store reviews for {app_name}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract reviews
    review_div = soup.find('div', class_='Jwxk6d')
    # all_review = review_div.find_all('div', {'class': 'EGFGHd'})
    # for review in all_review:
    #     rating_div = review.find('div', class_='c1bOId')
    #     rate_div = rating_div.find('div', class_='Jx4nYe')
    #     rating = rate_div.find('div')['aria-label'] if rate_div else "N/A"

    #     review_text_div = review.find('div', class_='h3YV2d')
    #     review_text=review_text_div.text

    #     print(f"Rating: {rating}")
    #     print(f"Review: {review_text}\n")
    print(review_div)

if __name__ == "__main__":
    app_name = "sort-my-scene"  # Replace with the actual app name
    scrape_play_store_reviews(app_name)
