from dataclasses import dataclass
from typing import Optional
from PIL import Image

@dataclass
class PDFDocument:
    """Reprezentuje pojedynczy dokument PDF."""
    file_path: str
    page_image: Optional[Image.Image] = None
    preview_image: Optional[Image.Image] = None

    def is_loaded(self) -> bool:
        """Sprawdza czy dokument został poprawnie załadowany."""
        return self.page_image is not None

    def clear(self):
        """Czyści załadowane obrazy."""
        self.page_image = None
        self.preview_image = None


@dataclass
class ComparisonResult:
    """Przechowuje wyniki porównania dwóch dokumentów PDF."""
    diff_image: Optional[Image.Image] = None
    original_image: Optional[Image.Image] = None
    base_document: Optional[PDFDocument] = None
    compare_document: Optional[PDFDocument] = None
    sensitivity: int = 0
    differences_count: int = 0

    def is_valid(self) -> bool:
        """Sprawdza czy porównanie zostało wykonane poprawnie."""
        return all([self.diff_image, self.original_image])

    def clear(self):
        """Czyści wyniki porównania."""
        self.diff_image = None
        self.original_image = None
        self.differences_count = 0
