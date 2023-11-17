# from fastapi import UploadFile
# from pathlib import Path
# from datetime import datetime
# from moviepy.editor import VideoFileClip

# BASE_DIR = Path(__file__).resolve().parent.parent.parent
# TEMP_DIR = BASE_DIR / "temp"
# FINAL_OUTPUT_DIR = BASE_DIR / "final_output"

# TEMP_DIR.mkdir(parents=True, exist_ok=True)
# FINAL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# def save_upload_file(video_file: UploadFile) -> Path:
#     """Save the uploaded file to the temporary directory with a unique name."""
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     unique_filename = f"{timestamp}_{video_file.filename}"
#     temp_file_path = TEMP_DIR / unique_filename
#     with temp_file_path.open('wb') as buffer:
#         buffer.write(video_file.file.read())
#     return temp_file_path

# def remove_temp_files(*file_paths):
#     """Removes temporary files given their file paths."""
#     for file_path in file_paths:
#         try:
#             file_path = Path(file_path)
#             if file_path.exists():
#                 file_path.unlink()
#         except Exception as e:
#             print(f"Error removing file {file_path}: {e}")

# def cleanup_final_output(keep_file_name: str):
#     """Remove all files from the final output directory except the specified file."""
#     for output_file in FINAL_OUTPUT_DIR.iterdir():
#         if output_file.is_file():
#             if output_file.name != keep_file_name:
#                 try:
#                     output_file.unlink()
#                 except Exception as e:
#                     print(f"Error deleting file {output_file.name}: {e}")

# def apply_aspect_ratio(video_path: str, aspect_ratio: str, output_path: str) -> None:
#     clip = VideoFileClip(video_path)
#     target_width, target_height = map(int, aspect_ratio.split(':'))
#     processed_clip = clip.resize(width=target_width)
#     processed_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', preset='fast', threads=4)

# # Example usage
# uploaded_file = UploadFile(...)
# temp_file_path = save_upload_file(uploaded_file)
# final_output_path = FINAL_OUTPUT_DIR / f"processed_{uploaded_file.filename}"

# apply_aspect_ratio(temp_file_path, "16:9", final_output_path)

# # Cleanup temporary files
# remove_temp_files(temp_file_path)
