import cv2

def draw_boxes(image_path, label_path, output_path):
    try:
        # Lese das Bild
        image = cv2.imread(image_path)

        # Höhe und Breite des Bildes
        img_height, img_width, _ = image.shape

        # Lese die Label-Datei
        with open(label_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            try:
                # Trenne die Werte in der Zeile
                class_id, x, y, width, height = map(float, line.strip().split())

                # Konvertiere die normalisierten Koordinaten in Pixel-Koordinaten
                x_pixel = int(x * img_width)
                y_pixel = int(y * img_height)
                width_pixel = int(width * img_width)
                height_pixel = int(height * img_height)

                # Zeichne die Bounding-Box auf das Bild
                cv2.rectangle(image, (x_pixel - width_pixel//2, y_pixel - height_pixel//2),
                              (x_pixel + width_pixel//2, y_pixel + height_pixel//2),
                              color=(0, 255, 0), thickness=2)

                # Füge den Klassennamen hinzu (optional)
                class_name = f"Class {int(class_id)}"
                cv2.putText(image, class_name, (x_pixel, y_pixel - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            except Exception as e:
                print(f"Fehler beim Verarbeiten der Zeile: {e}")
                continue

        # Speichere das Ausgabebild
        print("Speichern")
        cv2.imwrite(output_path, image)

    except Exception as e:
        print(f"Fehler beim Verarbeiten der Dateien: {e}")

files = '/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/TestDir/images'

for i in range(len(files)):
    # Beispielaufruf
    image_path = f'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/TestDir/images/sun_{i}.jpg'
    label_path = f'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/TestDir/labels/sun_{i}.txt'
    output_path = f'/Users/michaelkravt/PycharmProjects/BA_Repo/Tools/MainDir/TestDir/labeled_images/output_{i}.jpg'

    draw_boxes(image_path, label_path, output_path)
