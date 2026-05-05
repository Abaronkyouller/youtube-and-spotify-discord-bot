# Spotify API Example
import os
from dotenv import load_dotenv
import requests
load_dotenv()
TOKEN = api_key = os.getenv("SPOTIFY_API_TOKEN")

url = "https://api.spotify.com/v1/search"
headers = {
    "Authorization": "Bearer" + TOKEN
}
params = {
    "q": "Imagine Dragons",
    "type": "artist"
}
response = requests.get(url, headers=headers, params=params)
data = response.json()
print(data)