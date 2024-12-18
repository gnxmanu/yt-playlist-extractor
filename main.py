import os
import csv
import time
import pandas as pd
from datetime import datetime, timedelta
import yt_dlp
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from tqdm import tqdm

# Path to client secrets file
CLIENT_SECRET_FILE = r"client_secrets.json"


def authenticate_youtube():
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        ["https://www.googleapis.com/auth/youtube.readonly"]
    )
    credentials = flow.run_local_server(port=8080)
    return build("youtube", "v3", credentials=credentials)


def execute_request(request, backoff_time=900, max_backoff_time=3600):
    while True:
        try:
            return request.execute()
        except HttpError as e:
            if e.resp.status == 403:
                wait_time = datetime.now() + timedelta(seconds=backoff_time)
                print(f"Quota exceeded, retrying in {backoff_time // 60} minutes at {wait_time.strftime('%Y-%m-%d %H:%M:%S')}")
                time.sleep(backoff_time)
                backoff_time = min(backoff_time * 2, max_backoff_time)
            else:
                raise


def get_all_playlists(youtube_object):
    playlists, next_page_token = [], None
    while next_page_token is not None or playlists == []:
        request = youtube_object.playlists().list(part='snippet', mine=True, maxResults=50, pageToken=next_page_token)
        response = execute_request(request)
        playlists.extend(response['items'])
        next_page_token = response.get('nextPageToken')

    extracted_playlist_ids = [p['id'] for p in playlists]
    extracted_playlist_titles = [p['snippet']['title'] for p in playlists]
    extracted_playlist_links = [f'https://www.youtube.com/playlist?list={p["id"]}' for p in playlists]

    return extracted_playlist_ids, extracted_playlist_titles, extracted_playlist_links


def get_playlist_video_details(playlist_urls, youtube_object=None):
    all_videos = []
    processed_playlists = []

    if youtube_object:
        for playlist_id, playlist_title in tqdm(playlist_urls, desc="Processing playlists"):
            videos, next_page_token = [], None
            while True:
                request = youtube_object.playlistItems().list(part="snippet", playlistId=playlist_id, pageToken=next_page_token)
                response = execute_request(request)
                videos.extend([{
                    'title': item['snippet']['title'],
                    'video_id': item['snippet']['resourceId']['videoId'],
                    'video_url': f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}"
                } for item in response['items']])
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
            save_videos_to_csv(videos, playlist_title, folder='user_playlists')
            all_videos.extend(videos)
            processed_playlists.append((playlist_title, len(videos)))
    else:
        with yt_dlp.YoutubeDL({'extract_flat': True, 'no_retries': True, 'quiet': True, 'no_warnings': True}) as ydl:
            for playlist_url in tqdm(playlist_urls, desc="Processing playlists"):
                result = ydl.extract_info(playlist_url, download=False)
                if 'entries' in result:
                    playlist_title = result.get('title', 'Unknown Playlist')
                    videos = [{'title': video['title'], 'video_id': video['id'], 'video_url': video['url']}
                              for video in result['entries']]
                    all_videos.extend(videos)
                    save_videos_to_csv(videos, playlist_title, folder='public_playlists')
                    processed_playlists.append((playlist_title, len(videos)))

    for playlist_title, video_count in processed_playlists:
        print(f"\tProcessed {video_count} videos from playlist: '{playlist_title}'")

    print(f"Processed {len(all_videos)} videos in total from {len(processed_playlists)} playlist(s).")


def append_playlists_to_csv(directory_path, output_filename="_all_videos.csv"):
    df = pd.concat([pd.read_csv(os.path.join(directory_path, f)).assign(playlist=f) for f in os.listdir(directory_path) if f.endswith('.csv')], ignore_index=True)
    df.to_csv(os.path.join(directory_path, '..', output_filename), index=False)

    deleted_video_count = df['Title'].str.contains('Deleted video', case=False).sum()
    private_video_count = df['Title'].str.contains('Private video', case=False).sum()

    print(f"Deleted videos: {deleted_video_count}, Private videos: {private_video_count}")


def save_videos_to_csv(videos, playlist_title, folder='default_folder'):
    path = os.path.join(os.path.dirname(__file__), 'output', folder)
    os.makedirs(path, exist_ok=True)
    playlist_title = ''.join(c if c not in '/\\:*?"<>|; ' else '__' for c in playlist_title)
    try:
        with open(os.path.join(path, f'{playlist_title}__playlist.csv'), 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Video ID', 'Video URL'])
            writer.writerows([[video['title'], video['video_id'], video['video_url']] for video in videos])
    except Exception as e:
        print(f"Error saving CSV: {e}")


if __name__ == "__main__":
    playlists_list = []

    if playlists_list:
        get_playlist_video_details(playlists_list)
        append_playlists_to_csv(directory_path=os.path.join(os.path.dirname(__file__), 'output', 'public_playlists'), output_filename="public_playlists_videos.csv")
    else:
        youtube = authenticate_youtube()

        playlist_ids, playlist_titles, playlist_links = get_all_playlists(youtube)
        print(f"There are {len(set(playlist_ids))} unique playlists for this YouTube account.")

        get_playlist_video_details(list(zip(playlist_ids, playlist_titles)), youtube)

        append_playlists_to_csv(directory_path=os.path.join(os.path.dirname(__file__), 'output', 'user_playlists'), output_filename="user_playlists_videos.csv")
