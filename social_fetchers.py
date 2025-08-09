import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
APIFY_TOKEN = os.getenv("APIFY_TOKEN")

APIFY_BASE_URL = "https://api.apify.com/v2/actor-tasks"

PLATFORM_TASK_IDS = {
    "instagram": "edgy_bachelor~instagram-scraper-task",
    "tiktok": "edgy_bachelor~tiktok-data-extractor-task",
}

def prepare_input(platform, usernames, max_posts=20):
    platform = platform.lower()
    if platform == "instagram":
        urls = [f"https://www.instagram.com/{u}/" for u in usernames]
        return {
            "addParentData": False,
            "directUrls": urls,
            "enhanceUserSearchWithFacebookPage": False,
            "isUserReelFeedURL": False,
            "isUserTaggedFeedURL": False,
            "resultsLimit": max_posts,
            "resultsType": "posts",
            "searchLimit": 1,
            "searchType": "hashtag",
        }
    elif platform == "tiktok":
        return {
            "excludePinnedPosts": False,
            "profileScrapeSections": ["videos"],
            "profileSorting": "latest",
            "profiles": usernames,
            "resultsPerPage": max_posts,
            "shouldDownloadCovers": False,
            "shouldDownloadSlideshowImages": False,
            "shouldDownloadSubtitles": False,
            "shouldDownloadVideos": False,
        }
    else:
        raise ValueError(f"Unsupported platform: {platform}")


def start_actor(task_id, input_data):
    """
    Start Apify actor with unique id task_id, dict input_data (what to scrape).
    Returns run id.
    """
    url = f"{APIFY_BASE_URL}/{task_id}/runs" # doc
    headers = {"Authorization": f"Bearer {APIFY_TOKEN}"}
    response = requests.post(url, json={"body": input_data}, headers=headers)
    response.raise_for_status() # errors if connection has bad status
    return response.json()["data"]["id"]

def wait_for_run(task_id, run_id, timeout=300, interval=5):
    """
    Periodically checks status of async task and returns data or timeout error.
    Returns run details, link to output.
    """
    APIFY_RUNS_BASE_URL = "https://api.apify.com/v2/actor-runs"
    url = f"{APIFY_RUNS_BASE_URL}/{run_id}"
    headers = {"Authorization": f"Bearer {APIFY_TOKEN}"}
    max_attempts = timeout // interval

    for _ in range(max_attempts):
        response = requests.get(url, headers=headers)
        response.raise_for_status() # check connection
        data = response.json()["data"]
        status = data["status"]
        if status == "SUCCEEDED":
            return data
        elif status == "FAILED":
            raise Exception("Actor run failed")
        time.sleep(interval)

    raise TimeoutError(f"Actor run did not finish within {timeout} seconds.")


def fetch_social_media_data(platform, usernames, max_posts=20):
    """
    Fetch recent posts from a given platform (instagram, tiktok) for usernames list.
    """
    platform = platform.lower()
    if platform not in PLATFORM_TASK_IDS:
        raise ValueError(f"Unsupported platform: {platform}")

    task_id = PLATFORM_TASK_IDS[platform]
    input_data = prepare_input(platform, usernames, max_posts)
    run_id = start_actor(task_id, input_data)
    data = wait_for_run(task_id, run_id)
    dataset_id = data.get("defaultDatasetId")
    if not dataset_id:
        raise Exception("No dataset found for this run.")

    dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?clean=1&format=json"
    headers = {"Authorization": f"Bearer {APIFY_TOKEN}"}
    resp = requests.get(dataset_url, headers=headers)
    resp.raise_for_status()

    items = resp.json()
    df = pd.json_normalize(items)
    return df