from PyQt5.QtGui import QImage, QPixmap
from PIL import Image, ImageChops, ImageDraw
from typing import Tuple, Optional
import numpy as np
import cv2
import logging
from config.settings import DIFFERENCE_COLOR, DIFFERENCE_OUTLINE_WIDTH

def pil2qimage(pil_image):
    """Konwertuje obraz PIL na QImage bez zmiany kolejności kanałów."""
    try:
        if pil_image.mode == "RGB":
            # Bez zamiany kanałów
            arr = pil_image.tobytes()
            return QImage(arr, pil_image.width, pil_image.height,
                          pil_image.width * 3, QImage.Format_RGB888)
        elif pil_image.mode == "RGBA":
            # Dla RGBA również bez zamiany kanałów
            arr = pil_image.tobytes()
            return QImage(arr, pil_image.width, pil_image.height,
                          pil_image.width * 4, QImage.Format_RGBA8888)
        else:
            # Konwersja do RGBA w razie innego trybu i ponowna próba
            pil_image = pil_image.convert("RGBA")
            return pil2qimage(pil_image)
    except Exception as e:
        logging.error(f"Failed to convert PIL image to QImage: {e}")
        return None

def compare_images(base_image: Image.Image,
                   compare_image: Image.Image,
                   sensitivity: int = 15,
                   testing_mode: bool = False) -> Tuple[Optional[Image.Image], Optional[Image.Image]]:
    """Porównuje dwa obrazy i zwraca obraz z zaznaczonymi różnicami."""
    try:
        # Konwersja do RGB jeśli potrzebna
        if base_image.mode != 'RGB':
            base_image = base_image.convert('RGB')
        if compare_image.mode != 'RGB':
            compare_image = compare_image.convert('RGB')

        # Wyrównanie rozmiarów obrazów
        if base_image.size != compare_image.size:
            compare_image = resize_image_to_fit(compare_image, base_image.size, testing_mode)

        # Obliczanie różnicy
        diff = ImageChops.difference(base_image, compare_image)
        if testing_mode:
            diff.save("image_difference_grayscale_test.png", "PNG")

        diff = diff.convert('L')
        diff = diff.point(lambda x: 255 if x > sensitivity else 0)

        if testing_mode:
            diff.save("image_difference_thresholded_test.png", "PNG")

        # Znajdowanie konturów
        diff_array = np.array(diff).astype(np.uint8)

        # Zapis pliku tekstowego z różnicami
        if testing_mode:
            np.savetxt("difference_matrix_test.txt", diff_array, fmt='%d')
            logging.info("Plik difference_matrix_test.txt został pomyślnie zapisany.")

        contours, _ = cv2.findContours(diff_array,
                                       cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

        # Rysowanie prostokątów
        result_image = base_image.copy()
        draw = ImageDraw.Draw(result_image)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            draw.rectangle(
                [x-5, y-5, x+w+5, y+h+5],
                outline=DIFFERENCE_COLOR,
                width=DIFFERENCE_OUTLINE_WIDTH
            )

        if testing_mode:
            result_image.save("result_image_test.png", "PNG")
            base_image.save("original_image_test.png", "PNG")

        return result_image, base_image.copy()

    except Exception as e:
        logging.error(f"Failed to compare images: {e}")
        return None, None

def resize_image_to_fit(image: Image.Image, max_size: Tuple[int, int], testing_mode: bool = False) -> Image.Image:
    """Zmienia rozmiar obrazu zachowując proporcje."""
    try:
        ratio = min(max_size[0] / image.size[0], max_size[1] / image.size[1])
        new_size = tuple(int(dim * ratio) for dim in image.size)
        resized_image = image.resize(new_size, Image.LANCZOS)
        if testing_mode:
            resized_image.save("resized_image_test.png", "PNG")
        return resized_image
    except Exception as e:
        logging.error(f"Failed to resize image: {e}")
        return image
