from PIL import Image, ImageDraw


def draw_bounding_box(image, label_file, bg_width, bg_height):
    # Öffne die Textdatei und lies die Bounding Box-Koordinaten
    with open(label_file, 'r') as f:
        content = f.readline().split()
        class_id, x_min_normalized, y_min_normalized, width_normalized, height_normalized = map(float, content)

    # Skaliere die Koordinaten auf die Bildgröße
    x_min = int(x_min_normalized * bg_width)
    y_min = int(y_min_normalized * bg_height)
    width = int(width_normalized * bg_width)
    height = int(height_normalized * bg_height)

    # Zeichne die Bounding Box auf dem Bild
    draw = ImageDraw.Draw(image)
    draw.rectangle([x_min, y_min, x_min + width, y_min + height], outline='red', width=2)

# Lade und zeichne die Bounding Boxen für jedes Bild
for i in range(10):
    # Lade das Hintergrundbild
    bg_image_path = f'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/TestDir/Planetengetriebe_meshes/SynData/sun_with_blue_color_{i}.png'
    bg_image = Image.open(bg_image_path)
    bg_width, bg_height = bg_image.size

    label_file = f'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/TestDir/Planetengetriebe_meshes/SynData/labels/label_{i}.txt'

    # Öffne das Hintergrundbild erneut, um die ursprüngliche Kopie zu behalten
    image_with_boxes = Image.open(bg_image_path).convert("RGB")

    # Zeichne die Bounding Box
    draw_bounding_box(image_with_boxes, label_file, bg_width, bg_height)

    # Zeige das Bild mit Bounding Box an
    image_with_boxes.show()
