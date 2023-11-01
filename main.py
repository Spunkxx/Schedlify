from fastapi import FastAPI
from api import facebook, instagram, tiktok, youtube, pinterest, twitter, linkedin


app = FastAPI()



app.include_router(facebook.router, prefix="/facebook", tags=["Facebook"])
# app.include_router(instagram.router, prefix="/instagram", tags=["Instagram"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)