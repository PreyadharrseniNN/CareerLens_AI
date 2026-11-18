import PyPDF2
import docx
import io

def extract_text_from_pdf(file_stream):
    """
    Extracts text from a PDF file stream.
    """
    text = ""
    try:
        if hasattr(file_stream, 'seek'):
            file_stream.seek(0)
        pdf_reader = PyPDF2.PdfReader(file_stream)
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(file_stream):
    """
    Extracts text from a DOCX file stream including paragraphs and tables.
    """
    text = ""
    try:
        if hasattr(file_stream, 'seek'):
            file_stream.seek(0)
        doc = docx.Document(file_stream)
        for para in doc.paragraphs:
            text += para.text + "\n"
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text += cell.text + " "
                text += "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text

def extract_text(file_stream, filename):
    """
    Determines file type and extracts text accordingly.
    Wraps bytes into a seekable BytesIO stream if needed.
    """
    if hasattr(file_stream, 'read'):
        raw_bytes = file_stream.read()
        stream = io.BytesIO(raw_bytes)
    else:
        stream = file_stream

    if filename.lower().endswith('.pdf'):
        return extract_text_from_pdf(stream)
    elif filename.lower().endswith('.docx'):
        return extract_text_from_docx(stream)
    else:
        return ""
