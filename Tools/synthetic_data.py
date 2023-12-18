from PIL import Image
import pyvista as pv
import numpy as np
import os
import shutil
import argparse


def generate_random_rotation_matrix():
    # Generiere zufällige Winkel in Radiant für die Rotation um jede Achse
    i = np.pi / 4
    #angle_x = np.random.uniform(0, 2 * np.pi)
    #angle_y = np.random.uniform(0, 2 * np.pi)
    #angle_z = np.random.uniform(0, 2 * np.pi)

    angle_x = np.random.uniform(-i, i)
    angle_y = np.random.uniform(-i, i)
    angle_z = np.random.uniform(0, 2 * np.pi)

    # Erstelle Rotationsmatrizen für jede Achse
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

    # Multipliziere die Rotationsmatrizen, um die endgültige Rotationsmatrix zu erhalten
    final_rotation_matrix = np.dot(rotation_matrix_z, np.dot(rotation_matrix_y, rotation_matrix_x))

    return final_rotation_matrix

def create_label_file(label_path, class_id, x_center, y_center, width, height, bg_width, bg_height):
    # Skaliere die Koordinaten auf den Bereich [0, 1]
    x_min_normalized = x_center / bg_width
    y_min_normalized = y_center / bg_height
    width_normalized = width / bg_width
    height_normalized = height / bg_height

    with open(label_path, 'a') as f:
        f.write(f"{class_id} {x_min_normalized} {y_min_normalized} {width_normalized} {height_normalized}\n")

def main(args):
    # STL-Datei laden
    stl_files = args.stl_files
    images_folder = args.images_folder
    temp_folder = args.temp_folder
    final_image_path = args.output
    final_label_path = args.label

    for i, image_file in enumerate(os.listdir(images_folder)):
        try:
            if image_file.endswith(".png") or image_file.endswith(".jpg"):
                image_path = os.path.join(images_folder, image_file)

                for j, your_stl_file in enumerate(stl_files):
                    try:
                        # Lade STL-Datei und erstelle Mesh
                        mesh = pv.read(your_stl_file)

                        # Generiere zufällige Rotation
                        rotation_matrix = generate_random_rotation_matrix()

                        # Anwenden von Rotation auf das 3D-Objekt
                        mesh.transform(rotation_matrix)

                        if j == 2:
                            # Visualisiere das 3D-Objekt
                            plotter = pv.Plotter(off_screen=True)
                            plotter.add_mesh(mesh, color='black', show_edges=False)
                        else:
                            # Visualisiere das 3D-Objekt
                            plotter = pv.Plotter(off_screen=True)
                            plotter.add_mesh(mesh, color='white', show_edges=False)

                        # Setzen Sie die Kameraposition und -orientierung für eine Draufsicht
                        plotter.camera_position = [(0, 0, -2 * mesh.length), (0, 0, 0), (0, 1, 0)]

                        # Screenshot speichern
                        screenshot_path = f'{temp_folder}/{i}_{j}.png'
                        plotter.screenshot(screenshot_path, transparent_background=True)
                        plotter.close()
                    except Exception as e:
                        print(f"Fehler beim Verarbeiten der STL-Datei {your_stl_file}: {e}")
                        continue

                # Laden Sie das Hintergrundbild
                background_image = Image.open(image_path)

                # Zielgröße setzen
                target_size = (1920, 1080)

                # Verhältnis von Zielgröße zu Originalgröße berechnen
                # ratio = min(target_size[0] / background_image.width, target_size[1] / background_image.height)

                # Neue Größe berechnen
                # new_size_background = (int(background_image.width * ratio), int(background_image.height * ratio))

                # Hintergrundbild auf die neue Größe skalieren, ohne zu verzerrren
                background_image = background_image.resize(target_size)

                for x, screenshot_path in enumerate(os.listdir(temp_folder)):
                    print("- - - - -")
                    try:
                        # Laden Sie das gespeicherte Bild, das eingefügt werden soll
                        rotated_image_path = screenshot_path
                        rotated_image = Image.open(f'{temp_folder}/{rotated_image_path}')
                        file_name = os.path.basename(rotated_image_path)  # Get the file name from the path

                        if file_name[-5] == "3":
                            scaling_factor = np.random.uniform(0.5, 0.6)
                        else:
                            scaling_factor = np.random.uniform(0.1, 0.2)

                        # Größe des Screenshots ändern (verkleinern oder vergrößern)
                        new_size = (int((rotated_image.width * scaling_factor)),
                                    int((rotated_image.height * scaling_factor)))

                        # Für die Bounding Boxen
                        test_new_size = (int(((rotated_image.width - 520) * scaling_factor)),
                                         int(((rotated_image.height - 240) * scaling_factor)))

                        rotated_image = rotated_image.resize(new_size)

                        # Einfügen des veränderten Bildes in das Hintergrundbild in der Mitte
                        bg_width, bg_height = background_image.size
                        rotated_width, rotated_height = rotated_image.size
                        paste_position = (np.random.randint(0, bg_width - rotated_width),
                                          np.random.randint(0, bg_height - rotated_height))


                        background_image.paste(rotated_image, paste_position, rotated_image)

                        # Speichern Sie das endgültige Bild
                        # final_image_path = f'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/TestDir/images/{i}.png'
                        #final_image_path = f'{final_image_path}/{i}.jpg'
                        background_image.save(f'{final_image_path}/{i}.jpg')

                        # Kopiere die PNG-Datei als JPG-Datei
                        #shutil.copy(final_image_path,
                           #         f'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/TestDir/images/{i}.jpg')
                        #os.remove(final_image_path)

                        output_dir = final_label_path
                        label_path = os.path.join(output_dir, f"{i}.txt")
                        # print(f"File Name: {file_name}, Type: {type(file_name)}")  # Add this line
                        if file_name[-5] == "0":
                            class_id = 0
                        elif file_name[-5] == "1":
                            class_id = 1
                        elif file_name[-5] == "2":
                            class_id = 2
                        elif file_name[-5] == "3":
                            class_id = 3
                        x_center, y_center = paste_position[0] + new_size[0] / 2, paste_position[1] + new_size[1] / 2
                        # print(paste_position[0])
                        width, height = test_new_size

                        create_label_file(label_path, class_id, x_center, y_center, width, height, bg_width, bg_height)

                        # shutil.copy(f'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/TestDir/temp/{rotated_image_path}',
                        #             '/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/TestDir/temp_2')

                        # Löschen des Screenshots des 3D-Modells
                        os.remove(
                            f'{temp_folder}/{rotated_image_path}')
                    except Exception as e:
                        os.remove(
                            f'{temp_folder}/{rotated_image_path}')
                        print(f"Fehler beim Verarbeiten des Bildes {image_file}: {e}")
                        continue

                print(f"Verarbeite Bild {i + 1}: {image_path}")

        except Exception as e:
            print(f"Fehler beim Verarbeiten des Bildes {image_file}: {e}")
            continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description of your program")
    parser.add_argument("--stl_files", nargs="+", help="List of STL files")
    parser.add_argument("--images_folder", help="Path to the folder containing images")
    parser.add_argument("--output", help="Path to output folder")
    parser.add_argument("--label", help="Path to label folder")
    parser.add_argument("--temp_folder", help="Path to the temporary folder")

    args = parser.parse_args()
    main(args)
