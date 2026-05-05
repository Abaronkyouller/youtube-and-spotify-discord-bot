import os
from dotenv import load_dotenv
import requests
load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")


url = "https://www.googleapis.com/youtube/v3/search"

query = "Imagine Dragons"
params = {
    "part": "snippet",
    "q": query,
    "type": "video",
    "maxResults": 5,
    "key": API_KEY
}
response = requests.get(url, params=params)
data = response.json()
video_ids = [x["id"]["videoId"] for x in data["items"]]
link_youtube = ["https://www.youtube.com/watch?v=" + video_id for video_id in video_ids]
print(link_youtube)