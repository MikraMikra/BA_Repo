from moviepy.editor import VideoFileClip
from moviepy.video.VideoClip import ImageClip
import os
import argparse
from PIL import Image
import random
import time
import psutil
import csv

def monitor_memory(process, memory_usage):
    memory_usage.append(process.memory_info().rss / 1024 ** 2)  # Speichernutzung in MB

def convert_video_to_images(input_source, output_folder, image_size):
    start_time = time.time()
    process = psutil.Process()
    memory_usage = []
    video_processing_stats = []

    # Create the output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if os.path.isdir(input_source):
        video_files = [f for f in os.listdir(input_source) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
        for video_file in video_files:
            video_path = os.path.join(input_source, video_file)
            video_duration, processing_time = process_single_video(video_path, output_folder, image_size, process, memory_usage)
            video_processing_stats.append([video_file, video_duration, processing_time])
    else:
        video_duration, processing_time = process_single_video(input_source, output_folder, image_size, process, memory_usage)
        video_processing_stats.append(['Single Video', video_duration, processing_time])

    with open(os.path.join(output_folder, 'memory_usage.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time (s)', 'Memory Usage (MB)'])
        for i, usage in enumerate(memory_usage):
            writer.writerow([i, usage])

    with open(os.path.join(output_folder, 'video_processing_stats.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Video Name', 'Video Duration (s)', 'Processing Time (s)'])
        writer.writerows(video_processing_stats)

    end_time = time.time()
    print(f"Total processing completed in: {end_time - start_time} seconds.")

def process_single_video(input_video, output_folder, image_size, process, memory_usage):
    video_clip = VideoFileClip(input_video)
    video_start_time = time.time()
    video_duration = video_clip.duration

    for i, frame in enumerate(video_clip.iter_frames(fps=1, dtype='uint8')):
        monitor_memory(process, memory_usage)
        image_file = os.path.join(output_folder, f'{os.path.splitext(os.path.basename(input_video))[0]}_frame_{i + 1}.jpg')
        img_clip = ImageClip(frame)
        if image_size:
            img_clip = img_clip.resize(image_size)
        img_clip.save_frame(image_file, withmask=False)
        create_random_cuts_and_scale(image_file, 5)

    video_clip.close()
    processing_time = time.time() - video_start_time
    return video_duration, processing_time

def create_random_cuts_and_scale(image_path, cuts):
    with Image.open(image_path) as img:
        for _ in range(cuts):
            width, height = img.size
            x = random.randint(0, width - 900)
            y = random.randint(0, height - 900)
            cut = img.crop((x, y, x + 900, y + 900))
            cut = cut.resize((300, 300))
            cut_file_name = f'{os.path.splitext(image_path)[0]}_cut_scaled_{x}_{y}.jpg'
            cut.save(cut_file_name)
    os.remove(image_path)
