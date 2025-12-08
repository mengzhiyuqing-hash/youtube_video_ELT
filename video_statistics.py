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

def extract_video_data(video_ids):
    extracted_data=[]
    def batch_video_ids(video_id_list,batch_size):
        for i in range(0,len(video_id_list),batch_size):
            yield video_id_list[i:i+batch_size]
    try:
        for ids in batch_video_ids(video_ids,maxResults):
            video_ids_str=",".join(ids)
            url=f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails,snippet,statistics&id={video_ids_str}&key={API_KEY}"
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()
            
            for i in data.get("items",[]):
                video_id=i['id']
                snippet=i['snippet']
                contentDetails=i['contentDetails']
                statistics=i['statistics']
                
                video_data={
                    "video_id":video_id,
                    "title":snippet.get("title"),
                    "publishedAt":snippet.get("publishedAt"),
                    "duration":contentDetails.get("duration"),
                    "viewCount":statistics.get("viewCount",None),
                    "likeCount":statistics.get("likeCount",None),
                    "commentCount":statistics.get("commentCount",None),
                }
                extracted_data.append(video_data)
        return extracted_data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred:{e}")    
   

from datetime import date 
def save_to_json(extracted_data):
    file_path=f"D:\work\youtube_video_ELT\data\extracted_video_data_{date.today()}.json"
    with open(file_path,"w",encoding="utf-8") as json_outfile:
        json.dump(extracted_data,json_outfile,ensure_ascii=False,indent=4) 


if __name__ == "__main__":   
    playlistId=get_playlist_id()
    video_ids=get_video_ids(playlistId)
    extracted_data=extract_video_data(video_ids)
    save_to_json(extracted_data)
