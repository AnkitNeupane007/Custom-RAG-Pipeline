import fitz

# read PDF and extract text
def extract_text_from_pdf(file_bytes: bytes) -> list[str]:
    pages = []
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            pages.append(page.get_text())
    return pages

# * prints all
# * print(extract_text_from_pdf("./sample.pdf"))