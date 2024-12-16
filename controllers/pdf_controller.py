from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog
import logging
from models.pdf_document import PDFDocument, ComparisonResult
from services.pdf_service import PDFService
from utils.image_utils import pil2qimage
from config.settings import DEFAULT_SENSITIVITY, MSG_SELECT_FILES

MSG_ERROR_LOAD = "Błąd podczas ładowania pliku: {}"
MSG_ERROR_COMPARE = "Błąd podczas porównywania dokumentów: {}"
MSG_COMPARING = "Porównywanie dokumentów..."

class PDFController(QObject):
    def __init__(self):
        super().__init__()
        logging.debug("Initializing PDFController")
        self._init_services()
        self._init_variables()
        logging.debug("PDFController initialized successfully")

    def _init_services(self):
        self.pdf_service = PDFService()

    def _init_variables(self):
        # self.view pozostawiamy bez zmian - nie resetujemy jej tutaj.
        # Pozostałe zmienne pozostają bez zmian.
        self.doc1 = None
        self.doc2 = None
        self.base_doc_num = 1
        self.sensitivity = DEFAULT_SENSITIVITY
        self.comparison_result = None
        self.current_operation = None

    def set_view(self, view):
        self.view = view

    @pyqtSlot(int)
    def set_base_document(self, doc_num: int):
        """Ustawia dokument bazowy do porównania."""
        try:
            logging.debug(f"Setting base document to {doc_num}")
            self.base_doc_num = doc_num
            if self.doc1 and self.doc2:
                self.compare_documents()
        except Exception as e:
            logging.error(f"Error setting base document: {e}")
            if self.view:
                self.view.show_error(f"Error setting base document: {str(e)}")

    @pyqtSlot(int)
    def load_file(self, doc_num: int):
        """Obsługuje ładowanie pliku PDF."""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self.view,
                f"Select PDF file {doc_num}",
                "",
                "PDF files (*.pdf)"
            )

            if not file_path:
                return

            self.view.show_progress(f"Loading PDF file {doc_num}...")

            # Ładowanie dokumentu
            document = self.pdf_service.load_pdf(file_path)
            if not document:
                raise Exception(f"Failed to load PDF file {doc_num}")

            # Aktualizacja stanu
            if doc_num == 1:
                self.doc1 = document
            else:
                self.doc2 = document

            # Aktualizacja UI
            self._update_preview(doc_num, document)

            self.view.hide_progress()

            # Automatyczne porównanie jeśli oba dokumenty są załadowane
            if self.doc1 and self.doc2:
                self.compare_documents()

        except Exception as e:
            logging.error(f"Error loading file: {e}")
            if self.view:
                self.view.hide_progress()
                self.view.show_error(MSG_ERROR_LOAD.format(str(e)))

    def _update_preview(self, doc_num: int, document: PDFDocument):
        """Aktualizuje podgląd dokumentu."""
        try:
            if document and document.preview_image:
                qimage = pil2qimage(document.preview_image)
                if qimage:
                    pixmap = QPixmap.fromImage(qimage)
                    self.view.preview_panel.update_preview(doc_num, pixmap)
        except Exception as e:
            logging.error(f"Error updating preview: {e}")

    @pyqtSlot(int)
    def set_sensitivity(self, value: int):
        """Ustawia czułość porównywania."""
        self.sensitivity = value
        if self.doc1 and self.doc2:
            self.compare_documents()

    @pyqtSlot()
    def compare_documents(self):
        """Wykonuje porównanie dokumentów."""
        try:
            if not (self.doc1 and self.doc2):
                # Brak załadowanych obu dokumentów - wyświetlamy komunikat błędu
                if self.view:
                    self.view.show_error(MSG_SELECT_FILES)
                return

            if self.view:
                self.view.show_progress(MSG_COMPARING)

            # Określenie dokumentu bazowego i porównywanego
            base_doc = self.doc1 if self.base_doc_num == 1 else self.doc2
            compare_doc = self.doc2 if self.base_doc_num == 1 else self.doc1

            # Porównanie dokumentów
            self.comparison_result = self.pdf_service.compare_documents(
                base_doc,
                compare_doc,
                self.sensitivity
            )

            if self.comparison_result and self.comparison_result.is_valid():
                # Konwersja wyniku na QImage i wyświetlenie
                result_qimage = pil2qimage(self.comparison_result.diff_image)
                if result_qimage and self.view:
                    self.view.graphics_view.setPhoto(QPixmap.fromImage(result_qimage))
            else:
                raise Exception("Comparison failed")

            if self.view:
                self.view.hide_progress()

        except Exception as e:
            logging.error(f"Error comparing documents: {e}")
            if self.view:
                self.view.hide_progress()
                self.view.show_error(MSG_ERROR_COMPARE.format(str(e)))

    @pyqtSlot()
    def reset(self):
        """Resetuje stan aplikacji."""
        try:
            # Zapisujemy widok, aby go nie stracić
            current_view = self.view
            self._init_variables()
            # Przywracamy zapisany widok
            self.view = current_view

            if self.view:
                self.view.preview_panel.clear_preview(1)
                self.view.preview_panel.clear_preview(2)
                self.view.graphics_view.setPhoto(None)
        except Exception as e:
            logging.error(f"Error resetting application: {e}")

    @pyqtSlot()
    def clear(self):
        """Czyści wynik porównania i pokazuje oryginalny dokument."""
        try:
            if self.comparison_result and self.comparison_result.original_image:
                original_qimage = pil2qimage(self.comparison_result.original_image)
                if original_qimage and self.view:
                    self.view.graphics_view.setPhoto(QPixmap.fromImage(original_qimage))
        except Exception as e:
            logging.error(f"Error clearing comparison: {e}")

    def cancel_operation(self):
        """Anuluje bieżącą operację."""
        if self.current_operation:
            self.current_operation.cancel()
            self.current_operation = None
