# from fastapi import UploadFile
# from app.utils.moviepy_utils import get_video_quality, apply_aspect_ratio, reduce_video_quality
# from app.utils.moviepy_operations import remove_temp_files, TEMP_DIR, FINAL_OUTPUT_DIR
# from app.utils.enums import VideoQuality
# import logging
# from datetime import datetime

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# async def handle_video_upload(video: UploadFile, aspect_ratio: str, quality: VideoQuality) -> dict:
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     temp_filename = f"{timestamp}_{video.filename}"
#     temp_path = TEMP_DIR / temp_filename
#     final_output_filename = f"final_{timestamp}_{video.filename}"
#     final_output_path = FINAL_OUTPUT_DIR / final_output_filename
#     reduced_quality_filename = f"reduced_{final_output_filename}"
#     reduced_quality_output_path = FINAL_OUTPUT_DIR / reduced_quality_filename

#     try:
#         # Save the uploaded file to the temporary directory
#         with open(temp_path, "wb") as f:
#             f.write(await video.read())

#         # Get the original video quality
#         original_quality = get_video_quality(temp_path)

#         # Apply aspect ratio if specified
#         if aspect_ratio:
#             apply_aspect_ratio(temp_path, aspect_ratio, final_output_path)
#         else:
#             final_output_path = temp_path

#         # Determine the bitrate based on quality option
#         bitrate = '2000k' if quality == VideoQuality.HIGH else '1000k' if quality == VideoQuality.MEDIUM else '500k'

#         # Reduce video quality
#         reduce_video_quality(final_output_path, reduced_quality_output_path, bitrate)

#         return {
#             "original_quality": original_quality,
#             "output_file": reduced_quality_output_path
#         }
#     finally:
#         # Clean up temporary and original files
#         remove_temp_files(temp_path, final_output_path)
#         logging.info(f"Cleaned up temporary and original files.")
