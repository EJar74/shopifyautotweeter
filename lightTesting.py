import requests
from requests_oauthlib import OAuth1
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API URL
TWITTER_API_URL = "https://api.twitter.com/2/tweets"

# OAuth 1.0a User Context credentials
consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

# Function to post a tweet
def post_tweet_v2(message):
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
    payload = {
        "text": message
    }
    response = requests.post(TWITTER_API_URL, json=payload, auth=auth)
    return response

# Test the function
tweet_response = post_tweet_v2("Test tweet from OAuth 1.0a")
if tweet_response.status_code == 201:
    print("Tweet posted successfully.")
else:
    print("Failed to post tweet:", tweet_response.text)
