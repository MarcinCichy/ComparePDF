from PyQt5.QtGui import QImage
from PIL import Image, ImageChops, ImageDraw
import numpy as np
import fitz
import cv2


def pil2qimage(pil_image):
    """Konwertuje obraz PIL na obraz QImage."""
    try:
        print(f"Converting PIL image to QImage. Size: {pil_image.size}, Mode: {pil_image.mode}")
        data = pil_image.tobytes()
        if pil_image.mode == "RGB":
            img = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGB888)
            print("Conversion successful. Format: RGB888")
            return img
        elif pil_image.mode == "RGBA":
            img = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGBA8888)
            print("Conversion successful. Format: RGBA8888")
            return img
        elif pil_image.mode == "L":
            img = QImage(data, pil_image.width, pil_image.height, QImage.Format_Grayscale8)
            print("Conversion successful. Format: Grayscale8")
            return img
        print("Conversion failed. Unsupported format.")
        return None
    except Exception as e:
        print(f"An error occurred while converting PIL image to QImage: {e}")
        return None


def pdf_to_image(pdf_path):
    """Konwertuje pierwszą stronę PDF na obraz PIL."""
    try:
        print(f"Converting PDF to image: {pdf_path}")
        with fitz.open(pdf_path) as doc:
            page = doc.load_page(0)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        print(f"Successfully converted PDF to image: {pdf_path}")
        return img
    except Exception as e:
        print(f"Failed to convert PDF to image: {e}")
        return None


def compare_images(base_image, compare_image, sensitivity=15):
    """Porównuje dwa obrazy PIL i zwraca obraz z zaznaczonymi różnicami.
    Sensitivity określa minimalną różnicę w wartościach pikseli (0-255), która jest uznawana za znaczącą."""
    try:
        print(f"Comparing images with sensitivity: {sensitivity}")
        if base_image is None or compare_image is None:
            print("One of the images was not loaded.")
            return None, None
        if base_image.mode != 'RGB' or compare_image.mode != 'RGB':
            base_image = base_image.convert('RGB')
            compare_image = compare_image.convert('RGB')

        print("Calculating difference between images.")
        diff = ImageChops.difference(base_image, compare_image)
        diff = diff.convert('L')
        diff = diff.point(lambda x: 255 if x > sensitivity else 0, '1')
        diff_array = np.array(diff)

        print("Finding contours of differences.")
        diff_array = diff_array.astype(np.uint8)
        contours, _ = cv2.findContours(diff_array, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        original_image = base_image.copy()

        print(f"Drawing rectangles around differences: found {len(contours)} differences.")
        draw = ImageDraw.Draw(base_image)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            draw.rectangle([x - 5, y - 5, x + w + 5, y + h + 5], outline="red", width=3)

        print("Comparison complete.")
        return base_image, original_image
    except Exception as e:
        print(f"An error occurred while comparing images: {e}")
        return None, None
