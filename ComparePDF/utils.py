from PyQt5.QtGui import QImage
from PIL import Image, ImageChops, ImageDraw
import numpy as np
import fitz  # PyMuPDF


def pil2qimage(pil_image):
    """Konwertuje obraz PIL na obraz QImage."""
    data = pil_image.tobytes()
    if pil_image.mode == "RGB":
        img = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGB888)
        return img
    elif pil_image.mode == "RGBA":
        img = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGBA8888)
        return img
    elif pil_image.mode == "L":
        img = QImage(data, pil_image.width, pil_image.height, QImage.Format_Grayscale8)
        return img
    return None


def pdf_to_image(pdf_path):
    """Konwertuje pierwszą stronę PDF na obraz PIL."""
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    doc.close()
    return img


def compare_images(base_image, compare_image, sensitivity=15):
    """Porównuje dwa obrazy PIL i zwraca obraz z zaznaczonymi różnicami.
    Sensitivity określa minimalną różnicę w wartościach pikseli (0-255), która jest uznawana za znaczącą."""
    if base_image is None or compare_image is None:
        print("Jeden z obrazów nie został wczytany.")
        return None
    if base_image.mode != 'RGB' or compare_image.mode != 'RGB':
        base_image = base_image.convert('RGB')
        compare_image = compare_image.convert('RGB')

    diff = ImageChops.difference(base_image, compare_image)
    diff = diff.convert('L')
    # Ustawienie progu w punkcie określonym przez sensitivity
    diff = diff.point(lambda x: 255 if x > sensitivity else 0, '1')
    diff_array = np.array(diff)

    # Znajdowanie konturów i zaznaczanie ich na bazowym obrazie
    import cv2
    diff_array = diff_array.astype(np.uint8)
    contours, _ = cv2.findContours(diff_array, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    draw = ImageDraw.Draw(base_image)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        draw.rectangle([x - 5, y - 5, x + w + 5, y + h + 5], outline="red", width=3)

    return base_image


def save_image_to_pdf(image, filename):
    """Zapisuje obraz PIL do pliku PDF."""
    image.save(filename, "PDF", resolution=100.0)
