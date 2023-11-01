# from celery import Celery
# import logging
# from utils import post_text

# celery_app = Celery('worker', broker='redis://localhost:6379/0')
# celery_app.config_from_object('celery_config')


# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# @celery_app.task()
# def job_to_run(message: str, unix_timestamp: float, link: str = None):

#     logger.info("Starting the Job to run.")
#     try:
#         post_text(message, unix_timestamp, link)
#         logger.info("Successfully posted on Facebook from Celery task.")
#     except Exception as e:
#         logger.error(f"Failed to post from Celery task: {e}")

