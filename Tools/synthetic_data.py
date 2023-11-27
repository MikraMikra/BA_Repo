from PIL import Image
import pyvista as pv
import numpy as np
import os
import shutil


def generate_random_rotation_matrix():
    # Generiere zufällige Winkel in Radiant für die Rotation um jede Achse
    angle_x = np.random.uniform(0, 2 * np.pi)
    angle_y = np.random.uniform(0, 2 * np.pi)
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
    # Konvertiere die x- und y-Koordinaten in Bezug auf das Koordinatensystem mit Ursprung in der oberen linken Ecke
    x_min = x_center - width / 2
    y_min = y_center - height / 2

    # Skaliere die Koordinaten auf den Bereich [0, 1]
    x_min_normalized = x_center / bg_width
    y_min_normalized = y_center / bg_height
    width_normalized = width / bg_width
    height_normalized = height / bg_height

    with open(label_path, 'a') as f:
        f.write(f"{class_id} {x_min_normalized} {y_min_normalized} {width_normalized} {height_normalized}\n")


# STL-Datei laden
your_stl_file = r'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/Planetengetriebe_meshes/sun_c.stl'
stl_files = [
    r'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/Planetengetriebe_meshes/sun_c.stl',
    r'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/Planetengetriebe_meshes/planet_c.stl',
    r'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/Planetengetriebe_meshes/planet_c.stl'
]

images_folder = r'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/Office_building'
temp_folder = r'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/TestDir/temp'

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

                    # Screenshot speichern
                    screenshot_path = f'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/TestDir/temp/{i}_{j}.png'
                    plotter.screenshot(screenshot_path, transparent_background=True)
                    plotter.close()
                except Exception as e:
                    print(f"Fehler beim Verarbeiten der STL-Datei {your_stl_file}: {e}")
                    continue

            # Laden Sie das Hintergrundbild
            background_image = Image.open(image_path)

            for x, screenshot_path in enumerate(os.listdir(temp_folder)):
                try:
                    # Laden Sie das gespeicherte Bild, das eingefügt werden soll
                    rotated_image_path = screenshot_path
                    rotated_image = Image.open(
                        f'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/TestDir/temp/{rotated_image_path}')

                    scaling_factor = np.random.uniform(0.1, 0.5)

                    # Größe des Screenshots ändern (verkleinern oder vergrößern)
                    new_size = (int((rotated_image.width * scaling_factor)),
                                int((rotated_image.height * scaling_factor)))

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
                    final_image_path = f'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/TestDir/images/{i}.png'
                    background_image.save(final_image_path)

                    # Kopiere die PNG-Datei als JPG-Datei
                    shutil.copy(final_image_path,
                                f'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/TestDir/images/{i}.jpg')
                    os.remove(final_image_path)

                    output_dir = "/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/TestDir/labels"
                    label_path = os.path.join(output_dir, f"{i}.txt")
                    file_name = os.path.basename(rotated_image_path)  # Get the file name from the path
                    # print(f"File Name: {file_name}, Type: {type(file_name)}")  # Add this line
                    if file_name[-5] == "0":
                        class_id = 0
                    elif file_name[-5] == "1":
                        class_id = 1
                    elif file_name[-5] == "2":
                        class_id = 2
                    x_center, y_center = paste_position[0] + new_size[0] / 2, paste_position[1] + new_size[1] / 2
                    # print(paste_position[0])
                    width, height = test_new_size

                    create_label_file(label_path, class_id, x_center, y_center, width, height, bg_width, bg_height)

                    # shutil.copy(f'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/TestDir/temp/{rotated_image_path}',
                    #             '/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/TestDir/temp_2')

                    # Löschen des Screenshots des 3D-Modells
                    os.remove(
                        f'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/TestDir/temp/{rotated_image_path}')
                except Exception as e:
                    print(f"Fehler beim Verarbeiten des Bildes {image_file}: {e}")
                    continue

            print(f"Verarbeite Bild {i + 1}: {image_path}")

    except Exception as e:
        print(f"Fehler beim Verarbeiten des Bildes {image_file}: {e}")
        continue
