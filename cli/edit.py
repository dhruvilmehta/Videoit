import cv2
import sys
import os
import subprocess

def preprocess_frame(frame, blur_kernel_size=(5, 5)):
    """Preprocess the frame by converting to grayscale and applying Gaussian blur."""
    try:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except cv2.error as e:
        print(f"Error converting frame to grayscale: {e}")
        print(f"Frame shape: {frame.shape}, Frame type: {type(frame)}")
        return None
    
    frame = cv2.GaussianBlur(frame, blur_kernel_size, 0)

    return frame


from PIL import Image
import imagehash

def compute_frame_phash(gray_frame):
    # Convert to PIL Image
    pil_image = Image.fromarray(gray_frame)
    
    # Compute perceptual hash
    phash = imagehash.phash(pil_image, hash_size=16, highfreq_factor=16)
    
    return phash

def get_frame_hashes(video_path):
    cap = cv2.VideoCapture(video_path)
    phash=[]

    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f'FPS : {fps:0.2f}')

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = preprocess_frame(frame)
        # frames.append(frame)

        phash.append(compute_frame_phash(frame))

    cap.release()
    return phash

def frames_to_time(frame_count, fps):
    return round(frame_count / fps, 3)  # Round to 3 decimal places for better precision

def generate_hls_segment(video_file, start_time, duration, output_dir, segment_num):
    segment_path = os.path.join(output_dir, f"segment_{segment_num}.ts").replace("\\", "/")
    
    cmd = [
        "ffmpeg",
        "-y",
        "-ss", str(start_time),  # Start time
        "-i", video_file,        # Input video file
        "-t", str(duration),     # Duration of the segment
        "-c:v", "libx264",      # Re-encode video with libx264
        "-c:a", "aac",          # Re-encode audio with AAC
        "-strict", "experimental",  # Allow experimental codecs
        "-force_key_frames", "expr:gte(t,n_forced*1)",  # Force keyframes every second
        "-f", "mpegts",         # Set output format to .ts
        segment_path             # Output .ts file
    ]
    
    try:
        subprocess.run(cmd, check=True)
        return segment_path
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return None

def generate_playlist(segment_durations, final_output_m3u8):
    with open(final_output_m3u8, 'w') as outfile:
        outfile.write('#EXTM3U\n')  # HLS playlist header
        
        for idx, duration in enumerate(segment_durations):
            # Add segment info to playlist
            outfile.write(f'#EXTINF:{duration},\n')
            outfile.write(f"segment_{idx}.ts\n")
            outfile.write('#EXT-X-TARGETDURATION:' + str(max(segment_durations)) + '\n')  

def create_combined_hls_stream(video_file, frame_ranges, fps, output_dir, final_output_m3u8):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    start_frame = 0
    segment_durations = []

    for idx, frame_count in enumerate(frame_ranges):
        start_time = frames_to_time(start_frame, fps)
        duration = frames_to_time(frame_count, fps)
        
        segment_path = generate_hls_segment(video_file, start_time, duration, output_dir, idx)
        
        if segment_path:
            segment_durations.append(duration)
        
        start_frame += frame_count

    # Generate a playlist with exact durations
    generate_playlist(segment_durations, final_output_m3u8)
    
import boto3
import os
from dotenv import load_dotenv
load_dotenv()

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_ACCESS_KEY_SECRET"),
    region_name="us-east-1"
)

def upload_segment(output_dir, segment_number):
    print("Upload file",segment_number)
    # S3 client setup with credentials
    
    # Construct the file name based on segment number
    file_name = f"segment_{segment_number}.ts"
    file_path = os.path.join(output_dir, file_name)
    print(file_path)
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"File {file_name} does not exist in {output_dir}")
        return
    
    try:
        # Upload to S3
        s3_client.upload_file(file_path, f"videohlsstreams", f"{VIDEO_ID}/{file_name}")
        print(f"Successfully uploaded {file_name} to S3")
    except Exception as e:
        print(f"Failed to upload {file_name}: {e}")
        
