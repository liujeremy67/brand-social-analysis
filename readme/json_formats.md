YouTube API JSON Response Formats

PLAYLIST PAGE FORMAT
{
    "kind": "youtube#playlistItemListResponse",
    "etag": "...",
    "nextPageToken": "...", <- if theres another page
    "items": [ {...}, {...}, ... ], <- list of videos
    "pageInfo": { ... }
}

VIDEO FORMAT
{
    "kind": "youtube#playlistItem",
    "etag": "...",
    "id": "VVVCWlZvQzV1bnpob0VsVjNtUjJuMEZRU...etc",
    "snippet": { <- title, desc, other info etc
        "publishedAt": "2024-06-01T12:00:00Z",
        "title": "Nike Air Zoom Pegasus 40",
        "description": "The all-new...",
        "thumbnails": { ... },
        "resourceId": {
        "kind": "youtube#video",
        "videoId": "xYz123"
        }
    },
    "contentDetails": { <- technical
        "videoId": "xYz123",
        "videoPublishedAt": "2024-06-01T12:00:00Z"
    }
}

VIDEO STATS RESPONSE FORMAT
{
  "kind": "youtube#videoListResponse",
  "etag": "...",
  "items": [
    {
      "kind": "youtube#video",
      "etag": "...",
      "id": "xYz123",
      "snippet": {
        "title": "Nike Air Zoom Pegasus 40",
        "description": "The all-new...",
        "publishedAt": "2024-06-01T12:00:00Z",
        "tags": ["Nike", "Running"],
        ...
      },
      "statistics": {
        "viewCount": "54000",
        "likeCount": "1200",
        "commentCount": "230"
      }
    }
  ],
  "pageInfo": { ... }
}
