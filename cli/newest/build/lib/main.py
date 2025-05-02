#!/usr/bin/env python3

# from PIL import Image
# import imagehash
# import cv2
# import sys
# import os

# def compute_frame_phash(gray_frame):
#     pil_image = Image.fromarray(gray_frame)
    
#     phash = imagehash.phash(pil_image, hash_size=16, highfreq_factor=16)
#     return phash

# def preprocess_frame(frame, blur_kernel_size=(5, 5)):
#     """Preprocess the frame by converting to grayscale and applying Gaussian blur."""
#     try:
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     except cv2.error as e:
#         print(f"Error converting frame to grayscale: {e}")
#         print(f"Frame shape: {frame.shape}, Frame type: {type(frame)}")
#         return None
    
#     frame = cv2.GaussianBlur(frame, blur_kernel_size, 0)

#     return frame

# def get_frame_hashes(video_path):
#     cap = cv2.VideoCapture(video_path)
#     phash=[]

#     fps = cap.get(cv2.CAP_PROP_FPS)
#     print(f'FPS : {fps:0.2f}')

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         frame = preprocess_frame(frame)
#         phash.append(compute_frame_phash(frame))

#     cap.release()
#     return phash

# def get_video_bitrate(video_path):
#     result = subprocess.run([
#         "ffprobe", "-v", "error",
#         "-select_streams", "v:0",
#         "-show_entries", "stream=bit_rate",
#         "-of", "default=noprint_wrappers=1:nokey=1",
#         video_path
#     ], capture_output=True, text=True)
#     print("bitrate", int(result.stdout.strip()))
#     return int(result.stdout.strip())

# import subprocess
# def put_keyframes_at_new_length_of_streams(new_length_of_streams, video_name, output_file):
#     keyframe_frames = [0]  # Start at frame 0
#     cumulative_frames = 0
#     for frames in new_length_of_streams:
#         cumulative_frames += frames
#         keyframe_frames.append(cumulative_frames)
#     keyframe_frames.pop()
    
#     expressions = [f"eq(n,{frame})" for frame in keyframe_frames[1:]]  # Skip 0
#     keyframe_expr = "+".join(expressions) if expressions else "0"  # e.g., "eq(n,284)+eq(n,584)"
    
#     # ffmpeg_cmd = [
#     #     "ffmpeg",
#     #     "-i", video_name,
#     #     "-c:v", "libx264",
#     #     "-force_key_frames", f"expr:{keyframe_expr}",
#     #     "-sc_threshold", "0",
#     #     "-g", "1000",  # Large GOP to prevent extra keyframes
#     #     "-keyint_min", "1000",
#     #     "-vf", "setpts=PTS-STARTPTS",
#     #     "-c:a", "aac",
#     #     "-af", "asetpts=PTS-STARTPTS",
#     #     "-r", "30",
#     #     "-vsync", "1",
#     #     "-y",
#     #     output_file
#     # ]
#     # ffmpeg_cmd = [
#     #     "ffmpeg",
#     #     "-i", video_name,
#     #     "-c:v", "libx264",
#     #     "-crf", "18",  # High quality
#     #     "-maxrate", "12.9M",
#     #     "-bufsize", "25.8M",
#     #     "-force_key_frames", f"expr:{keyframe_expr}",
#     #     "-sc_threshold", "0",
#     #     "-g", "1000",
#     #     "-keyint_min", "1000",
#     #     "-vf", "setpts=PTS-STARTPTS",
#     #     "-c:a", "aac",
#     #     "-b:a", "192k",
#     #     "-af", "asetpts=PTS-STARTPTS",
#     #     "-r", "30",
#     #     "-vsync", "1",
#     #     "-map", "0",
#     #     "-y",
#     #     output_file
#     # ]
#     bitrate = get_video_bitrate(video_name)
#     ffmpeg_cmd = [
#         "ffmpeg",
#         "-i", video_name,
#         "-c:v", "libx264",
#         "-b:v", f"{bitrate}",
#         "-maxrate", f"{bitrate}",
#         "-bufsize", f"{bitrate * 2}",
#         "-force_key_frames", f"expr:{keyframe_expr}",
#         "-sc_threshold", "0",
#         "-g", "1000",
#         "-keyint_min", "1000",
#         "-c:a", "copy",
#         "-r", "30",
#         "-y", output_file
#     ]

    
#     try:
#         # Run FFmpeg command
#         subprocess.run(ffmpeg_cmd, check=True, capture_output=True, text=True)
#         print(f"Successfully created {output_file} with keyframes at frames: {keyframe_frames}")
#         return True
#     except subprocess.CalledProcessError as e:
#         print(f"Error running FFmpeg: {e.stderr}")
#         return False

