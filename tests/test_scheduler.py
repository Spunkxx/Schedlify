import requests
import time
import os

# Constants (replace these with your actual values)
FB_PAGE_TOKEN = 'EAAEyKgTjQzcBO24mRZCZC8cGTXdWEQxN2hRXP71HrgqG5YZBBWkbgai51FJFJhTRZBBXPAaDFEJ3UAbSeGVtcty0AU1ZCz2h5LyI5oqqgZBneEyzj5z61jSyKnYUndeOlc6wtoh3cH3wYtHzX6uKmvNh8aaStSJVuxZBRM7UTWdLzCJNvTZCb1XgZC3us4PgyYecZD'
FB_PAGE_ID = '152395871282160'
FB_VIDEO_URL = f'https://graph.facebook.com/v13.0/{FB_PAGE_ID}/videos' # Adjust version if necessary

def post_video_to_facebook(video_path, title, description):
    # Step 1: Initialize video session
    video_size = os.path.getsize(video_path)
    init_payload = {
        "upload_phase": "start",
        "access_token": FB_PAGE_TOKEN,
        "file_size": video_size
    }
    init_response = requests.post(FB_VIDEO_URL, data=init_payload)
    init_data = init_response.json()
    
    upload_session_id = init_data["upload_session_id"]
    start_offset = int(init_data["start_offset"])
    end_offset = int(init_data["end_offset"])
    
    # Step 2: Upload the video in chunks
    with open(video_path, 'rb') as f:
        while start_offset < video_size:
            f.seek(start_offset)
            chunk = f.read(end_offset - start_offset)
            
            chunk_payload = {
                "upload_phase": "transfer",
                "upload_session_id": upload_session_id,
                "access_token": FB_PAGE_TOKEN,
                "start_offset": start_offset
            }
            
            chunk_response = requests.post(FB_VIDEO_URL, data=chunk_payload, files={"video_file_chunk": chunk})
            chunk_data = chunk_response.json()
            
            start_offset = int(chunk_data["start_offset"])
            end_offset = int(chunk_data["end_offset"])
    
    # Step 3: Finalize the upload
    finish_payload = {
        "upload_phase": "finish",
        "upload_session_id": upload_session_id,
        "access_token": FB_PAGE_TOKEN
    }
    finish_response = requests.post(FB_VIDEO_URL, data=finish_payload)
    finish_data = finish_response.json()
    video_id = finish_data.get('video_id')
    
    if not video_id:
        print("Failed to get video ID after uploading.")
        return

    # Step 4: Post the video with title and description
    post_payload = {
        "access_token": FB_PAGE_TOKEN,
        "title": title,
        "description": description,
        "attached_media": f'[{{"media_fbid":"{video_id}"}}]'
    }
    post_response = requests.post(FB_VIDEO_URL, data=post_payload)
    
    if post_response.status_code == 200:
        print(f"Successfully posted video with title: {title} and description: {description}")
    else:
        print(f"Failed to post video. Error: {post_response.text}")

if __name__ == "__main__":
    video_path = "path_to_your_video.mp4"  # Replace with your video path
    title = "Your Video Title"
    description = "Your Video Description"
    post_video_to_facebook(video_path, title, description)
