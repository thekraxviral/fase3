import os
import csv
import cv2
import pytesseract

# Configurar la ruta hacia el ejecutable de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold_image = cv2.threshold(grayscale_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return pytesseract.image_to_string(threshold_image)


# Obtener la ruta del directorio actual
current_dir = os.getcwd()

# Obtener la ruta del directorio de capturas de pantalla
screenshots_dir = os.path.join(current_dir, 'screenshots')

# Crear el directorio de capturas de pantalla si no existe
os.makedirs(screenshots_dir, exist_ok=True)

# Obtener la ruta del archivo CSV
csv_file_path = os.path.join(current_dir, 'publicaciones.csv')

try:
    # Crear o abrir el archivo CSV para guardar la información extraída
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['ID', 'Texto de la publicación'])  # Encabezado del archivo CSV

        # Procesar cada archivo de captura de pantalla
        for screenshot_file in os.listdir(screenshots_dir):
            # Obtener la ruta completa del archivo de captura de pantalla
            screenshot_path = os.path.join(screenshots_dir, screenshot_file)
            
            # Obtener el texto de la captura de pantalla utilizando OCR
            current_text = extract_text_from_image(screenshot_path)

            # Generar un identificador único (usando el nombre del archivo sin extensión)
            image_id = os.path.splitext(screenshot_file)[0]
            separator_line = '-' * 20

            # Guardar el identificador y el texto extraído en el archivo CSV
            writer.writerow([image_id, separator_line])
            writer.writerow([current_text])

    print('---------------------------------------------------')
    print('.         Procesamiento completado                .')
    print('---------------------------------------------------')

except Exception as e:
    print("Ocurrió un error:", e)