# # ffprobe -loglevel error -select_streams v:0 -show_entries packet=pts_time,flags -of csv=print_section=0 input.mp4
# def get_keyframes(file_path):
#     cmd = [
#         "ffprobe",
#         "-loglevel", "error",
#         "-select_streams", "v:0",
#         "-show_entries", "packet=pts_time,flags",
#         "-of", "csv=print_section=0",
#         file_path
#     ]

#     try:
#         result = subprocess.run(cmd, check=True, capture_output=True, text=True)
#         keyframes = []
#         for line in result.stdout.splitlines():
#             pts_time, flags = line.split(",")
#             if flags.__contains__("K"):
#                 keyframes.append(float(pts_time))
#         return keyframes
#     except subprocess.CalledProcessError as e:
#         print(f"Error running ffprobe: {e.stderr}")
#         return []
    
# def create_combined_hls_stream(directory, subdirectory="hls"):
#     file_path = os.path.join(directory, "keyframes.mp4")
#     hls_dir = os.path.join(directory, subdirectory)
#     segment_path = os.path.join(hls_dir, "segment_%03d.ts").replace("\\", "/")
#     final_output_m3u8 = os.path.join(hls_dir, "playlist.m3u8").replace("\\", "/")
    
#     try:
#         os.makedirs(hls_dir, exist_ok=True)
#     except Exception as e:
#         print(f"Error creating hls folder {hls_dir}: {e}")
#         return False
    
#     # ffmpeg -i temp_new_video.mp4 -c:v copy -c:a copy -f hls -hls_time 1 -hls_list_size 0 -hls_segment_filename "segment_%03d.ts" playlist.m3u8
#     cmd = [
#         "ffmpeg",
#         "-i", file_path,
#         "-c:v", "copy",
#         "-c:a", "copy",
#         "-f", "hls",
#         "-hls_time", "1",
#         "-hls_list_size", "0",
#         "-hls_segment_filename", segment_path,
#         final_output_m3u8
#     ]
    
#     try:
#         # Run FFmpeg command
#         subprocess.run(cmd, check=True, capture_output=True, text=True)
#         print(f"Successfully created HLS stream at {final_output_m3u8}")
#     except subprocess.CalledProcessError as e:
#         print(f"Error running FFmpeg: {e.stderr}")
#         return False

# def is_significantly_different(hash1, hash2, threshold=5):
#     return hash1 - hash2 > threshold
# import os

# def get_previous_length_of_streams(video_id, frames1_length: int):
#     file_path = f"{video_id}/previousContext/previousLengthOfStreams.txt"
    
#     if os.path.exists(file_path):
#         # Read from file if it exists
#         with open(file_path, "r") as file:
#             previous_length_of_streams = [int(line.strip()) for line in file.readlines()]
#     else:
#         # Compute and store if file doesn't exist
#         previous_length_of_streams = []
#         i = frames1_length
#         while i >= 0 and i // 300 != 0:
#             previous_length_of_streams.append(300)
#             i -= 300

#         if i % 300 != 0:
#             previous_length_of_streams.append(i % 300)

#         os.makedirs(os.path.dirname(file_path), exist_ok=True)
#         with open(file_path, "w") as file:
#             for length in previous_length_of_streams:
#                 file.write(f"{length}\n")

#     return previous_length_of_streams