def upload_metadata(output_dir):
    fileNames=["previous_hashes.txt", "previous_length_of_streams.txt", "playlist.m3u8"]
    
    for upload in fileNames:
        file=os.path.join(output_dir, upload)
        
        if not os.path.isfile(file_path):
            print(f"File {file} does not exist in {output_dir}")
            return
        
        try:
        # Upload to S3
            s3_client.upload_file(file_path, f"videohlsstreams", file)
            print(f"Successfully uploaded {upload} to S3")
        except Exception as e:
            print(f"Failed to upload {upload}: {e}")
        
        
def create_video_list_file(videoId):
    # Create the file list
    directory = VIDEO_ID
    with open(f'{videoId}/segments.txt', 'w') as f:
        for filename in sorted(os.listdir(directory)):
            if filename.endswith('.ts') and not filename.__contains__("merged"):
                f.write(f"file '{os.path.join(directory, filename)}'\n")

def is_significantly_different(hash1, hash2, threshold=5):
    return hash1 - hash2 > threshold

print(sys.argv)
if '--init' in sys.argv:
    #  python3 edit.py --init main_edited_copy_2.mp4 version1
    videoName=sys.argv[2]
    VIDEO_ID=sys.argv[3]
    phash1= get_frame_hashes(videoName)
    # Will be done while initial uploading.

    directory = f"{VIDEO_ID}"
    file_path = os.path.join(directory, 'previous_hashes.txt')
    
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(f'{directory}/previous_hashes.txt', 'w') as file:
        for item in phash1:
            file.write(str(item) + "\n")
            
    fps=30
    previous_length_of_streams=[]
    i=len(phash1)

    while i>=0 and i//(fps*10)!=0:
        previous_length_of_streams.append(fps*10)
        i-=(fps*10)

    if i%(fps*10)!=0:
        previous_length_of_streams.append(i%(fps*10))

    with open(f'{directory}/previous_length_of_streams.txt', 'w') as file:
        for item in previous_length_of_streams:
            file.write(str(item) + "\n")

    final_output_m3u8 = os.path.join(directory, "playlist.m3u8").replace("\\", "/")
    create_combined_hls_stream(videoName, previous_length_of_streams, fps, directory, final_output_m3u8)
    
    for segment in range(len(previous_length_of_streams)):
        upload_segment(directory,segment)

    create_video_list_file(VIDEO_ID)
    upload_metadata(directory)

else:
    EDITED_VIDEO_NAME=sys.argv[1]
    VIDEO_ID=sys.argv[2]
    
    with open(f'{VIDEO_ID}/previous_hashes.txt', 'r') as file:
        # Read all lines and convert them to integers
        phash1 = [imagehash.hex_to_hash(line.strip())  for line in file]

    phash2=get_frame_hashes(EDITED_VIDEO_NAME)
    print("hash calculated")
    
    i,j=0,0
    deleted=[]
    added=[]
    changedFrames=[]
    while i<len(phash1) and j<len(phash2):
        currphash1=phash1[i]
        currphash2=phash2[j]
        if is_significantly_different(currphash1, currphash2):
            flag=True
            if (len(phash1)!=len(phash2)):
                for k in range(1,60):
                    if i + k >= len(phash1):
                        break
                    newphash1=phash1[i+k]
                    if newphash1==currphash2:
                        if k+1<15: # doubt-----------------------------------------------------------
                            break
                        print(i, i+k, i/30, "-", (i+k)/30)
                        deleted.append((i,i+k-1))
                        i=i+k
                        print(i/30)
                        flag=False
                        break
                
                if flag:
                    for k in range(1,60):
                        if j + k >= len(phash2):
                            break
                        newphash2=phash2[j+k]
                        if currphash1==newphash2:
                            if k+1<15: # doubt-----------------------------------------------------------
                                break
                            print(j, j+k, j/30, "-", (j+k)/30)
                            added.append((j,j+k-1))
                            j=j+k
                            print(j/30)
                            flag=False
                            break
                    
            if flag:
                changedFrames.append(j)
                
        i+=1
        j+=1

    print("Deleted",deleted)
    print("Added", added)
    print("Changed Frames",changedFrames)