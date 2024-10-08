import cv2
import os

def split_video(input_video, output_prefix, segment_duration):
    cap = cv2.VideoCapture(input_video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    segment_frames = int(segment_duration * fps)
    
    i = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if i % segment_frames == 0:
            output_file = f"{output_prefix}_{i // segment_frames}.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_file, fourcc, fps, (frame.shape[1], frame.shape[0]))
        out.write(frame)
        
        if i % segment_frames == segment_frames - 1:
            out.release()
        
        i += 1

    cap.release()
    cv2.destroyAllWindows()

# Example usage:
input_video = 'main_edit.mp4'
output_prefix = 'main_edit'
segment_duration = 5  # Segment duration in seconds
split_video(input_video, output_prefix, segment_duration)




def merge_videos(input_prefix, output_video):
    video_files = [file for file in os.listdir() if file.startswith(input_prefix) and file.endswith('.mp4')]
    video_files.sort()  # Sort the files in alphanumeric order
    
    if not video_files:
        print("No segmented videos found.")
        return
    
    # Get the properties of the first video
    first_video = cv2.VideoCapture(video_files[0])
    fps = first_video.get(cv2.CAP_PROP_FPS)
    width = int(first_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(first_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    # Create video writer object
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
    
    # Iterate through each segmented video and append it to the output video
    for video_file in video_files:
        video = cv2.VideoCapture(video_file)
        while True:
            ret, frame = video.read()
            if not ret:
                break
            out.write(frame)
        video.release()
    
    out.release()

# Example usage:
input_prefix = 'split_main'
output_video = 'merged_main.mp4'
# merge_videos(input_prefix, output_video)