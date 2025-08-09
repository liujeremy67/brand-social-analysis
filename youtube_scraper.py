# scraper.py

import pandas as pd
from googleapiclient.discovery import build
from isodate import parse_duration

def get_youtube_channel_videos(api_key, channel_ids, max_results=50, max_videos=100):
    """
    Fetch videos from multiple YouTube channels and return a dict of DataFrames.

    Parameters:
        api_key (str): YouTube Data API key.
        channel_ids (list[str]): List of channel unique IDs.
        max_results (int): Max number of videos to fetch per API call (max=50).
        max_videos (int): Max total videos to fetch per channel.

    Returns:
        dict: {channel_id: pd.DataFrame} of video metadata per channel.
    """
    from googleapiclient.discovery import build
    import pandas as pd

    youtube = build('youtube', 'v3', developerKey=api_key)
    channel_videos = {}

    for channel_id in channel_ids:
        videos = []
        next_page_token = None

        # Get uploads playlist ID for this channel
        channel_response = youtube.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()
        uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        while True:
            playlist_response = youtube.playlistItems().list(
                part='snippet,contentDetails',
                playlistId=uploads_playlist_id,
                maxResults=max_results,
                pageToken=next_page_token
            ).execute()

            for item in playlist_response['items']:
                if len(videos) >= max_videos:
                    break

                video_id = item['contentDetails']['videoId']
                video_snippet = item['snippet']

                video_response = youtube.videos().list(
                    part='statistics,snippet,contentDetails',
                    id=video_id
                ).execute()

                video_data = video_response['items'][0]
                duration = parse_duration(video_data['contentDetails']['duration']).total_seconds()
                if duration <= 60:
                    continue

                videos.append({
                    'video_id': video_id,
                    'title': video_snippet['title'],
                    'description': video_snippet['description'],
                    'published_at': video_snippet['publishedAt'],
                    'views': int(video_data['statistics'].get('viewCount', 0)),
                    'likes': int(video_data['statistics'].get('likeCount', 0)),
                    'comments': int(video_data['statistics'].get('commentCount', 0)),
                    'url': f"https://www.youtube.com/watch?v={video_id}"
                })

            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token or len(videos) >= max_videos:
                break

        channel_videos[channel_id] = pd.DataFrame(videos)

    return channel_videos