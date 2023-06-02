import os
import shutil
import csv
import uuid
import cv2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytesseract
import subprocess

# Configurar la ruta hacia el ejecutable de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

try:
    # Configurar las opciones del navegador para desactivar las notificaciones
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")

    # Iniciar el navegador Chrome con las opciones configuradas
    driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)

    # Abrir Facebook
    driver.get('https://www.facebook.com')

    # Iniciar sesión en Facebook (modifica con tus credenciales)
    email = '3016086924'
    password = 'Mm1004374386'
    email_input = driver.find_element(By.ID, 'email')
    email_input.send_keys(email)
    password_input = driver.find_element(By.ID, 'pass')
    password_input.send_keys(password)
    login_button = driver.find_element(By.NAME, 'login')
    login_button.click()
    print('---------------------------------------------------')
    print('.         Sesión iniciada con éxito               .')
    print('---------------------------------------------------')

    # Esperar 5 segundos después de iniciar sesión
    driver.implicitly_wait(5)

    # Mover el cursor del mouse al campo de búsqueda y hacer clic en él
    search_bar = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Buscar en Facebook"]')
    actions = ActionChains(driver)
    actions.move_to_element(search_bar).click().perform()

    # Esperar a que se cargue el campo de búsqueda
    wait = WebDriverWait(driver, 10)
    search_bar = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Buscar en Facebook"]')))

    # Interactuar con el campo de búsqueda
    search_bar.send_keys("cover")
    search_bar.send_keys(Keys.RETURN)
    print('---------------------------------------------------')
    print('.         Búsqueda realizada con éxito            .')
    print('---------------------------------------------------')

    # Esperar a que se carguen todos los resultados
    time.sleep(5)  # Esperar un tiempo suficiente para que se carguen las publicaciones (puedes ajustar este valor)

    # Definir la ruta de la imagen de referencia del final de la página
    reference_image_path = 'end_of_page.png'

    # Cargar la imagen de referencia
    reference_image = cv2.imread(reference_image_path, cv2.IMREAD_COLOR)

    # Obtener el tamaño de la imagen de referencia
    reference_image_height, reference_image_width, _ = reference_image.shape

    # Variable para almacenar la posición vertical del último desplazamiento
    last_scroll_position = 0

    # Variable para almacenar el número de desplazamientos sin encontrar el final de la página
    no_end_of_page_count = 0

    # Obtener la ruta del directorio actual
    current_dir = os.getcwd()

    # Obtener la ruta del directorio de capturas de pantalla
    screenshots_dir = os.path.join(current_dir, 'screenshots')

    # Crear el directorio de capturas de pantalla si no existe
    os.makedirs(screenshots_dir, exist_ok=True)

    # Configurar la velocidad de desplazamiento y la espera entre capturas
    scroll_speed = 50  # Valor más bajo para un desplazamiento más lento
    capture_delay = 1  # Valor más alto para una espera más larga entre capturas

    # Realizar el scroll hasta el final de la página
    while True:
        # Tomar una captura de pantalla de la página actual
        screenshot_path = os.path.join(screenshots_dir, f'screenshot_{uuid.uuid4().hex}.png')
        driver.save_screenshot(screenshot_path)

        # Hacer scroll hacia abajo para cargar más contenido
        driver.execute_script(f"window.scrollBy(0, {scroll_speed});")

        # Esperar antes de tomar la siguiente captura de pantalla
        time.sleep(capture_delay)

        # Obtener la posición vertical actual del scroll
        current_scroll_position = driver.execute_script('return window.pageYOffset;')

        if current_scroll_position == last_scroll_position:
            # Si la posición vertical del scroll no ha cambiado, se asume que no hay más contenido y se detiene el ciclo
            print('---------------------------------------------------')
            print('.         Fin de la página alcanzado              .')
            print('---------------------------------------------------')
            break
        else:
            # Actualizar la posición vertical del último desplazamiento
            last_scroll_position = current_scroll_position

    print('---------------------------------------------------')
    print('.       Captura de imágenes completada           .')
    print('---------------------------------------------------')

    
except Exception as e:
    print("Ocurrió un error:", e)

    # Cerrar el navegador en caso de error
    driver.quit()
