import PyPDF2


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text


pdf_text = extract_text_from_pdf("Docs/Code_the_Classics-book.pdf")
print(pdf_text[:500])

