import pandas as pd

def clean_yt(df):
    # turn column names lowercase
    df.columns = [col.lower() for col in df.columns]

    # clean strings
    if 'title' in df.columns:
        df['title'] = df['title'].fillna('').astype(str).str.strip()
    else:
        df['title'] = ''

    if 'description' in df.columns:
        df['description'] = df['description'].fillna('').astype(str).str.strip()
    else:
        df['description'] = ''

    # standardize timestamps
    timestamp_cols = ['publishedat', 'publish_time', 'timestamp', 'created_time']
    ts_col = next((col for col in timestamp_cols if col in df.columns), None)
    if ts_col:
        df['timestamp'] = pd.to_datetime(df[ts_col], errors='coerce')
    else:
        df['timestamp'] = pd.NaT

    return df


def clean_insta(df):
    columns_to_keep = [
        'id',
        'ownerUsername',
        'timestamp',
        'likesCount',
        'mentions',
        'commentsCount',
        'videoPlayCount',
        'url',
        'caption'
    ]
    df = df.loc[:, df.columns.intersection(columns_to_keep)].copy()

    # standardizing names
    df = df.rename(columns={
        'likesCount': 'likes',
        'commentsCount': 'comments',
        'videoPlayCount': 'views',
        'caption': 'description',
        'url': 'url',
        'mentions': 'mentions',
        'timestamp': 'published_at',
        'ownerUsername': 'author',
        'id': 'post_id'
    })

    # fill nan views
    df['views'] = df['views'].fillna(0).astype(int)
    df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce')

    # nan, int cast
    df['likes'] = df['likes'].fillna(0).astype(int)
    df['comments'] = df['comments'].fillna(0).astype(int)

    return df.reset_index(drop=True)


def add_engagement_rates(df):
    # avoid div 0
    df['views_nozero'] = df['views'].replace(0, pd.NA)

    df['like_rate'] = (df['likes'] / df['views_nozero']).fillna(0)
    df['comment_rate'] = (df['comments'] / df['views_nozero']).fillna(0)
    df['engagement_rate'] = ((df['likes'] + df['comments']) / df['views_nozero']).fillna(0)

    # del temp col
    df.drop(columns=['views_nozero'], inplace=True)

    return df
