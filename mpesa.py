import os
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
api_url = os.getenv("api_url")
