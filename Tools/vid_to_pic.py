
from moviepy.editor import VideoFileClip
from moviepy.video.VideoClip import ImageClip
import os
import argparse
from PIL import Image
import random

def convert_video_to_images(input_source, output_folder, image_size):
    # Create the output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if os.path.isdir(input_source):
        # If the source is a directory, process all video files in the directory
        video_files = [f for f in os.listdir(input_source) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
        for video_file in video_files:
            video_path = os.path.join(input_source, video_file)
            process_single_video(video_path, output_folder, image_size)
    else:
        # If the source is a single video file, process it
        process_single_video(input_source, output_folder, image_size)

def process_single_video(input_video, output_folder, image_size):
    # load the video
    video_clip = VideoFileClip(input_video)

    # Iterate over every second of the video and save an image
    for i, frame in enumerate(video_clip.iter_frames(fps=1, dtype='uint8')):
        image_file = os.path.join(output_folder, f'{os.path.splitext(os.path.basename(input_video))[0]}_frame_{i + 1}.jpg')
        img_clip = ImageClip(frame)

        if image_size:
            img_clip = img_clip.resize((image_size[0], image_size[1]))

        img_clip.save_frame(image_file, withmask=False)
        create_random_cuts_and_scale(image_file, 5)

    # close the video
    video_clip.close()

def create_random_cuts_and_scale(image_path, cuts):
    with Image.open(image_path) as img:
        for _ in range(cuts):
            width, height = img.size
            x = random.randint(0, width - 900)
            y = random.randint(0, height - 900)

            cut = img.crop((x, y, x + 900, y + 900))
            cut = cut.resize((300, 300), Image.ANTIALIAS)
            cut_file_name = f'{os.path.splitext(image_path)[0]}_cut_scaled_{x}_{y}.jpg'
            cut.save(cut_file_name)

    os.remove(image_path)  # Delete the original image after creating cuts

def main():
    parser = argparse.ArgumentParser(description='Convert a video or videos in a folder to images.')
    parser.add_argument('--source', required=True, help='Path to the input video file or folder.')
    parser.add_argument('--output', required=True, help='Path to the output folder for images.')
    parser.add_argument('--size', default=None, type=str,
                        help='Size of the output images (widthxheight). Example: 640x480')

    args = parser.parse_args()

    image_size = None
    if args.size:
        image_size = tuple(map(int, args.size.split('x')))

    convert_video_to_images(args.source, args.output, image_size)

if __name__ == "__main__":
    main()
