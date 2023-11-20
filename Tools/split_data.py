import os
import random
import shutil
import argparse

def split_data(root_folder, train_ratio, val_ratio):
    # Paths to folders
    images_folder = os.path.join(root_folder, "images")
    labels_folder = os.path.join(root_folder, "labels")

    # Create new folders
    train_folder = os.path.join(root_folder, "train")
    val_folder = os.path.join(root_folder, "valid")
    test_folder = os.path.join(root_folder, "test")

    for folder in [train_folder, val_folder, test_folder]:
        os.makedirs(os.path.join(folder, "images"), exist_ok=True)
        os.makedirs(os.path.join(folder, "labels"), exist_ok=True)

    # Get filenames from "images" and "labels" folders
    image_files = os.listdir(images_folder)
    label_files = os.listdir(labels_folder)

    # Ensure there is a corresponding text file for each image file
    image_files = [file for file in image_files if file.replace(".jpg", ".txt") in label_files]

    # Random order of files
    random.shuffle(image_files)

    # Data split
    total_files = len(image_files)
    train_split = int(train_ratio * total_files)
    val_split = int(val_ratio * total_files)

    # Distribute files into corresponding folders
    for i, file in enumerate(image_files):
        source_img = os.path.join(images_folder, file)
        source_txt = os.path.join(labels_folder, file.replace(".jpg", ".txt"))

        if i < train_split:
            destination_folder = train_folder
        elif i < train_split + val_split:
            destination_folder = val_folder
        else:
            destination_folder = test_folder

        dest_img = os.path.join(destination_folder, "images", file)
        dest_txt = os.path.join(destination_folder, "labels", file.replace(".jpg", ".txt"))

        shutil.copyfile(source_img, dest_img)
        shutil.copyfile(source_txt, dest_txt)

def main():
    parser = argparse.ArgumentParser(description='Split image and label files into training, validation, and test sets.')
    parser.add_argument('--source', required=True, help='Path to the root folder containing "images" and "labels" folders.')
    parser.add_argument('--train_ratio', type=float, default=0.7, help='Percentage of data for the training set.')
    parser.add_argument('--val_ratio', type=float, default=0.15, help='Percentage of data for the validation set.')

    args = parser.parse_args()

    split_data(args.source, args.train_ratio, args.val_ratio)

main()
