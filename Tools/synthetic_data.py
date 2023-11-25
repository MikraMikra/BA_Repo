from PIL import Image
import pyvista as pv
import numpy as np
import os


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


# STL-Datei laden
your_stl_file = r'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/TestDir/Planetengetriebe_meshes/sun_c.stl'
background_image_path = r'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/TestDir/a-room-at-the-beach.jpg'

for i in range(10):
    # Lade STL-Datei und erstelle Mesh
    mesh = pv.read(your_stl_file)

    # Generiere zufällige Rotation
    rotation_matrix = generate_random_rotation_matrix()

    # Anwenden von Rotation auf das 3D-Objekt
    mesh.transform(rotation_matrix)

    # Visualisiere das 3D-Objekt
    plotter = pv.Plotter(off_screen=True)
    plotter.add_mesh(mesh, color='white', show_edges=False)

    # Screenshot speichern
    screenshot_path = f'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/TestDir/Planetengetriebe_meshes/sun_c_{i}.png'
    plotter.screenshot(screenshot_path, transparent_background=True)
    plotter.close()

    # Laden Sie das Hintergrundbild
    background_image = Image.open(background_image_path)

    # Laden Sie das gespeicherte Bild, das eingefügt werden soll
    rotated_image_path = screenshot_path
    rotated_image = Image.open(rotated_image_path)

    scaling_factor = np.random.uniform(0.1, 0.5)

    # Größe des Screenshots ändern (verkleinern oder vergrößern)
    new_size = (int(rotated_image.width * scaling_factor),
                int(rotated_image.height * scaling_factor))

    rotated_image = rotated_image.resize(new_size)

    # Einfügen des veränderten Bildes in das Hintergrundbild in der Mitte
    bg_width, bg_height = background_image.size
    rotated_width, rotated_height = rotated_image.size
    paste_position = (np.random.randint(0, bg_width - rotated_width),
                      np.random.randint(0, bg_height - rotated_height))
    background_image.paste(rotated_image, paste_position, rotated_image)

    # Speichern Sie das endgültige Bild
    final_image_path = f'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/TestDir/Planetengetriebe_meshes/SynData/sun_with_blue_color_{i}.png'
    background_image.save(final_image_path)

    # Löschen des Screenshots des 3D-Modells
    os.remove(screenshot_path)
