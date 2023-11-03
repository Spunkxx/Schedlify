from configs import settings as fb_conf
from io import BytesIO
import requests
import logging
import time
# from utils.cloudinary_utils import upload_to_cloudinary



fb_page_token = fb_conf.FB_PAGE_TOKEN
fb_page_id = fb_conf.FB_PAGE_ID
fb_feed = fb_conf.FB_FEED
fb_photo = fb_conf.FB_PHOTO
fb_video = fb_conf.FB_VIDEO


FB_REELS_INIT = fb_conf.FB_REELS_INIT
FB_REELS_UPLOAD = fb_conf.FB_REELS_UPLOAD
FB_REELS_PUBLISH = fb_conf.FB_REELS_PUBLISH


logger = logging.getLogger(__name__)

def post_text(message: str, link: str = None, published: bool = True, scheduled_time: int = None):
    """Post text to Facebook page."""
    url = fb_feed.format(page_id=fb_page_id)
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "access_token": fb_page_token,
        "message": message,
        "published": published
    }

    if link:
        payload["link"] = link
        
    if not published and scheduled_time:
        logger.info(f"Scheduled time: {scheduled_time}")
        payload["scheduled_publish_time"] = scheduled_time
        
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        error_message = f"Failed to post to Facebook. Status Code: {response.status_code}. Details: {response.text}"
        logger.error(error_message)
        raise ValueError(error_message)

def post_image(message: str, image_url: str = None, link: str = None):
    """Post image with optional message to Facebook page."""
    if not image_url:
        raise ValueError("Please provide an Image_url")

    url = fb_photo.format(page_id=fb_page_id)
    
    if link:
        message += f"\n\n{link}"

    payload = {
        "access_token": fb_page_token,
        "message": message,
        'url': image_url
    }
    
    response = requests.post(url, data=payload)

    if response.status_code != 200:
        error_message = f"Failed to post to Facebook. Status Code: {response.status_code}. Details: {response.text}"
        logger.error(error_message)
        raise ValueError(error_message)

    return response.json()


"""Video Content Containers and Post Method"""

def initialize_upload(video_size, access_token):
    """Initialize video session"""
    
    url = fb_video.format(page_id=fb_page_id)
    payload = {
        "upload_phase": "start",
        "access_token": access_token,
        "file_size": video_size
    }
    
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()

def upload_video_chunk(upload_session_id, start_offset, video_chunk, access_token):
    """Upload a chunk of video during resumable video upload."""
    
    url = fb_video.format(page_id=fb_page_id)
    payload = {
        "upload_phase": "transfer",
        "upload_session_id": upload_session_id,
        "access_token": access_token,
        "start_offset": start_offset
    }
    
    files = {'video_file_chunk': video_chunk}
    
    response = requests.post(url, data=payload, files=files)
    response.raise_for_status()
    return response.json()

def end_upload_session(upload_session_id, access_token):
    """Finalize video upload session."""
    
    url = fb_video.format(page_id=fb_page_id)
    payload = {
        "upload_phase": "finish",
        "upload_session_id": upload_session_id,
        "access_token": access_token
    }

    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()

def fetch_video_data(video_url=None, video_file=None):
    """Retrieve video data from a URL or file."""
    
    if video_url:
        return BytesIO(requests.get(video_url).content)
    elif video_file:
        return BytesIO(video_file.read())
    else:
        raise ValueError("Either video_url or video_file must be provided.")

def post_to_facebook(video_post_data, description, title=None, link=None):
    video_id = video_post_data.get('video_id')
    if not video_id:
        print("No video_id found in the video_post_data. Unable to proceed.")
        return False

    post_url = fb_video
    params = {
        "access_token": fb_page_token,
        "description": description,  # Using description now
        "title": title,  # Added this line to set the title
        "attached_media": '[{"media_fbid":"' + video_id + '"}]'
    }

    if link:
        params['link'] = link

    response = requests.post(post_url, data=params)

    if response.status_code != 200:
        # Adding detailed logging
        logger.error(f"Failed to post to Facebook. Status Code: {response.status_code}. Content: {response.text}")
        return False

    # Assuming the post was successful, let's log the response for diagnosis
    logger.info(f"Posted to Facebook. Response: {response.text}")
    return True


# def post_resumable_video(description, video_url=None, video_file=None, title=None, link=None, chunk_size=1048576, max_retries=3):
    
#     def exponential_backoff_retry(func, stage, *args, **kwargs):
#         delay = 10  # Initial delay in seconds

#         print(f"Starting the {stage.replace('_', ' ')} job.")
    
#         for attempt in range(max_retries):
#             try:
#                 result = func(*args, **kwargs)
#                 if stage == "post_to_facebook" and not result:
#                     continue  # Skip this iteration and proceed to next retry
#                 print(f"Successfully completed {stage.replace('_', ' ')} on Facebook.")
#                 return result
#             except Exception as e:
#                 if attempt < max_retries - 1:  # Don't log if it's the last attempt
#                     time.sleep(delay)
#                     delay *= 2
#                 else:
#                     print(f"Failed to complete {stage.replace('_', ' ')} on Facebook: {e}")
#                     raise e
    
#     # Fetch video data
#     video_data = fetch_video_data(video_url, video_file)
#     video_size = len(video_data.getvalue())

