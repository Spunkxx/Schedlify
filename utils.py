# from configs import settings as fb_conf
# import requests
# import logging

# logger = logging.getLogger(__name__)

 
# fb_page_token = fb_conf.FB_PAGE_TOKEN
# fb_page_id = fb_conf.FB_PAGE_ID
# fb_feed = fb_conf.FB_FEED


# def post_text(
#     message: str, 
#     link: str = None,
#     published: bool = True,
#     scheduled_time: int = None          
# ):
#     url = fb_feed.format(page_id=fb_page_id)
#     headers = {"Content-Type": "application/json"}
    
#     payload = {
#         "access_token": fb_page_token,
#         "message": message,
#         "published": published
#     }
    
#     if link:
#         payload["link"] = link
        
#     if not published and scheduled_time:
#         print(f"Scheduled time: {scheduled_time}")
#         payload["scheduled_publish_time"] = scheduled_time
        
        
        
#     response = requests.post(url, headers=headers, json=payload)
    
#     if response.status_code != 200:
#         logger.error(f"Failed to post to Facebook. Details: {response.text}")
#         raise ValueError(f"Failed to post to Facebook. Status Code: {response.status_code}")
    
#     pass