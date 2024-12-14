# PDF Comparator v2.0

PDF Comparator v2.0 is a PyQt5-based desktop application designed to visually compare two PDF files. It highlights differences between the PDFs, allowing users to quickly identify changes or discrepancies. The application also includes additional features like sensitivity adjustment, file preview, and printing options.

- This application was created almost entirely with the help of AI, specifically ChatGPT, which assisted in generating code, debugging, and documentation.

## Features

- **PDF Comparison**: Compare two PDF files and highlight differences using visual markers.
- **Custom Sensitivity**: Adjust sensitivity to fine-tune the detection of differences.
- **Drag-and-Zoom**: Interactive view of the compared images with mouse drag and zoom.
- **PDF Preview**: Preview the loaded PDF files before comparison.
- **Result Printing**: Print the comparison result directly from the application.
- **Error Handling**: Robust error handling with descriptive messages for user convenience.

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
