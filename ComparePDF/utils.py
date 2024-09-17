from PyQt5.QtGui import QImage, QPixmap
from PIL import Image, ImageChops, ImageDraw
import numpy as np
import fitz
import cv2


def pil2qimage(pil_image):
    """Converts a PIL Image to QImage."""
    try:
        print(f"Converting PIL image to QImage. Size: {pil_image.size}, Mode: {pil_image.mode}")
        if pil_image.mode == "RGB":
            data = pil_image.tobytes("raw", "RGB")
            qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGB888)
            qimage = qimage.rgbSwapped()  # Swap RGB to BGR
        elif pil_image.mode == "RGBA":
            data = pil_image.tobytes("raw", "RGBA")
            qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGBA8888)
            qimage = qimage.rgbSwapped()  # Swap RGBA to BGRA
        elif pil_image.mode == "L":
            data = pil_image.tobytes("raw", "L")
            qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format_Grayscale8)
        else:
            pil_image = pil_image.convert("RGBA")
            data = pil_image.tobytes("raw", "RGBA")
            qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGBA8888)
            qimage = qimage.rgbSwapped()
        print("Conversion successful.")
        return qimage
    except Exception as e:
        print(f"An error occurred while converting PIL image to QImage: {e}")
        return None


def pdf_to_image(pdf_path, dpi=72):
    """Converts the first page of a PDF to a PIL Image."""
    try:
        print(f"Converting PDF to image: {pdf_path}")
        zoom = dpi / 72  # 72 DPI is the default value
        mat = fitz.Matrix(zoom, zoom)
        with fitz.open(pdf_path) as doc:
            page = doc.load_page(0)
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        print(f"Successfully converted PDF to image: {pdf_path}")
        return img
    except Exception as e:
        print(f"Failed to convert PDF to image: {e}")
        return None


def compare_images(base_image, compare_image, sensitivity=15):
    """Compares two PIL Images and returns an image with differences highlighted.
    Sensitivity determines the minimum pixel value difference (0-255) considered significant."""
    try:
        print(f"Comparing images with sensitivity: {sensitivity}")
        if base_image is None or compare_image is None:
            print("One of the images was not loaded.")
            return None, None
        if base_image.mode != 'RGB':
            base_image = base_image.convert('RGB')
        if compare_image.mode != 'RGB':
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
