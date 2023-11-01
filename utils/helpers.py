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
    if video_url:
        return requests.get(video_url).content
    elif video_file:
        return video_file.read()
    else:
        raise ValueError("Either video_url or video_file must be provided.")


    
def post_to_facebook(video_post_data, description, link=None):
    """Post video to Facebook after successful upload."""
    
    video_id = video_post_data.get('video_id')
    
    if not video_id:
        raise ValueError(f"Failed to review video ID. Response data: {video_post_data}")
    
    post_url = fb_video
    
    payload = {
        "access_token": fb_page_token,
        "attached_media": '[{"media_fbid":"'+ video_id +'"}]',
        "message": description
    }
    
    if link:
        payload['link'] = link
        # message += f"\n\n{link}"
        
    response = requests.post(post_url, data=payload)
    response.raise_for_status()

def post_resumable_video(description, video_url=None, video_file=None, link=None, chunk_size=1048576, max_retries=3):
    
    def exponential_backoff_retry(func, stage, *args, **kwargs):
        delay = 10  # Initial delay in seconds
        last_exception = None
        for attempt in range(max_retries):
            try:
                result = func(*args, **kwargs)
                if stage == "post_to_facebook" and not result.get("video_id"):
                    raise ValueError(f"Failed to retrieve video ID. Response data: {result}")
                return result
            except Exception as e:
                last_exception = e
                print(f"[{stage.upper()}] Failed on attempt {attempt + 1}. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
        print(f"[{stage.upper()}] Failed after {max_retries} attempts. Last error: {last_exception}")
        raise last_exception
    
    # Fetch video data
    video_data = fetch_video_data(video_url, video_file)
    video_size = len(video_data)


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
    time.sleep(10)  # Adding a delay after the last chunk is uploaded
    video_post_data = exponential_backoff_retry(end_upload_session, "end_upload_session", upload_session_id, fb_page_token)


    # Post to Facebook with retry
    result = exponential_backoff_retry(post_to_facebook, "post_to_facebook", video_post_data, description, link)
    if result.get("video_id"):
        print(f"Video successfully posted with video ID: {result['video_id']}")