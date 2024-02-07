# Import necessary libraries
from PIL import Image
import pyvista as pv
import numpy as np
import os
import argparse


# Function to generate a random 3D rotation matrix
def generate_random_rotation_matrix():
    """
    Generate a random 3D rotation matrix.

    Returns:
        np.ndarray: The random rotation matrix.
    """
    # Generate random rotation angles for each axis
    i = np.pi / 4
    angle_x = np.random.uniform(-i, i)
    angle_y = np.random.uniform(-i, i)
    angle_z = np.random.uniform(0, 2 * np.pi)

    # Create rotation matrices for each axis
    rotation_matrix_x = np.array([
        [1, 0, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x), 0],
        [0, np.sin(angle_x), np.cos(angle_x), 0],
        [0, 0, 0, 1]
    ])

    rotation_matrix_y = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y), 0],
        [0, 1, 0, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y), 0],
        [0, 0, 0, 1]
    ])

    rotation_matrix_z = np.array([
        [np.cos(angle_z), -np.sin(angle_z), 0, 0],
        [np.sin(angle_z), np.cos(angle_z), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    # Combine rotation matrices to get the final rotation matrix
    final_rotation_matrix = np.dot(rotation_matrix_z, np.dot(rotation_matrix_y, rotation_matrix_x))

    return final_rotation_matrix


# Function to create a label file with bounding box information
def create_label_file(label_path, class_id, x_center, y_center, width, height, bg_width, bg_height):
    """
    Create a label file with bounding box information.

    Args:
        label_path (str): Path to the label file.
        class_id (int): Class ID.
        x_center (float): X-coordinate of the bounding box center.
        y_center (float): Y-coordinate of the bounding box center.
        width (float): Width of the bounding box.
        height (float): Height of the bounding box.
        bg_width (int): Width of the background image.
        bg_height (int): Height of the background image.
    """
    # Normalize coordinates and dimensions
    x_min_normalized = x_center / bg_width
    y_min_normalized = y_center / bg_height
    width_normalized = width / bg_width
    height_normalized = height / bg_height

    # Write the normalized bounding box information to the label file
    with open(label_path, 'a') as f:
        f.write(f"{class_id} {x_min_normalized} {y_min_normalized} {width_normalized} {height_normalized}\n")


# Main function to generate synthetic images with labeled bounding boxes
def main(args):
    """
    Main function to generate synthetic images with labeled bounding boxes.

    Args:
        args (argparse.Namespace): Command-line arguments.
    """
    # Extract command-line arguments
    stl_files = args.stl_files
    images_folder = args.images_folder
    temp_folder = args.temp_folder
    final_image_path = args.output
    final_label_path = args.label

    # Iterate over images in the specified folder
    for i, image_file in enumerate(os.listdir(images_folder)): # Hintergrundbilder
        try:
            # Check if the file is an image (PNG or JPG)
            if image_file.endswith(".png") or image_file.endswith(".jpg"):
                image_path = os.path.join(images_folder, image_file)

                # Iterate over STL files
                for j, your_stl_file in enumerate(stl_files):
                    try:
                        # Read STL file and apply a random rotation
                        mesh = pv.read(your_stl_file)
                        rotation_matrix = generate_random_rotation_matrix()
                        mesh.transform(rotation_matrix)

                        # Create a PyVista plotter for visualization
                        if j == 2:
                            plotter = pv.Plotter(off_screen=True)
                            plotter.add_mesh(mesh, color='black', show_edges=False)
                        else:
                            plotter = pv.Plotter(off_screen=True)
                            plotter.add_mesh(mesh, color='white', show_edges=False)

                        # Set the camera position for the plotter
                        plotter.camera_position = [(0, 0, -2 * mesh.length), (0, 0, 0), (0, 1, 0)]

                        # Save a screenshot of the scene
                        screenshot_path = f'{temp_folder}/{i}_{j}.png'
                        plotter.screenshot(screenshot_path, transparent_background=True)
                        plotter.close()
                    except Exception as e:
                        print(f"Fehler beim Verarbeiten der STL-Datei {your_stl_file}: {e}")
                        continue

                # Open the background image and resize it
                background_image = Image.open(image_path)
                target_size = (1920, 1080)
                background_image = background_image.resize(target_size)

                # Iterate over generated screenshots
                for x, screenshot_path in enumerate(os.listdir(temp_folder)):
                    print("- - - - -")
                    try:
                        rotated_image_path = screenshot_path
                        rotated_image = Image.open(f'{temp_folder}/{rotated_image_path}')
                        file_name = os.path.basename(rotated_image_path)

                        # Randomly scale the rotated image
                        if file_name[-5] == "3":
                            scaling_factor = np.random.uniform(0.5, 0.6)
                        else:
                            scaling_factor = np.random.uniform(0.1, 0.2)

                        # Resize the rotated image
                        new_size = (int((rotated_image.width * scaling_factor)),
                                    int((rotated_image.height * scaling_factor)))

                        test_new_size = (int(((rotated_image.width - 520) * scaling_factor)),
                                         int(((rotated_image.height - 240) * scaling_factor)))

                        rotated_image = rotated_image.resize(new_size)

                        # Get dimensions of images
                        bg_width, bg_height = background_image.size
                        rotated_width, rotated_height = rotated_image.size

                        # Randomly choose a position to paste the rotated image on the background
                        paste_position = (np.random.randint(0, bg_width - rotated_width),
                                          np.random.randint(0, bg_height - rotated_height))

                        # Paste the rotated image onto the background
                        background_image.paste(rotated_image, paste_position, rotated_image)

                        # Save the final image
                        background_image.save(f'{final_image_path}/{i}.jpg')

                        # Create label file path and determine class ID based on the filename
                        output_dir = final_label_path
                        label_path = os.path.join(output_dir, f"{i}.txt")
                        if file_name[-5] == "0":
                            class_id = 0
                        elif file_name[-5] == "1":
                            class_id = 1
                        elif file_name[-5] == "2":
                            class_id = 2
                        elif file_name[-5] == "3":
                            class_id = 3

                        # Calculate the center coordinates and dimensions of the bounding box
                        x_center, y_center = paste_position[0] + new_size[0] / 2, paste_position[1] + new_size[1] / 2
                        width, height = test_new_size

                        # Create the label file with bounding box information
                        create_label_file(label_path, class_id, x_center, y_center, width, height, bg_width, bg_height)

                        # Remove the temporary rotated image file
                        os.remove(f'{temp_folder}/{rotated_image_path}')
                    except Exception as e:
                        # Remove the temporary rotated image file in case of an error
                        os.remove(f'{temp_folder}/{rotated_image_path}')
                        print(f"Fehler beim Verarbeiten des Bildes {image_file}: {e}")
                        continue

                print(f"Verarbeite Bild {i + 1}: {image_path}")

        except Exception as e:
            print(f"Fehler beim Verarbeiten des Bildes {image_file}: {e}")
            continue


# Check if the script is being run as the main program
if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Description of your program")
    parser.add_argument("--stl_files", nargs="+", help="List of STL files")
    parser.add_argument("--images_folder", help="Path to the folder containing images")
    parser.add_argument("--output", help="Path to output folder")
    parser.add_argument("--label", help="Path to label folder")
    parser.add_argument("--temp_folder", help="Path to the temporary folder")

    args = parser.parse_args()

    # Call the main function with the parsed arguments
    main(args)
