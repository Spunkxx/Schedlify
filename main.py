from fastapi import FastAPI, UploadFile, Form, HTTPException
import os
from api import facebook, instagram, tiktok, youtube, pinterest, twitter, linkedin
from tests.test_scheduler import post_video_to_facebook


app = FastAPI()



app.include_router(facebook.router, prefix="/facebook", tags=["Facebook"])
# app.include_router(instagram.router, prefix="/instagram", tags=["Instagram"])



# @app.post("/post_video")
# async def post_video_endpoint(title: str = Form(...), description: str = Form(...), video_file: UploadFile = Form(...)):
#     try:
#         video_path = video_file.filename
#         with open(video_path, "wb") as buffer:
#             buffer.write(video_file.file.read())

#         post_video_to_facebook(video_path, title, description)
#         os.remove(video_path)  # Remove the video file after posting
#         return {"status": "success", "message": "Video posted successfully!"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
