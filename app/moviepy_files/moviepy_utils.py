# from moviepy.editor import VideoFileClip, VideoClip
# from moviepy.video.fx.all import resize

# def get_video_quality(video_path: str) -> dict:
#     clip = VideoFileClip(video_path)
#     return {
#         'bit_rate': int(clip.bitrate),
#         'streams': [{'width': clip.size[0], 'height': clip.size[1]}]
#     }

# def reduce_video_quality(video_path: str, output_path: str, bitrate: str = '800k') -> None:
#     clip = VideoFileClip(video_path)
#     processed_clip = clip.set_bitrate(bitrate)
#     processed_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', bitrate=bitrate)

# def compare_video_quality(original_path: str, processed_path: str):
#     original_quality = get_video_quality(original_path)
#     processed_quality = get_video_quality(processed_path)

#     original_bitrate = original_quality['bit_rate']
#     processed_bitrate = processed_quality['bit_rate']

#     original_resolution = (original_quality['streams'][0]['width'], original_quality['streams'][0]['height'])
#     processed_resolution = (processed_quality['streams'][0]['width'], processed_quality['streams'][0]['height'])

#     print(f"Original Bitrate: {original_bitrate}, Processed Bitrate: {processed_bitrate}")
#     print(f"Original Resolution: {original_resolution}, Processed Resolution: {processed_resolution}")

#     if processed_bitrate < original_bitrate:
#         print("The bitrate has been reduced.")
#     else:
#         print("The bitrate has not been reduced.")

#     if processed_resolution != original_resolution:
#         print("The resolution has been changed.")
#     else:
#         print("The resolution remains the same.")

# def apply_aspect_ratio(video_path: str, aspect_ratio: str, output_path: str) -> None:
#     clip = VideoFileClip(video_path)

#     target_width, target_height = map(int, aspect_ratio.split(':'))

#     processed_clip = resize(clip, width=target_width)
#     processed_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', preset='fast', threads=4)

# # Example usage:
# original_path = "input_video.mp4"
# processed_path = "output_video.mp4"
# aspect_ratio = "16:9"
# output_path_aspect_ratio = "output_video_aspect_ratio.mp4"

# compare_video_quality(original_path, processed_path)

# apply_aspect_ratio(original_path, aspect_ratio, output_path_aspect_ratio)
