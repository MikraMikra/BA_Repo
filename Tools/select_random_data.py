import os
import random
import shutil
import argparse

def select_random_files(source_folder, destination_folder, num_files):
    # List all JPG files in the source folder
    all_files = [f for f in os.listdir(source_folder) if f.endswith('.jpg')]

    # Check if there are enough JPG files in the folder
    if len(all_files) < num_files:
        print("There are fewer than", num_files, "JPG files in the folder.")
    else:
        # Create the destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Randomly select the specified number of files
        random_files = random.sample(all_files, num_files)

        # Copy the selected files to the destination folder
        for file in random_files:
            source_path = os.path.join(source_folder, file)
            destination_path = os.path.join(destination_folder, file)
            shutil.copy(source_path, destination_path)
            print(f"{file} has been copied to {destination_folder}")

def main():
    parser = argparse.ArgumentParser(description='Randomly select and copy JPG files from a source folder to a output folder.')
    parser.add_argument('--source', required=True, help='Path to the source folder containing JPG files.')
    parser.add_argument('--output', required=True, help='Path to the output folder where files will be copied.')
    parser.add_argument('--num_files', type=int, required=True, help='Number of files to randomly select and copy.')

    args = parser.parse_args()

    select_random_files(args.source, args.output, args.num_files)

main()
