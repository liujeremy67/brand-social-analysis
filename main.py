# main.py

import os
import pandas as pd
from dotenv import load_dotenv
from youtube_scraper import get_youtube_channel_videos
from social_fetchers import fetch_social_media_data
from categorizer import categorize_batch
from data_cleaner import *

load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

CHANNELS = {
    "Nike": "UCUFgkRb0ZHc4Rpq15VRCICA",
    "Adidas": "UCuLUOxd7ezJ8c6NSLBNRRfg"
}

CATEGORIES = [
    "Product Spotlight",
    "Athlete Feature",
    "Training and Fitness Tips",
    "Lifestyle and Culture",
]


def save_df(df, filename):
    """
    Save a pandas DataFrame to CSV with UTF-8 encoding and index disabled.
    
    Args:
        df (pd.DataFrame): DataFrame to save.
        filename (str): Output CSV filename.
    """
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"[INFO] Saved DataFrame to {filename}")


def process_platform_data(api_key, yt_channels, social_accounts, categories, platform_names, output_name_prefix):
    # print("[INFO] Fetching YouTube data...")
    # yt_dfs = get_youtube_channel_videos(api_key, channel_ids=yt_channels)  # dict: channel_id → df

    # # clean + add engagement rates for yt
    # for channel_id, df in yt_dfs.items():
    #     print(f"[INFO] Cleaning YouTube data for channel {channel_id}...")
    #     df_clean = clean_yt(df)
    #     df_clean = add_engagement_rates(df_clean)
        
    #     print(f"[INFO] Categorizing YouTube content for channel {channel_id}...")
    #     df_clean['category'] = categorize_batch(
    #         df_clean['title'] + " " + df_clean['description'], 
    #         categories
    #     )
    
    #     filename = f"{output_name_prefix}_youtube_channel_{channel_id}.csv"
    #     save_df(df_clean, filename)

    # same for social data
    social_dfs = {}
    for platform_name in platform_names:
        print(f"[INFO] Fetching social data for {platform_name}...")
        df = fetch_social_media_data(platform_name, social_accounts)

        print(f"[INFO] Cleaning {platform_name} data...")
        if platform_name == "instagram":
            df = clean_insta(df)
            df = add_engagement_rates(df)
        else:
            continue # tiktok not added yet TODO

        print(f"[INFO] Categorizing {platform_name} content...")
        df['category'] = categorize_batch(
            df['description'],
            categories
        )
        
        social_dfs[platform_name] = df
        
        # Save individually
        save_df(df, f"{output_name_prefix}_{platform_name}_clean.csv")

    print("[SUCCESS] Data processing complete for YouTube and social platforms.")
    return social_dfs #, yt_dfs



def main():
    process_platform_data(
        api_key=API_KEY,
        yt_channels=[CHANNELS["Adidas"], CHANNELS["Nike"]],
        social_accounts=["adidas", "nike"],
        categories=CATEGORIES,
        platform_names=["instagram"],  # TODO ADD TIKTOK
        output_name_prefix="all_platforms"
    )


if __name__ == "__main__":
    main()
