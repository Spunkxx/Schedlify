# import cloudinary
from decouple import config
import cloudinary.uploader

cloudinary.config(
    cloud_name = config("CLOUD_NAME"),
    api_key = config("API_KEY"),
    api_secret = config("API_SECRET")
)

def upload_to_cloudinary(content: bytes, content_type: str = 'image', is_url: bool = False):
    
    if content_type not in ['image', 'video']:
        raise ValueError("Invalid content_type. Choose between 'image' or 'video'.")
    
    upload_params = {"resource_type" : content_type}
    
    if is_url:
        upload_params['file'] = content
    else:
        upload_params['file'] = content
    
    try:
        upload_result = cloudinary.uploader.upload(**upload_params)
        return upload_result['secure_url']
    except Exception as e:
        raise Exception(f"Error uploading to Cloudinary: {e}")