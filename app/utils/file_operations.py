from fastapi import UploadFile
from pathlib import Path
import logging
# import uuid
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMP_DIR = BASE_DIR / "temp"
FINAL_OUTPUT_DIR = BASE_DIR / "final_output"

# logging.info(f"Base directory: {BASE_DIR}")
# logging.info(f"Temporary directory: {TEMP_DIR}")
# logging.info(f"Final output directory: {FINAL_OUTPUT_DIR}")


TEMP_DIR.mkdir(parents=True, exist_ok=True)
FINAL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


async def save_upload_file(video_file: UploadFile) -> Path:
    """Save the uploaded file to the temporary directory with a unique name."""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{timestamp}_{video_file.filename}"
    temp_file_path = TEMP_DIR / unique_filename
    with temp_file_path.open('wb') as buffer:
        buffer.write(await video_file.read())
        logging.info(f"Saved file {unique_filename} to temp directory.")
    return temp_file_path



def remove_temp_files(*file_paths):
    """Removes temporary files given their file paths."""
    for file_path in file_paths:
        try:
            file_path = Path(file_path) 
            if file_path.exists():
                file_path.unlink()
                logging.info(f"Removed temp file {file_path.name}.")
        except Exception as e:
            logging.error(f"Error removing file {file_path}: {e}")

def cleanup_final_output(keep_file_name: str):
    """Remove all files from the final output directory except the specified file."""
    for output_file in FINAL_OUTPUT_DIR.iterdir():
        if output_file.is_file():
            if output_file.name != keep_file_name:
                try:
                    output_file.unlink()
                    logging.info(f"Deleted file: {output_file.name}")
                except Exception as e:
                    logging.error(f"Error deleting file {output_file.name}: {e}")
            else:
                logging.info(f"Keeping file: {output_file.name}")
                
