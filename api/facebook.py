from fastapi import HTTPException, APIRouter, UploadFile, File
from datetime import datetime
from typing import Optional
from io import BytesIO
import base64

from tasks.celery_tasks import job_to_run_text, job_to_run_image, job_to_run_video
from utils.cloudinary_utils import upload_to_cloudinary

router = APIRouter()

def compute_delay(post_time: str) -> float:
    try:
        post_datetime = datetime.strptime(post_time, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        return (post_datetime - now).total_seconds()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'.")

@router.post("/schedule_post_text/")
async def schedule_post_text(message: str, post_time: str, link: str = None):
    delay = compute_delay(post_time)
    job_to_run_text.apply_async(args=[message, link, True], countdown=delay)
    return {"status": "posted", "message": message, "post_time": post_time}

@router.post("/schedule_post_image")
async def schedule_post_image(message: str, post_time: str, image_url: Optional[str] = None, image_file: UploadFile = File(None, description="Upload an Image File"), link: str = None):
    
    delay = compute_delay(post_time)
    
    if image_file and image_url:
        raise HTTPException(status_code=400, detail="Please provide either an image_url or image_file, not both.")
    
    if not image_file and not image_url:
        raise HTTPException(status_code=400, detail="Either an image_url or image_file must be provided.")
    
    if image_file:
        image_content = await image_file.read()
        image_url = upload_to_cloudinary(image_content)

    job_to_run_image.apply_async(args=[message, link, image_url], countdown=delay)
    return {"status": "scheduled", "message": message, "post_time": post_time, "image_url": image_url}


@router.post("/schedule_post_video")
async def schedule_post_video(message: str, post_time: str, video_url: Optional[str] = None, video_file: UploadFile = File(None, description="Upload an Video file"), link: str= None ):
    
    delay = compute_delay(post_time)
    
    video_content_encoded = None  # Set a default value for video_content_encoded
    
    if video_file:
        video_content = BytesIO(await video_file.read()).getvalue() # Getting bytes from BytesIO for Celery task
        video_content_encoded = base64.b64encode(video_content).decode('utf-8')  # Encode the video content to base64 string

    elif not video_url:
        raise HTTPException(status_code=400, detail="Either a video_url or video_file must be provided.")
    
    job_to_run_video.apply_async(args=[message, video_url, video_content_encoded, link], countdown=delay)
    return {"status": "scheduled", "message": message, "post_time": post_time, "video_url": video_url}
