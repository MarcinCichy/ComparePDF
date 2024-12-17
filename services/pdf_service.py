import fitz
import logging
from PIL import Image
from typing import Optional
import concurrent.futures
from models.pdf_document import PDFDocument, ComparisonResult
from utils.image_utils import compare_images, resize_image_to_fit
from config.settings import DEFAULT_DPI, PDF_LOAD_TIMEOUT, COMPARISON_TIMEOUT

class PDFService:
    """Serwis do operacji na dokumentach PDF."""

    @staticmethod
    def load_pdf(file_path: str, testing_mode: bool = False, dpi: int = DEFAULT_DPI) -> Optional[PDFDocument]:
        """Ładuje dokument PDF i konwertuje pierwszą stronę na obraz."""
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(PDFService._load_pdf_page, file_path, dpi, testing_mode)
                document = future.result(timeout=PDF_LOAD_TIMEOUT)
                return document
        except concurrent.futures.TimeoutError:
            logging.error(f"PDF loading timed out for {file_path}")
            raise TimeoutError(f"Loading PDF file timed out after {PDF_LOAD_TIMEOUT} seconds")
        except Exception as e:
            logging.error(f"Failed to load PDF {file_path}: {e}")
            return None

    @staticmethod
    def _load_pdf_page(file_path: str, dpi: int, testing_mode: bool) -> PDFDocument:
        """Wewnętrzna metoda do ładowania strony PDF."""
        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)

        document = PDFDocument(file_path=file_path)

        with fitz.open(file_path) as pdf:
            page = pdf.load_page(0)
            pix = page.get_pixmap(matrix=mat)

            # Konwersja na obraz PIL
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            document.page_image = img

            # Tworzenie podglądu
            document.preview_image = resize_image_to_fit(
                img.copy(),
                (350, 150),  # Rozmiar podglądu
                testing_mode
            )

            if testing_mode:
                img.save(f"{file_path}_page_test.png", "PNG")
                document.preview_image.save(f"{file_path}_preview_test.png", "PNG")

        return document

    @staticmethod
    def compare_documents(base_doc: PDFDocument,
                          compare_doc: PDFDocument,
                          sensitivity: int,
                          testing_mode: bool = False) -> Optional[ComparisonResult]:
        """Porównuje dwa dokumenty PDF."""
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    PDFService._compare_images,
                    base_doc,
                    compare_doc,
                    sensitivity,
                    testing_mode
                )
                result = future.result(timeout=COMPARISON_TIMEOUT)
                return result
        except concurrent.futures.TimeoutError:
            logging.error("PDF comparison timed out")
            raise TimeoutError(f"Comparison timed out after {COMPARISON_TIMEOUT} seconds")
        except Exception as e:
            logging.error(f"Failed to compare documents: {e}")
            return None

    @staticmethod
    def _compare_images(base_doc: PDFDocument,
                        compare_doc: PDFDocument,
                        sensitivity: int,
                        testing_mode: bool) -> ComparisonResult:
        """Wewnętrzna metoda do porównywania obrazów."""
        if not (base_doc.is_loaded() and compare_doc.is_loaded()):
            raise ValueError("Both documents must be loaded")

        diff_image, original_image = compare_images(
            base_doc.page_image,
            compare_doc.page_image,
            sensitivity,
            testing_mode
        )

        if diff_image is None or original_image is None:
            raise ValueError("Image comparison failed")

        if testing_mode:
            diff_image.save(f"{base_doc.file_path}_diff_test.png", "PNG")
            original_image.save(f"{base_doc.file_path}_original_test.png", "PNG")

        return ComparisonResult(
            diff_image=diff_image,
            original_image=original_image,
            base_document=base_doc,
            compare_document=compare_doc,
            sensitivity=sensitivity
        )

    @staticmethod
    def cleanup_document(document: PDFDocument):
        """Czyści zasoby dokumentu."""
        if document:
            document.clear()
