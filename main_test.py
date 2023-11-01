# from fastapi import FastAPI, HTTPException
# import logging
# from datetime import datetime
# import pytz
# import time

# from worker import job_to_run

# app = FastAPI()
# logger = logging.getLogger(__name__)



# @app.post("/schedule_post_text_test/")
# async def schedule_post_test(
#     message: str, 
#     post_time: str,
#     link: str = None
# ):
#     try:
#         post_datetime = datetime.strptime(post_time, '%Y-%m-%d %H:%M:%S')
#         now = datetime.now()
#         delay = (post_datetime - now).total_seconds()  # Calculate the delay in seconds
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'.")

#     # time.sleep(delay)  # Wait for the desired time

#     job_to_run.apply_async(args=[message, link, True], countdown=delay)

#     return {"status": "posted", "message": message, "post_time": post_time}
