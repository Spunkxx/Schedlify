from fastapi import FastAPI
from starlette.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import uvicorn
from app.api.video_router import router as video_router
from fastapi.middleware.cors import CORSMiddleware
import os


app = FastAPI()

load_dotenv()

VIDEO_DIRECTORY = os.getenv('VIDEO_DIRECTORY', default='D:/PCFiles/Desktop/Tools-back_end/final_output')
print("Video directory is set to:", VIDEO_DIRECTORY)

# Set up CORS middleware
origins = [
    "http://localhost:5173",  # Add your frontend origin here
    "http://localhost",  # Depending on your setup, you might need this
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)



app.include_router(video_router, prefix="/video", tags=["video"])

app.mount("/videos", StaticFiles(directory=VIDEO_DIRECTORY), name="videos")



@app.get("/videos/{filename}")
async def get_video(filename: str):
    file_path = f"{VIDEO_DIRECTORY}/{filename}"
    if os.path.exists(file_path):  # Check if the file exists
        return FileResponse(path=file_path)
    else:
        return {"detail": "File not found"}, 404

@app.get("/")
async def main():
    return RedirectResponse(url='/docs')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)