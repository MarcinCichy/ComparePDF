# Image settings
MAX_IMAGE_SIZE = 50 * 1024 * 1024  # 50 MB
DEFAULT_DPI = 72
DEFAULT_SENSITIVITY = 15

# UI settings
WINDOW_TITLE = 'PDF Comparator v2.1'
PREVIEW_PANEL_WIDTH = 450
PREVIEW_MIN_SIZE = (350, 150)

# Messages
MSG_LOAD_PDF_1 = "Click to load the first PDF file"
MSG_LOAD_PDF_2 = "Click to load the second PDF file"
MSG_COMPARING = "Comparing PDFs..."
MSG_SELECT_FILES = "Please upload both PDF files."
MSG_SELECT_BASE = "Please select the base file using the radio buttons."
MSG_ERROR_LOAD = "Error loading file: {}"
MSG_ERROR_COMPARE = "Error comparing documents: {}"
MSG_ERROR_GENERAL = "Wystąpił nieoczekiwany błąd: {}"

# Timeouts
PDF_LOAD_TIMEOUT = 15
COMPARISON_TIMEOUT = 30

# Colors
DIFFERENCE_COLOR = (255, 0, 0)  # Red
DIFFERENCE_OUTLINE_WIDTH = 3

# Layout
SLIDER_MIN = 1
SLIDER_MAX = 100
ZOOM_FACTOR_IN = 1.25
ZOOM_FACTOR_OUT = 0.8
