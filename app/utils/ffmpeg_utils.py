import subprocess
import json
import cv2
import numpy as np
import logging
from pathlib import Path

def get_video_quality(video_path: str) -> dict:
    cmd = [
        'ffprobe', '-v', 'quiet', '-print_format', 'json',
        '-show_format', '-show_streams', video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return json.loads(result.stdout)


def reduce_video_quality(video_path: str, output_path: str, bitrate: str = '800k') -> None:
    cmd = [
        'ffmpeg', '-i', video_path, '-b:v', bitrate, '-maxrate', bitrate, '-bufsize', '1000k', output_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    

def compare_video_quality(original_path: str, processed_path: str):
    # Get the quality information for both videos
    original_quality = get_video_quality(original_path)
    processed_quality = get_video_quality(processed_path)

    # Extract bitrate and resolution
    original_bitrate = int(original_quality['format']['bit_rate'])
    processed_bitrate = int(processed_quality['format']['bit_rate'])

    original_resolution = (original_quality['streams'][0]['width'], original_quality['streams'][0]['height'])
    processed_resolution = (processed_quality['streams'][0]['width'], processed_quality['streams'][0]['height'])

    # Compare and print the results
    print(f"Original Bitrate: {original_bitrate}, Processed Bitrate: {processed_bitrate}")
    print(f"Original Resolution: {original_resolution}, Processed Resolution: {processed_resolution}")

    if processed_bitrate < original_bitrate:
        print("The bitrate has been reduced.")
    else:
        print("The bitrate has not been reduced.")

    if processed_resolution != original_resolution:
        print("The resolution has been changed.")
    else:
        print("The resolution remains the same.")


def get_video_size(video_path: str):
    cmd = [
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height', '-of', 'csv=s=x:p=0', video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    width, height = map(int, result.stdout.strip().split('x'))
    return width, height

def apply_aspect_ratio(video_path: str, aspect_ratio: str, output_path: str) -> None:

    target_width, target_height = map(int, aspect_ratio.split(':'))

    width, height = get_video_size(video_path)

    scale_width = width / target_width
    scale_height = height / target_height

    if scale_width > scale_height:
        # Horizontal padding
        pad = int(((width / target_width * target_height) - height) / 2)
        filter_string = f"pad={width}:{width//target_width*target_height}:(ow-iw)/2:{pad}"
        # filter_string = f"scale={width}:{new_height},pad={width}:{new_height}:{pad_top}:{pad_bottom}"
    else:
        # Vertical padding
        pad = int(((height / target_height * target_width) - width) / 2)
        filter_string = f"pad={height//target_height*target_width}:{height}:(ow-iw)/2:{pad}"
        
    logging.info(f"Filter string for FFmpeg: {filter_string}")

    cmd = [
        'ffmpeg', '-i', str(video_path), '-vf', filter_string, 
        '-c:v', 'libx264', '-preset', 'fast', 
         '-an',
        str(output_path)
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        # logging.info(f"FFmpeg command executed successfully for {video_path}")
    except subprocess.CalledProcessError as e:
        # logging.error(f"FFmpeg command failed: {e.stderr.decode()}")
        return json.loads(result.stdout)

    # if Path(output_path).exists():
    #     logging.info(f"Output file created successfully: {output_path}")
    # else:
    #     logging.error(f"Output file not created: {output_path}")
