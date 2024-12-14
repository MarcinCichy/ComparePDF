# PDF Comparator v2.0

PDF Comparator v2.0 is a PyQt5-based desktop application designed to visually compare two PDF files. It highlights differences between the PDFs, allowing users to quickly identify changes or discrepancies. The application also includes additional features like sensitivity adjustment, file preview, and printing options.

## Features

- **PDF Comparison**: Compare two PDF files and highlight differences using visual markers.
- **Custom Sensitivity**: Adjust sensitivity to fine-tune the detection of differences.
- **Drag-and-Zoom**: Interactive view of the compared images with mouse drag and zoom.
- **PDF Preview**: Preview the loaded PDF files before comparison.
- **Result Printing**: Print the comparison result directly from the application.
- **Error Handling**: Robust error handling with descriptive messages for user convenience.

## How the PDF Comparison Works

### 1. Loading PDF Files
Users select two PDF files to be compared. This is handled by the `loadFile` method in the `PDFComparer` class. 
Each file is loaded using the `PDFLoadTask` class, which utilizes PyMuPDF (fitz) to convert the first page of each PDF into an image (bitmap) via the `load_pdf` method.

### 2. Converting PDF to Image
The `load_pdf` method in `utils.py`:
- Opens the PDF file using PyMuPDF.
- Renders the first page as an image using the `get_pixmap` method from the page object.
- Converts the resulting RGB image into a Pillow Image object.

### 3. Comparing Images
After loading two images, the comparison is performed using the `compare_images` function in `utils.py`.
#### Steps in the comparison process:
1. **Calculating Differences**:
   - The `ImageChops.difference` function from Pillow calculates pixel-by-pixel differences between the two images.
   - The resulting difference image is converted to grayscale.
2. **Sensitivity Threshold**:
   - Using a threshold operation (lambda), differences below the specified sensitivity level are ignored.
3. **Detecting Contours**:
   - The difference image is converted to a NumPy array and passed to OpenCV.
   - The `cv2.findContours` function identifies areas of difference as contours.
4. **Marking Differences**:
   - On a copy of the first image, rectangles are drawn around detected differences using Pillow ImageDraw.

### 4. Displaying Results
The resulting image with highlighted differences is converted into a QImage format using the `pil2qimage` function (in `utils.py`).
The image is displayed in the graphical component of the application using the `GraphicsView` class.

### 5. User Interactions
The user can adjust sensitivity for the comparison using a slider (method `updateSensitivity` in the `PDFComparer` class).
Available options:
- Resetting comparison results.
- Viewing the original image.
- Printing results using the QPrinter class.

### 6. Error Handling
Each stage of the comparison is surrounded by exception handling.
In case of errors (e.g., issues loading files or converting images), the user receives a message in a dialog window.

### Example of the Process
When comparing two PDF files with differences, the application calculates the discrepancies, identifies their contours, and marks them with red rectangles. The resulting image can be saved, printed, or reset.

## Requirements

To run this application, the following software and libraries are required:

- Python 3.8 or higher
- PyQt5
- Fitz (PyMuPDF)
- Pillow
- NumPy
- OpenCV

## Installation

1. Clone this repository or download the project files:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```bash
   cd ComparePDF
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## File Structure

```
ComparePDF/
|
|-- graphics_view.py     # Custom QGraphicsView class for image display
|-- main.py              # Entry point of the application
|-- pdf_comparer.py      # Main GUI logic and application features
|-- utils.py             # Utility functions for image and PDF processing
|-- requirements.txt     # List of dependencies
|-- app.log              # Application logs (created at runtime)
```

## Usage

1. Launch the application by running `main.py`.
2. Load the first and second PDF files using the provided buttons.
3. Select the base file for comparison using the radio buttons.
4. Adjust the sensitivity slider to fine-tune the comparison.
5. Click the "Compare" button to generate the difference image.
6. View the highlighted differences and optionally print the results.

## Troubleshooting

- Ensure that the required dependencies are installed.
- Use PDF files with standard encoding. Encrypted or malformed PDFs might cause errors.
- For large files or high-resolution comparisons, ensure sufficient system memory.

## Logs

Logs are saved in `app.log` for debugging and troubleshooting purposes. They include detailed messages about application processes and errors.

## Contributing

Feel free to contribute to the project by submitting pull requests or reporting issues. Any enhancements or bug fixes are welcome.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

Special thanks to the developers of PyQt5, PyMuPDF, and other libraries that make this project possible.

This application was created almost entirely with the help of AI, specifically ChatGPT, which assisted in generating code, debugging, and documentation.
