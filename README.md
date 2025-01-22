# ComparePDF  v3.0

### Screenshot:
![Main application interface](images/Application window.png "Main interface") 

ComparePDF (PDF Comparator)  v3.0 is a PyQt5-based desktop application designed to visually compare two PDF files. It highlights differences between the documents, enabling users to quickly identify changes. In this updated version, the interface has been modernized using stylesheets (QSS) and a dedicated settings file for color palettes, as well as preparations for easily adding icons to buttons.
## Features

- **PDF Comparison**: Compare two PDF files and visually highlight their differences.
- **Adjustable Sensitivity**: Fine-tune the sensitivity to control which differences are highlighted
- **Interactive View**: IPan and zoom the comparison results using your mouse.
- **PDF Preview**: Preview the loaded PDF files before comparison.
- **Result Printing**: Print the comparison result directly from the application.
- **Error Handling**: Robust error handling with descriptive messages for user convenience.
- **Test Mode**: Save intermediate results and debug data during the comparison process.
- **Modern Look**: Version 3.0 introduces a contemporary, dark-themed UI with QSS and a flexible structure for adding icons to buttons.

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
|-- main.py               # Entry point of the application, applies palette/QSS and launches the main window
|-- main_window.py        # Main application window (UI layout and setup)
|-- preview_panel.py      # PDF preview panel with radio buttons for base selection
|-- control_panel.py      # Control panel with Compare, Reset, Clear, Print buttons and sensitivity slider
|-- graphics_view.py      # Custom QGraphicsView for image display and interaction
|-- controllers/
|   `-- pdf_controller.py # Application logic: loading PDFs, comparing, resetting, handling errors
|-- services/
|   `-- pdf_service.py    # PDF operations: loading files, converting to images, performing comparisons
|-- models/
|   `-- pdf_document.py   # Data models for PDF documents and comparison results
|-- utils/
|   `-- image_utils.py    # Image processing utilities (difference detection, resizing)
|-- config/
|   `-- settings.py       # Application configuration (colors, default sensitivity, etc.)
|-- settings.py           # External file for style/QSS and palette definitions
|-- icons/                # Folder for icons (optional)
`-- requirements.txt      # List of dependencies
```

## Usage

1. Launch the application by running `main.py`.
2. Load the first and second PDF files using the provided buttons.
3. Select the base file for comparison using the radio buttons.
4. Adjust the sensitivity slider to fine-tune the comparison.
5. Click the "Compare" button to generate the difference image.
6. View the highlighted differences and optionally print the results.

## Changes in Version 3.0
* Modern Interface:

  Uses the Fusion style and a QSS stylesheet defined in settings.py to create a cohesive, dark, and modern UI.
* Separation of Style and Logic:

  The color palette and QSS stylesheet are placed in a separate file (settings.py), making it easier to modify the look without altering core logic.
* Icon Support:

   The structure now supports adding icons to buttons (e.g., in control_panel.py via QIcon and the icons/ folder), improving the visual intuitiveness of the UI.
* Expanded Dimensions:

  The UI elements (PDF areas, buttons, sliders) have been enlarged and adjusted to be more readable and modern-looking.

## Test Mode (`testing_mode`)

The application provides a test mode to save intermediate images and data during the comparison process. This mode is useful for debugging and analyzing how the program processes the PDF files.

### Generated Files in Test Mode

#### 1. `preview_1_test.png` and `preview_2_test.png`

- **Description**: These are previews of the loaded PDF files, converted into images.
- **Purpose**: Verify that the PDFs were correctly loaded and converted into images.
- **Example**:

   ![Preview 1](images/preview_1_test.png)
   ![Preview 2](images/preview_2_test.png)

#### 2. `image_difference_grayscale_test.png`

- **Description**: A grayscale image showing the raw pixel differences between the two PDFs.
- **Purpose**: Darker pixels indicate smaller differences, while brighter pixels indicate larger differences.
- **Example**:

   ![Grayscale Difference](images/image_difference_grayscale_test.png)

#### 3. `image_difference_thresholded_test.png`

- **Description**: A binary image highlighting significant differences. White pixels represent differences above the sensitivity threshold, while black pixels represent no difference.
- **Purpose**: Focus on critical differences after applying sensitivity thresholding.
- **Example**:

   ![Thresholded Difference](images/image_difference_thresholded_test.png)

#### 4. `difference_matrix_test.txt`

- **Description**: A textual representation of the binary difference image as a matrix. Each number represents a pixel value (0 for no difference, 255 for significant difference).
- **Purpose**: Useful for further data analysis or debugging.
- **Example**: Contents of the file:
   ```
   0 0 0 255 255
   0 0 0 0 255
   255 255 0 0 0
   ```

#### 5. `result_image_test.png`

- **Description**: The final result image with rectangles drawn around the detected differences.
- **Purpose**: Highlight significant differences directly on the base image.
- **Example**:

   ![Result Image](images/result_image_test.png)

#### 6. `original_image_test.png`

- **Description**: A copy of the base PDF image before any differences are marked.
- **Purpose**: Serves as a reference for the original state of the base image.
- **Example**:

   ![Original Image](images/original_image_test.png)

### How to Enable Test Mode

1. Open the `pdf_comparer.py` file.
2. In the `PDFComparer` class, set the `self.testing_mode` attribute to `True`:
   ```python
   self.testing_mode = True  # Enable test mode
   ```
3. Run the application as usual. Test files will be saved in the current working directory.

## Troubleshooting

- Ensure that the required dependencies are installed.
- Use PDF files with standard encoding. Encrypted or malformed PDFs might cause errors.
- For large files or high-resolution comparisons, ensure sufficient system memory.

## Logs

Logs are saved in `app.log` for debugging and troubleshooting purposes. They include detailed messages about application processes and errors.

## Contributing

Feel free to contribute to the project by submitting pull requests or reporting issues. Any enhancements or bug fixes are welcome.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
 

## Acknowledgments

Special thanks to the developers of PyQt5, PyMuPDF, and other libraries that make this project possible.

Additionally, this application was created with significant assistance from AI, specifically OpenAI's ChatGPT, to streamline the development process.