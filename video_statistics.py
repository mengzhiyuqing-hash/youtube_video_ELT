import requests
import json

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")
API_KEY=os.getenv("api_key")
CHANNEL_HANDLE="MrBeast"



def get_playlist_id():
    try:
        url=f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
        response=requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data=response.json()
        channel_items=data["items"][0]
        channel_playlistId=channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print(channel_playlistId)
        return channel_playlistId
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None   

maxResults=50

def get_video_ids(playlistId):
    video_ids=[]
    page_token=""
    base_url=f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={API_KEY}"
    try:
        while True:
            url=base_url
            if page_token:
                url+=f"&pageToken={page_token}"
            response=requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            data=response.json()
            for item in data["items"]:
                video_id=item["contentDetails"]["videoId"]
                video_ids.append(video_id)
            page_token=data.get("nextPageToken")
            if not page_token:
                break
        return video_ids
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")   


# 如果直接运行这个脚本，才执行函数 
    
if __name__ == "__main__":   
    playlistId=get_playlist_id()
    print(get_video_ids(playlistId))
    