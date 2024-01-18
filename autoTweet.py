import shopify
import tweepy
import datetime
import pytz
import time
from dotenv import load_dotenv
import os
import requests
from requests_oauthlib import OAuth1

load_dotenv()  # This loads the variables from .env into the environment

# Load API credentials from environment variables
SHOPIFY_API_KEY = os.environ.get('SHOPIFY_API_KEY')
SHOPIFY_PASSWORD = os.environ.get('SHOPIFY_PASSWORD')
SHOPIFY_SHOP_NAME = os.environ.get('SHOPIFY_SHOP_NAME')

# Setting up Shopify API session
shop_url = f"https://{SHOPIFY_SHOP_NAME}.myshopify.com/admin"
shopify.ShopifyResource.set_site(f'{shop_url}/api/2021-04')
shopify.ShopifyResource.set_user(SHOPIFY_API_KEY)
shopify.ShopifyResource.set_password(SHOPIFY_PASSWORD)

shop_tweet_url = os.environ.get('SHOP_TWEET_URL')

# Twitter API URL
TWITTER_API_URL = "https://api.twitter.com/2/tweets"

# OAuth 1.0a User Context credentials
consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

# Function to get the latest products from Shopify
def get_latest_products(since_datetime):
    products = shopify.Product.find(created_at_min=since_datetime)
    return products

# Function to generate hashtags from product title
def generate_hashtags(title):
    words = title.split()
    hashtags = ' '.join([f'#{word}' for word in words])
    return hashtags

# Function to post a tweet using Twitter API v2
def post_tweet_v2(message):
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
    payload = {
        "text": message,
        "reply_settings": "mentionedUsers"  # Limit replies to the posting account
    }
    response = requests.post(TWITTER_API_URL, json=payload, auth=auth)
    return response

# Main function to check for new products and tweet
def check_and_tweet_new_products():
    # Define the time interval for checking new products
    # last_checked_time = datetime.datetime.now(pytz.UTC) - datetime.timedelta(hours=1)
    last_checked_time = datetime.datetime.now(pytz.UTC) - datetime.timedelta(days=30)
    
    # Get the latest products
    new_products = get_latest_products(last_checked_time)
    
    # Post a tweet for each new product
    for product in new_products:
        hashtags = generate_hashtags(product.title)
        tweet_message = f"Check out our new product: {product.title}! See more at {shop_tweet_url}/products/{product.handle}\n{hashtags}"
        # print("tweet message", tweet_message)

        res = post_tweet_v2(tweet_message)
        if res.status_code == 201:
            print("Tweet posted successfully.")
        else:
            print("Failed to post tweet:", res.text)

# Example of scheduling - This part would ideally be run in a server or cloud function
while True:
    check_and_tweet_new_products()
    time.sleep(3600)  # Wait for 1 hour before checking again