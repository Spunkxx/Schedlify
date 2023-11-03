from celery import Celery
import logging
import base64
from io import BytesIO

from utils.helpers import post_text, post_image,post_resumable_video,publish_reel

# Celery setup
celery_app = Celery('tasks', broker='redis://localhost:6379/0')
celery_app.config_from_object('configs.celery_config')

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def job_to_run_text(self, message: str, unix_timestamp: float, link: str = None):
    """Celery task to post text content to Facebook."""
    logger.info("Starting the text content post job.")
    try:
        post_text(message, unix_timestamp, link)
        logger.info("Successfully posted text content on Facebook from Celery task.")
    except Exception as e:
        logger.error(f"Failed to post text content from Celery task: {e}")
        # Optionally, we can update the task state if necessary
        self.update_state(state='FAILURE', meta=str(e))

@celery_app.task(bind=True)
def job_to_run_image(self, message: str, link: str = None, image_url: str = None, image_file_path: str = None):
    """Celery task to post image content to Facebook."""
    logger.info("Starting the image content post job.")
    try:
        if image_file_path:
            post_image(message=message, image_file=image_file_path, link=link)
        else:
            post_image(message=message, image_url=image_url, link=link)
        logger.info("Successfully posted image content on Facebook from Celery task.")
    except Exception as e:
        logger.error(f"Failed to post image content from Celery task: {e}")
        # Optionally, we can update the task state if necessary
        self.update_state(state='FAILURE', meta=str(e))


@celery_app.task()
def job_to_run_video(description: str, title: str, video_url=None, video_content_encoded: bytes = None, link: str = None):
    """Post video content to Facebook using a Celery task."""
    logger.info("Starting the video content post job.")
    
    video_file = None
    
    if video_content_encoded:
        video_content_bytes = base64.b64decode(video_content_encoded)
        video_file = BytesIO(video_content_bytes)
    
    try:
        post_resumable_video(description=description, title=title, video_url=video_url, video_file=video_file, link=link)
        logger.info("Successfully posted video content on Facebook from Celery task.")
        print(f"Posting with description: {description}")
    except Exception as e:
        logger.error(f"Failed to post video content on Facebook from Celery task: {e}")
  
    
            
@celery_app.task()
def job_to_run_reel(description: str, video_url=None, reel_content_encoded: bytes = None):
    """Post reel content to Facebook using a Celery task."""
    logger.info("Starting the reel content post job.")

    reel_file = None

    if reel_content_encoded:
        reel_content_bytes = base64.b64decode(reel_content_encoded)
        reel_file = BytesIO(reel_content_bytes)

    try:
        publish_reel(description=description, reel_file=reel_file, video_url=video_url)
        logger.info("Successfully posted reel content on Facebook from Celery task.")
    except Exception as e:
        logger.error(f"Failed to post reel content on Facebook from Celery task: {e}")
    