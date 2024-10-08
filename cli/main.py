import hashlib
# import time

def generate_md5_checksum(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

# # Example usage:
file_path1 = 'main_edit.mp4'
file_path2 = 'main.mp4'
# file_path3 = 'hello3.mp4'
# file_path4 = 'hello4.mp4'
# file_path5 = 'hello5.mp4'
# file_path1copy = 'hello1copy.mp4'
# canvacopy = 'canvacopy.mp4'
# start_time = time.time()
checksum1 = generate_md5_checksum(file_path1)
print(checksum1)
checksum1 = generate_md5_checksum(file_path2)
print(checksum1)
# training_time = time.time() - start_time
# print(training_time)
# start_time = time.time()
# checksum2 = generate_md5_checksum(file_path2)
# training_time = time.time() - start_time
# print(training_time)
# start_time = time.time()
# checksum3 = generate_md5_checksum(file_path3)
# training_time = time.time() - start_time
# print(training_time)
# start_time = time.time()
# checksum4 = generate_md5_checksum(file_path4)
# training_time = time.time() - start_time
# print(training_time)
# start_time = time.time()
# checksum5 = generate_md5_checksum(file_path5)
# training_time = time.time() - start_time
# print(training_time)
# checksum1copy = generate_md5_checksum(file_path1copy)
# checksumcanva1copy = generate_md5_checksum(canvacopy)

# print("MD5 Checksum:", checksum1)
# print("MD5 Checksum:", checksum2)
# print("MD5 Checksum:", checksum3)
# print("MD5 Checksum:", checksum4)
# print("MD5 Checksum:", checksum1copy)
# print("MD5 Checksum:", checksumcanva1copy)


# file_path1 = '3_edit_3.mp4'
# checksum1copy = generate_md5_checksum(file_path1)
# print(checksum1copy)
# file_path1 = 'edit_3_3.mp4'
# checksum1copy = generate_md5_checksum(file_path1)
# print(checksum1copy)



# import cv2
# import hashlib

# def generate_segment_hashes(video_path, segment_duration=5):
#     cap = cv2.VideoCapture(video_path)
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     frame_hashes = []

#     segment_frames = int(segment_duration * fps)
#     while cap.isOpened():
#         segment_data = b''
#         for _ in range(segment_frames):
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             frame_data = cv2.imencode('.png', frame)[1].tostring()
#             segment_data += frame_data
        
#         if segment_data:
#             segment_hash = hashlib.md5(segment_data).hexdigest()
#             frame_hashes.append(segment_hash)

#     cap.release()
#     return frame_hashes

# # Example usage:
# video_path = '3_edit.mp4'
# segment_hashes = generate_segment_hashes(video_path)
# print("MD5 Hashes for 5-second Segments:", segment_hashes)


# import hashlib
# import cv2

# def generate_segment_hashes(video_path, num_segments):
#     cap = cv2.VideoCapture(video_path)
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     segment_hashes = []

#     frames_per_segment = total_frames // num_segments

#     for i in range(num_segments):
#         segment_data = b''
#         for _ in range(frames_per_segment):
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             frame_data = cv2.imencode('.png', frame)[1].tostring()
#             segment_data += frame_data
        
#         if segment_data:
#             segment_hash = hashlib.md5(segment_data).hexdigest()
#             segment_hashes.append(segment_hash)

#     cap.release()
#     return segment_hashes

# def detect_segment_changes(video_path, num_segments):
#     segment_hashes = generate_segment_hashes(video_path, num_segments)

#     # Compare the hashes with the original video
#     for i, hash_value in enumerate(segment_hashes):
#         print(f"Segment {i+1} hash:", hash_value)

# # Example usage:
# video_path = 'canvacopy.mp4'
# num_segments = 5
# detect_segment_changes(video_path, num_segments)