#     # Initialize upload with retry
#     init_data = exponential_backoff_retry(initialize_upload, "initialize_upload", video_size, fb_page_token)
#     upload_session_id = init_data["upload_session_id"]
#     start_offset = int(init_data["start_offset"])
#     end_offset = int(init_data["end_offset"])

#     # Upload in chunks with retry
#     while start_offset < video_size:
#         video_data.seek(start_offset)
#         chunk = video_data.read(min(chunk_size, end_offset - start_offset))
#         upload_data = exponential_backoff_retry(upload_video_chunk, "upload_video_chunk", upload_session_id, start_offset, chunk, fb_page_token)
#         start_offset = int(upload_data["start_offset"])
#         end_offset = min(int(upload_data["end_offset"]), video_size)

#     # Finish the upload session with retry
#     print("[INFO] Waiting for Facebook to process video...")
#     time.sleep(10)
#     video_post_data = exponential_backoff_retry(end_upload_session, "end_upload_session", upload_session_id, fb_page_token)

#     # Post the video to Facebook using the data received after ending the upload session
#     posted = exponential_backoff_retry(post_to_facebook, "post_to_facebook", video_post_data, description, title, link)
#     if not posted:
#         print("Failed to post the video to Facebook after all retries.")

def post_resumable_video(description, video_url=None, video_file=None, title=None, link=None, chunk_size=1048576, max_retries=3):
    
    def exponential_backoff_retry(func, stage, *args, **kwargs):
        delay = 10  # Initial delay in seconds

        print(f"Starting the {stage.replace('_', ' ')} job.")
    
        for attempt in range(max_retries):
            try:
                result = func(*args, **kwargs)
                if stage == "post_to_facebook" and not result:
                    continue  # Skip this iteration and proceed to next retry
                print(f"Successfully completed {stage.replace('_', ' ')} on Facebook.")
                return result
            except Exception as e:
                if attempt < max_retries - 1:  # Don't log if it's the last attempt
                    time.sleep(delay)
                    delay *= 2
                else:
                    print(f"Failed to complete {stage.replace('_', ' ')} on Facebook: {e}")
                    raise e
    
    # Fetch video data
    video_data = fetch_video_data(video_url, video_file)
    video_size = len(video_data.getvalue())

    # Initialize upload with retry
    init_data = exponential_backoff_retry(initialize_upload, "initialize_upload", video_size, fb_page_token)
    upload_session_id = init_data["upload_session_id"]
    start_offset = int(init_data["start_offset"])
    end_offset = int(init_data["end_offset"])

    # Upload in chunks with retry
    while start_offset < video_size:
        video_data.seek(start_offset)
        chunk = video_data.read(min(chunk_size, end_offset - start_offset))
        upload_data = exponential_backoff_retry(upload_video_chunk, "upload_video_chunk", upload_session_id, start_offset, chunk, fb_page_token)
        start_offset = int(upload_data["start_offset"])
        end_offset = min(int(upload_data["end_offset"]), video_size)

    # Finish the upload session with retry
    print("[INFO] Waiting for Facebook to process video...")
    time.sleep(10)
    video_post_data = exponential_backoff_retry(end_upload_session, "end_upload_session", upload_session_id, fb_page_token)

    # Ensure 'video_id' is present before attempting to post the video
    if 'video_id' not in video_post_data:
        print("No video_id found in the video_post_data. Unable to proceed.")
        return None

    # Post the video to Facebook using the data received after ending the upload session
    posted = exponential_backoff_retry(post_to_facebook, "post_to_facebook", video_post_data, description, title, link)
    if not posted:
        print("Failed to post the video to Facebook after all retries.")

        



def initialize_reel_upload(access_token: str) -> dict:
    payload = {
        "upload_phase": "start",
        "access_token": access_token
    }
    response = requests.post(FB_REELS_INIT, data=payload)
    response.raise_for_status()
    return response.json()

def upload_reel_video(video_id: str, video_file: bytes, access_token: str) -> None:
    upload_url = FB_REELS_UPLOAD.format(video_id=video_id)
    headers = {
        "Authorization": f"OAuth {access_token}",
        "offset": "0",
        "file_size": str(len(video_file))
    }
    response = requests.post(upload_url, headers=headers, data=video_file)
    response.raise_for_status()

def upload_video_from_url(video_id: str, video_url: str, access_token: str) -> None:
    upload_url = FB_REELS_UPLOAD.format(video_id=video_id)
    headers = {
        "Authorization": f"OAuth {access_token}",
        "file_url": video_url
    }
    response = requests.post(upload_url, headers=headers)
    response.raise_for_status()


def publish_reel(description: str, reel_file: BytesIO, video_url: str = None) -> None:
    
    # Step 1: Initialize upload session
    init_data = initialize_reel_upload(fb_page_token)
    video_id = init_data.get("video_id")
    if not video_id:
        raise Exception("Failed to initialize video upload.")
    
    # Step 2: Upload the video
    if reel_file:
        reel_file.seek(0)  
        video_content = reel_file.read()
        upload_reel_video(video_id, video_content, fb_page_token)
    elif video_url:
        upload_video_from_url(video_id, video_url, fb_page_token)

    else:
        raise Exception("Either a reel file or a video URL must be provided.")

    # Step 3: Publish the reel
    payload = {
        "access_token": fb_page_token,
        "video_id": video_id,
        "upload_phase": "finish",
        "video_state": "PUBLISHED",
        "description": description
    }
    response = requests.post(FB_REELS_PUBLISH, data=payload)
    response.raise_for_status()