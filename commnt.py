from googleapiclient.discovery import build
import re
import csv
import time
import json

# --- Configuration ---
API_KEY = 'AIzaSyBm2txz83DWABe3NPnKSIDRe8ZOBSBuMhk'  # Replace with your key
VIDEO_ID = 'c7Jld02-d1w'  # Replace with your video ID

# --- YouTube API Setup ---
youtube = build('youtube', 'v3', developerKey=API_KEY)

# --- Regex Patterns ---
sinhala_pattern = re.compile(r'[\u0D80-\u0DFF]')
clean_pattern = re.compile(r'[^\u0D80-\u0DFF\s]')

# --- Clean Sinhala Text ---
def clean_sinhala_text(text):
    cleaned = clean_pattern.sub('', text)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

# --- Get Sinhala Comments ---
def get_sinhala_comments(video_id):
    sinhala_comments = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part='snippet,replies',
            videoId=video_id,
            pageToken=next_page_token,
            maxResults=100,
            textFormat='plainText'
        )
        response = request.execute()

        for item in response['items']:
            top_comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            if sinhala_pattern.search(top_comment):
                cleaned = clean_sinhala_text(top_comment)
                if cleaned:
                    sinhala_comments.append(cleaned)

            if 'replies' in item:
                for reply in item['replies']['comments']:
                    reply_text = reply['snippet']['textDisplay']
                    if sinhala_pattern.search(reply_text):
                        cleaned_reply = clean_sinhala_text(reply_text)
                        if cleaned_reply:
                            sinhala_comments.append(cleaned_reply)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

        time.sleep(0.1)

    return sinhala_comments

# --- Run and Save ---
comments = get_sinhala_comments(VIDEO_ID)

# Save as JSON (Array Format)
json_array = [{"data": {"text": comment}} for comment in comments if comment.strip()]
json_filename = f"sinhala_comments_{VIDEO_ID}_labelstudio.json"
with open(json_filename, 'w', encoding='utf-8') as f:
    json.dump(json_array, f, ensure_ascii=False, indent=2)

print(f"✅ Exported {len(json_array)} Sinhala comments to {json_filename} (JSON array for Label Studio)")
