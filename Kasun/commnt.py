from googleapiclient.discovery import build
import re
import csv
import time

API_KEY = 'AIzaSyBm2txz83DWABe3NPnKSIDRe8ZOBSBuMhk'
VIDEO_ID = 'JijlkFwbhWU'

youtube = build('youtube', 'v3', developerKey=API_KEY)

# Regex for Sinhala unicode block
sinhala_pattern = re.compile(r'[\u0D80-\u0DFF]')

# Regex to remove emojis and unwanted characters:
# Keep Sinhala letters (\u0D80-\u0DFF), spaces, and optionally basic punctuation
clean_pattern = re.compile(r'[^\u0D80-\u0DFF\s]')

def clean_sinhala_text(text):
    # Remove all characters except Sinhala letters and spaces
    cleaned = clean_pattern.sub('', text)
    # Replace multiple spaces with a single space
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

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
            # Top-level comment
            top_comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            if sinhala_pattern.search(top_comment):
                cleaned_comment = clean_sinhala_text(top_comment)
                if cleaned_comment:
                    sinhala_comments.append(cleaned_comment)

            # Replies
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

comments = get_sinhala_comments(VIDEO_ID)

# Save to CSV
filename = f"sinhala_comments_{VIDEO_ID}.csv"
with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Index', 'Sinhala Comment'])
    for idx, comment in enumerate(comments, 1):
        writer.writerow([idx, comment])

print(f"✅ Extracted and cleaned {len(comments)} Sinhala comments to {filename}")