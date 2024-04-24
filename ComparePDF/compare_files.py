import fitz  # PyMuPDF
from PIL import Image, ImageChops

def pdf_to_image(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)  # załadowanie pierwszej strony
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    doc.close()
    return img

def compare_images(img1, img2):
    diff = ImageChops.difference(img1, img2)
    for x in range(diff.width):
        for y in range(diff.height):
            if diff.getpixel((x, y)) != (0, 0, 0):
                diff.putpixel((x, y), (255, 0, 0))  # zaznaczenie różnic na czerwono
    return diff

def comparePDFs(path1, path2):
    img1 = pdf_to_image(path1)
    img2 = pdf_to_image(path2)
    result = compare_images(img1, img2)
    result.show()  # wyświetlenie wyniku