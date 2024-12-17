import fitz
from PIL import Image, ImageChops, ImageDraw
import numpy as np
import cv2
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)


class PDFComparator:
    def __init__(self, sensitivity=15, testing_mode=False):
        self.sensitivity = sensitivity
        self.testing_mode = testing_mode

    def pdf_to_image(self, pdf_path, dpi=72):
        """Konwertuje pierwszy PDF na obraz."""
        try:
            logger.info(f"Konwersja PDF do obrazu: {pdf_path}")
            zoom = dpi / 72
            mat = fitz.Matrix(zoom, zoom)
            with fitz.open(pdf_path) as doc:
                page = doc.load_page(0)
                pix = page.get_pixmap(matrix=mat)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                if self.testing_mode:
                    img.save(f"{pdf_path}_converted_test.png", "PNG")

                return img
        except Exception as e:
            logger.error(f"Błąd podczas konwersji PDF do obrazu: {e}")
            return None

    def compare_images(self, base_image, compare_image):
        """Porównuje dwa obrazy PIL."""
        try:
            logger.info(f"Porównywanie obrazów z czułością: {self.sensitivity}")
            if base_image is None or compare_image is None:
                logger.error("Jeden z obrazów nie został załadowany.")
                return None, None

            diff = ImageChops.difference(base_image, compare_image)
            if self.testing_mode:
                diff.save("image_difference_grayscale_test.png", "PNG")

            diff = diff.convert('L').point(lambda x: 255 if x > self.sensitivity else 0, '1')

            if self.testing_mode:
                diff.save("image_difference_thresholded_test.png", "PNG")

            diff_array = np.array(diff).astype(np.uint8)
            contours, _ = cv2.findContours(diff_array, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            original_image = base_image.copy()
            draw = ImageDraw.Draw(base_image)
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                draw.rectangle([x - 5, y - 5, x + w + 5, y + h + 5], outline=(255, 0, 0), width=2)

            return base_image, original_image
        except Exception as e:
            logger.error(f"Błąd podczas porównywania obrazów: {e}")
            return None, None
