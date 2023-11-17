from fastapi import APIRouter, UploadFile, HTTPException, File, Form, Query
from app.services.video_service import handle_video_upload
from app.utils.enums import AspectRatio
from app.utils.enums import VideoQuality
from moviepy.editor import VideoFileClip
from pathlib import Path
import os
import shutil

router = APIRouter()

VIDEO_DIRECTORY = Path(os.getenv('VIDEO_DIRECTORY', default='D:/PCFiles/Desktop/Tools-back_end/final_output'))

@router.post("/upload")
async def upload_video(
    video: UploadFile = File(...),
    aspect_ratio: AspectRatio = Form(default=None),
    quality: VideoQuality = Form(VideoQuality.HIGH)
):
    try:
        response = await handle_video_upload(video, aspect_ratio, quality)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/trim")
async def trim_video(
    start_time: str = Query(..., description="Format: HH:MM:SS"),
    end_time: str = Query(..., description="Format: HH:MM:SS"),
    video: UploadFile = File(...)
):
    try:
        # Save temporary video file
        temp_video_path = VIDEO_DIRECTORY / video.filename
        with open(temp_video_path, "wb") as temp_file:
            shutil.copyfileobj(video.file, temp_file)

        # Load video into moviepy and trim
        with VideoFileClip(str(temp_video_path)) as clip:
            # Validate start_time and end_time format before using them
            # ...

            trimmed_clip = clip.subclip(start_time, end_time)
            output_filename = f"trimmed_{video.filename}"
            output_path = VIDEO_DIRECTORY / output_filename
            trimmed_clip.write_videofile(str(output_path))

        # Optional: Delete the temporary file after processing
        temp_video_path.unlink()

        return {"trimmed_video": output_filename}
    except Exception as e:
        # Optional: Clean up if something goes wrong
        if temp_video_path.exists():
            temp_video_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))
