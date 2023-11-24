from PIL import Image

import pyvista as pv

import numpy as np

# STL-Datei laden

your_stl_file = r'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/TestDir/Planetengetriebe_meshes/ring.stl'

mesh = pv.read(your_stl_file)

angle_degrees = 45.0

angle_radians = np.radians(angle_degrees)

# Rotationsmatrix erstellen

rotation_matrix = np.array([

    [np.cos(angle_radians), -np.sin(angle_radians), 0, 0],

    [np.sin(angle_radians), np.cos(angle_radians), 0, 0],

    [0, 0, 1, 0],

    [0, 0, 0, 1]

])

# 3D-Objekt transformieren (rotieren)

mesh.transform(rotation_matrix)

# 3D-Objekt visualisieren

plotter = pv.Plotter(off_screen=True)

plotter.add_mesh(mesh, color='lightgrey', show_edges=False)

plotter.screenshot(r'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/TestDir/Planetengetriebe_meshes/ring.png',
                   transparent_background=True)

plotter.close()

# Laden Sie das vorhandene Hintergrund-PNG

background_image_path = r'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/TestDir/a-room-at-the-beach.jpg'

background_image = Image.open(background_image_path)

# Laden Sie das gespeicherte PNG, das eingefügt werden soll

rotated_image_path = r'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/TestDir/Planetengetriebe_meshes/ring.png'

rotated_image = Image.open(rotated_image_path)

# Einfügen des Rotationsbildes in das Hintergrundbild

background_image.paste(rotated_image, (500, 500), rotated_image)

# Speichern Sie das endgültige Bild

final_image_path = r'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/TestDir/Planetengetriebe_meshes/ring.png'

background_image.save(final_image_path)