# import shutil
# import os
# import shutil

# def copy_changed_segments_and_playlist(directory, changed_segments, temp_hls_dir="temp_hls", primary_hls_dir="hls", temp_m3u8="playlist.m3u8", primary_m3u8="playlist.m3u8"):
#     temp_hls_path = os.path.join(directory, temp_hls_dir)
#     primary_hls_path = os.path.join(directory, primary_hls_dir)
#     temp_m3u8_path = os.path.join(directory, temp_hls_dir, temp_m3u8)
#     primary_m3u8_path = os.path.join(directory, primary_hls_dir, primary_m3u8)
    
#     try:
#         # Ensure temp folder exists
#         if not os.path.exists(temp_hls_path):
#             print(f"Temp HLS folder {temp_hls_path} does not exist")
#             return False
        
#         # Create primary hls folder if needed
#         os.makedirs(primary_hls_path, exist_ok=True)
        
#         # Copy changed segments
#         for idx in changed_segments:
#             segment_file = f"segment_{idx:03d}.ts"
#             src_path = os.path.join(temp_hls_path, segment_file)
#             dst_path = os.path.join(primary_hls_path, segment_file)
#             if os.path.exists(src_path):
#                 shutil.copy2(src_path, dst_path)
#                 print(f"Copied {segment_file} to {primary_hls_path}")
#             else:
#                 print(f"Segment {segment_file} not found in {temp_hls_path}")
#                 return False
        
#         # Copy temp_hls.m3u8 to primary playlist.m3u8
#         if os.path.exists(temp_m3u8_path):
#             shutil.copy2(temp_m3u8_path, primary_m3u8_path)
#             print(f"Copied {temp_m3u8_path} to {primary_m3u8_path}")
#         else:
#             print(f"Temp .m3u8 {temp_m3u8_path} not found")
#             return False
        
#         return True
    
#     except Exception as e:
#         print(f"Error copying segments or playlist: {e}")
#         return False

# # ffmpeg -allowed_extensions ALL -i playlist.m3u8 -r 30 -c:v copy -c:a copy merged.mp4
# def merge_hls_streams(directory):
#     hls_dir = os.path.join(directory, "hls")
#     merged_file = os.path.join(hls_dir, "merged_video.mp4")
    
#     cmd = [
#         "ffmpeg",
#         "-allowed_extensions", "ALL",
#         "-i", os.path.join(hls_dir, "playlist.m3u8"),
#         "-r", "30",
#         "-c:v", "copy",
#         "-c:a", "copy",
#         "-y",
#         merged_file
#     ]
#     try:
#         subprocess.run(cmd, check=True)
#         print(f"Merged video saved to {merged_file}")
#     except subprocess.CalledProcessError as e:
#         print(f"Error merging HLS streams: {e.stderr}")

# def update_hashes_file(directory, phash1):
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#         os.makedirs(os.path.join(directory, "previousContext"))
#     file_path = os.path.join(directory, "previousContext", "previous_hashes.txt")
    
#     with open(file_path, 'w') as file:
#         for item in phash1:
#             file.write(str(item) + "\n")
            
#     print(f"Updated hashes file at {file_path}")

# def update_length_of_streams_file(directory, previous_length_of_streams):
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#         os.makedirs(os.path.join(directory, "previousContext"))
#     file_path = os.path.join(directory, "previousContext", "previousLengthOfStreams.txt")
    
#     with open(file_path, 'w') as file:
#         for item in previous_length_of_streams:
#             file.write(str(item) + "\n")
            
#     print(f"Updated length of streams file at {file_path}")

# if '--init' in sys.argv:
#     videoName=sys.argv[2]
#     VIDEO_ID=sys.argv[3]
#     phash1= get_frame_hashes(videoName)
#     directory = f"{VIDEO_ID}"
#     file_path = os.path.join(directory, f'previousContext/previous_hashes.txt')
            
#     update_hashes_file(directory, phash1)
#     fps=30
#     previous_length_of_streams=[]
#     i=len(phash1)

