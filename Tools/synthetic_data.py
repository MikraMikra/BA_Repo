from PIL import Image
import pyvista as pv
import numpy as np

# STL-Datei laden
your_stl_file = r'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/TestDir/Planetengetriebe_meshes/sun_c.stl'
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
# Änderung: Das Mesh wird jetzt blau gefärbt
plotter.add_mesh(mesh, color='white', show_edges=False)

plotter.screenshot(r'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/TestDir/Planetengetriebe_meshes/sun_c.png',
                   transparent_background=True)

plotter.close()

# Laden Sie das vorhandene Hintergrund-PNG
background_image_path = r'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/TestDir/a-room-at-the-beach.jpg'
background_image = Image.open(background_image_path)

# Laden Sie das gespeicherte PNG, das eingefügt werden soll
rotated_image_path = r'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/TestDir/Planetengetriebe_meshes/sun_c.png'
rotated_image = Image.open(rotated_image_path)
# Ermitteln der Breite und Höhe des Hintergrundbildes
bg_width, bg_height = background_image.size
print(bg_width, bg_height)

# Ermitteln der Breite und Höhe des rotierten Bildes
rotated_width, rotated_height = rotated_image.size
print(rotated_width, rotated_height)

# Berechnen der Position, um das rotierte Bild in der Mitte des Hintergrundbildes zu platzieren
paste_position = ((bg_width - rotated_width) // 2, (bg_height - rotated_height) // 2)
print(paste_position)

# Einfügen des Rotationsbildes in das Hintergrundbild in der Mitte
background_image.paste(rotated_image, paste_position, rotated_image)

# Einfügen des Rotationsbildes in das Hintergrundbild
#background_image.paste(rotated_image, (640, 0), rotated_image)

# Speichern Sie das endgültige Bild
final_image_path = r'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/TestDir/Planetengetriebe_meshes/sun_with_blue_color.png'
background_image.save(final_image_path)