#     while i>=0 and i//(fps*10)!=0:
#         previous_length_of_streams.append(fps*10)
#         i-=(fps*10)

#     if i%(fps*10)!=0:
#         previous_length_of_streams.append(i%(fps*10))
            
#     update_length_of_streams_file(directory, previous_length_of_streams)
#     put_keyframes_at_new_length_of_streams(previous_length_of_streams, videoName, os.path.join(directory, "keyframes.mp4"))
    
#     print(get_keyframes(os.path.join(directory, "keyframes.mp4")))
            
#     create_combined_hls_stream(directory)
    
# else:
#     EDITED_VIDEO_NAME=sys.argv[1]
#     VIDEO_ID=sys.argv[2]
#     directory = f"{VIDEO_ID}"
#     with open(f'{VIDEO_ID}/previousContext/previous_hashes.txt', 'r') as file:
#         phash1 = [imagehash.hex_to_hash(line.strip())  for line in file]
    
#     phash2=get_frame_hashes(EDITED_VIDEO_NAME)
    
#     i,j=0,0
#     deleted=[]
#     added=[]
#     changedFrames=[]
#     while i<len(phash1) and j<len(phash2):
#         currphash1=phash1[i]
#         currphash2=phash2[j]
#         if is_significantly_different(currphash1, currphash2):
#             flag=True
#             if (len(phash1)!=len(phash2)):
#                 for k in range(1,60): # check changes for 2 seconds as of now
#                     if i + k >= len(phash1): # out of bounds
#                         break
#                     newphash1=phash1[i+k]
#                     if newphash1==currphash2:
#                         # if k+1<15: # doubt-----------------------------------------------------------
#                         #     break
#                         print("-----------Deleted Frames-----------")
#                         print(i, i+k, i/30,"sec", "-", (i+k)/30,"sec")
#                         deleted.append((i,i+k-1))
#                         i=i+k
#                         # print(i/30)
#                         print("----------------------")
#                         flag=False
#                         break
                
#                 if flag:
#                     for k in range(1,60):
#                         if j + k >= len(phash2):
#                             break
#                         newphash2=phash2[j+k]
#                         if currphash1==newphash2:
#                             # if k+1<15: # doubt-----------------------------------------------------------
#                             #     break
#                             print("-----------Added Frames-----------")
#                             print(j, j+k, j/30,"sec", "-", (j+k)/30,"sec")
#                             added.append((j,j+k-1))
#                             j=j+k
#                             # print(j/30)
#                             print("----------------------")
#                             flag=False
#                             break
                    
#             if flag:
#                 changedFrames.append(j)
#                 # print("J=",j)
                
#         i+=1
#         j+=1
#     print("Deleted Frames",deleted)
#     print("Added Frames", added)
#     print("Changes Frames", changedFrames)
    
#     previous_length_of_streams= get_previous_length_of_streams(VIDEO_ID, len(phash1))
#     print("previous_length_of_streams", previous_length_of_streams)
    
#     new_length_of_streams=previous_length_of_streams[:] ## first copy it into new length and then calculated the revised length of streams
#     changedSegments=set()
    
#     # For deleted Frames
#     for deletedFrame in deleted:
#         start=deletedFrame[0]
#         end=deletedFrame[1]

#         index=start//300
#         changedSegments.add(index)
#         new_length_of_streams[index]-=end-start+1

#     # For added frames
#     for addedFrame in added:
#         start=addedFrame[0]
#         end=addedFrame[1]

#         index=start//300
#         changedSegments.add(index)
#         new_length_of_streams[index]+=end-start+1
    
#     for frame in changedFrames:
#         index=frame//300
#         changedSegments.add(index)
#         print(index, frame)

#     print("new_length_of_streams", new_length_of_streams)
#     print("changedSegments", changedSegments)
    
#     put_keyframes_at_new_length_of_streams(new_length_of_streams, EDITED_VIDEO_NAME, os.path.join(directory, "keyframes.mp4"))
    
#     create_combined_hls_stream(directory, "temp_hls")
    
#     copy_changed_segments_and_playlist(directory, changedSegments)
#     merge_hls_streams(directory)
    
#     update_hashes_file(directory, phash2)
#     update_length_of_streams_file(directory, new_length_of_streams)
    
    
from PIL import Image
import imagehash
import cv2
import sys
import os
import subprocess
import shutil
import argparse

# All your existing functions remain unchanged
def compute_frame_phash(gray_frame):
    pil_image = Image.fromarray(gray_frame)
    phash = imagehash.phash(pil_image, hash_size=16, highfreq_factor=16)
    return phash

def preprocess_frame(frame, blur_kernel_size=(5, 5)):
    try:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except cv2.error as e:
        print(f"Error converting frame to grayscale: {e}")
        print(f"Frame shape: {frame.shape}, Frame type: {type(frame)}")
        return None
    frame = cv2.GaussianBlur(frame, blur_kernel_size, 0)
    return frame

def get_frame_hashes(video_path):
    cap = cv2.VideoCapture(video_path)
    phash = []
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f'FPS : {fps:0.2f}')
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = preprocess_frame(frame)
        phash.append(compute_frame_phash(frame))
    cap.release()
    return phash

def get_video_bitrate(video_path):
    result = subprocess.run([
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=bit_rate",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ], capture_output=True, text=True)
    print("bitrate", int(result.stdout.strip()))
    return int(result.stdout.strip())

def put_keyframes_at_new_length_of_streams(new_length_of_streams, video_name, output_file):
    keyframe_frames = [0]
    cumulative_frames = 0
    for frames in new_length_of_streams:
        cumulative_frames += frames
        keyframe_frames.append(cumulative_frames)
    keyframe_frames.pop()
    expressions = [f"eq(n,{frame})" for frame in keyframe_frames[1:]]
    keyframe_expr = "+".join(expressions) if expressions else "0"
    bitrate = get_video_bitrate(video_name)
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", video_name,
        "-c:v", "libx264",
        "-b:v", f"{bitrate}",
        "-maxrate", f"{bitrate}",
        "-bufsize", f"{bitrate * 2}",
        "-force_key_frames", f"expr:{keyframe_expr}",
        "-sc_threshold", "0",
        "-g", "1000",
        "-keyint_min", "1000",
        "-c:a", "copy",
        "-r", "30",
        "-y", output_file
    ]
    try:
        subprocess.run(ffmpeg_cmd, check=True, capture_output=True, text=True)
        print(f"Successfully created {output_file} with keyframes at frames: {keyframe_frames}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running FFmpeg: {e.stderr}")
        return False

def get_keyframes(file_path):
    cmd = [
        "ffprobe",
        "-loglevel", "error",
        "-select_streams", "v:0",
        "-show_entries", "packet=pts_time,flags",
        "-of", "csv=print_section=0",
        file_path
    ]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        keyframes = []
        for line in result.stdout.splitlines():
            pts_time, flags = line.split(",")
            if flags.__contains__("K"):
                keyframes.append(float(pts_time))
        return keyframes
    except subprocess.CalledProcessError as e:
        print(f"Error running ffprobe: {e.stderr}")
        return []

def create_combined_hls_stream(directory, subdirectory="hls"):
    file_path = os.path.join(directory, "keyframes.mp4")
    hls_dir = os.path.join(directory, subdirectory)
    segment_path = os.path.join(hls_dir, "segment_%03d.ts").replace("\\", "/")
    final_output_m3u8 = os.path.join(hls_dir, "playlist.m3u8").replace("\\", "/")
    try:
        os.makedirs(hls_dir, exist_ok=True)
    except Exception as e:
        print(f"Error creating hls folder {hls_dir}: {e}")
        return False
    cmd = [
        "ffmpeg",
        "-i", file_path,
        "-c:v", "copy",
        "-c:a", "copy",
        "-f", "hls",
        "-hls_time", "1",
        "-hls_list_size", "0",
        "-hls_segment_filename", segment_path,
        final_output_m3u8
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Successfully created HLS stream at {final_output_m3u8}")
    except subprocess.CalledProcessError as e:
        print(f"Error running FFmpeg: {e.stderr}")
        return False

def is_significantly_different(hash1, hash2, threshold=5):
    return hash1 - hash2 > threshold

def get_previous_length_of_streams(video_id, frames1_length: int):
    file_path = f"{video_id}/previousContext/previousLengthOfStreams.txt"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            previous_length_of_streams = [int(line.strip()) for line in file.readlines()]
    else:
        previous_length_of_streams = []
        i = frames1_length
        while i >= 0 and i // 300 != 0:
            previous_length_of_streams.append(300)
            i -= 300
        if i % 300 != 0:
            previous_length_of_streams.append(i % 300)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            for length in previous_length_of_streams:
                file.write(f"{length}\n")
    return previous_length_of_streams

def copy_changed_segments_and_playlist(directory, changed_segments, temp_hls_dir="temp_hls", primary_hls_dir="hls", temp_m3u8="playlist.m3u8", primary_m3u8="playlist.m3u8"):
    temp_hls_path = os.path.join(directory, temp_hls_dir)
    primary_hls_path = os.path.join(directory, primary_hls_dir)
    temp_m3u8_path = os.path.join(directory, temp_hls_dir, temp_m3u8)
    primary_m3u8_path = os.path.join(directory, primary_hls_dir, primary_m3u8)
    try:
        if not os.path.exists(temp_hls_path):
            print(f"Temp HLS folder {temp_hls_path} does not exist")
            return False
        os.makedirs(primary_hls_path, exist_ok=True)
        for idx in changed_segments:
            segment_file = f"segment_{idx:03d}.ts"
            src_path = os.path.join(temp_hls_path, segment_file)
            dst_path = os.path.join(primary_hls_path, segment_file)
            if os.path.exists(src_path):
                shutil.copy2(src_path, dst_path)
                print(f"Copied {segment_file} to {primary_hls_path}")
            else:
                print(f"Segment {segment_file} not found in {temp_hls_path}")
                return False
        if os.path.exists(temp_m3u8_path):
            shutil.copy2(temp_m3u8_path, primary_m3u8_path)
            print(f"Copied {temp_m3u8_path} to {primary_m3u8_path}")
        else:
            print(f"Temp .m3u8 {temp_m3u8_path} not found")
            return False
        return True
    except Exception as e:
        print(f"Error copying segments or playlist: {e}")
        return False

def merge_hls_streams(directory):
    hls_dir = os.path.join(directory, "hls")
    merged_file = os.path.join(hls_dir, "merged_video.mp4")
    cmd = [
        "ffmpeg",
        "-allowed_extensions", "ALL",
        "-i", os.path.join(hls_dir, "playlist.m3u8"),
        "-r", "30",
        "-c:v", "copy",
        "-c:a", "copy",
        "-y",
        merged_file
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"Merged video saved to {merged_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error merging HLS streams: {e.stderr}")

def update_hashes_file(directory, phash1):
    if not os.path.exists(directory):
        os.makedirs(directory)
        os.makedirs(os.path.join(directory, "previousContext"))
    file_path = os.path.join(directory, "previousContext", "previous_hashes.txt")
    with open(file_path, 'w') as file:
        for item in phash1:
            file.write(str(item) + "\n")
    print(f"Updated hashes file at {file_path}")

def update_length_of_streams_file(directory, previous_length_of_streams):
    if not os.path.exists(directory):
        os.makedirs(directory)
        os.makedirs(os.path.join(directory, "previousContext"))
    file_path = os.path.join(directory, "previousContext", "previousLengthOfStreams.txt")
    with open(file_path, 'w') as file:
        for item in previous_length_of_streams:
            file.write(str(item) + "\n")
    print(f"Updated length of streams file at {file_path}")

def main():
    parser = argparse.ArgumentParser(
        description="CLI tool for video processing with keyframe and HLS stream management."
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="Initialize the video processing with a new video."
    )
    parser.add_argument(
        "video_path",
        help="Path to the input video file."
    )
    parser.add_argument(
        "video_id",
        help="Unique identifier for the video (used for directory structure)."
    )

    args = parser.parse_args()

    if args.init:
        # Initialization mode
        video_name = args.video_path
        video_id = args.video_id
        phash1 = get_frame_hashes(video_name)
        directory = f"{video_id}"
        update_hashes_file(directory, phash1)
        fps = 30
        previous_length_of_streams = []
        i = len(phash1)
        while i >= 0 and i // (fps * 10) != 0:
            previous_length_of_streams.append(fps * 10)
            i -= (fps * 10)
        if i % (fps * 10) != 0:
            previous_length_of_streams.append(i % (fps * 10))
        update_length_of_streams_file(directory, previous_length_of_streams)
        put_keyframes_at_new_length_of_streams(
            previous_length_of_streams,
            video_name,
            os.path.join(directory, "keyframes.mp4")
        )
        print(get_keyframes(os.path.join(directory, "keyframes.mp4")))
        create_combined_hls_stream(directory)
    else:
        # Update mode
        edited_video_name = args.video_path
        video_id = args.video_id
        directory = f"{video_id}"
        with open(f'{video_id}/previousContext/previous_hashes.txt', 'r') as file:
            phash1 = [imagehash.hex_to_hash(line.strip()) for line in file]
        phash2 = get_frame_hashes(edited_video_name)
        i, j = 0, 0
        deleted = []
        added = []
        changedFrames = []
        while i < len(phash1) and j < len(phash2):
            currphash1 = phash1[i]
            currphash2 = phash2[j]
            if is_significantly_different(currphash1, currphash2):
                flag = True
                if len(phash1) != len(phash2):
                    for k in range(1, 60):
                        if i + k >= len(phash1):
                            break
                        newphash1 = phash1[i + k]
                        if newphash1 == currphash2:
                            print("-----------Deleted Frames-----------")
                            print(i, i + k, i / 30, "sec", "-", (i + k) / 30, "sec")
                            deleted.append((i, i + k - 1))
                            i = i + k
                            print("----------------------")
                            flag = False
                            break
                    if flag:
                        for k in range(1, 60):
                            if j + k >= len(phash2):
                                break
                            newphash2 = phash2[j + k]
                            if currphash1 == newphash2:
                                print("-----------Added Frames-----------")
                                print(j, j + k, j / 30, "sec", "-", (j + k) / 30, "sec")
                                added.append((j, j + k - 1))
                                j = j + k
                                print("----------------------")
                                flag = False
                                break
                if flag:
                    changedFrames.append(j)
            i += 1
            j += 1
        print("Deleted Frames", deleted)
        print("Added Frames", added)
        print("Changes Frames", changedFrames)
        previous_length_of_streams = get_previous_length_of_streams(video_id, len(phash1))
        print("previous_length_of_streams", previous_length_of_streams)
        new_length_of_streams = previous_length_of_streams[:]
        changedSegments = set()
        for deletedFrame in deleted:
            start = deletedFrame[0]
            end = deletedFrame[1]
            index = start // 300
            changedSegments.add(index)
            new_length_of_streams[index] -= end - start + 1
        for addedFrame in added:
            start = addedFrame[0]
            end = addedFrame[1]
            index = start // 300
            changedSegments.add(index)
            new_length_of_streams[index] += end - start + 1
        for frame in changedFrames:
            index = frame // 300
            changedSegments.add(index)
            print(index, frame)
        print("new_length_of_streams", new_length_of_streams)
        print("changedSegments", changedSegments)
        put_keyframes_at_new_length_of_streams(
            new_length_of_streams,
            edited_video_name,
            os.path.join(directory, "keyframes.mp4")
        )
        create_combined_hls_stream(directory, "temp_hls")
        copy_changed_segments_and_playlist(directory, changedSegments)
        merge_hls_streams(directory)
        update_hashes_file(directory, phash2)
        update_length_of_streams_file(directory, new_length_of_streams)

if __name__ == "__main__":
    main()