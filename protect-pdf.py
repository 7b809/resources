import dropbox
import os
import io
from PyPDF2 import PdfReader, PdfWriter

# Retrieve Dropbox access token from environment variable
ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')
APP_FOLDER = '/Apps/getdata101/getdata101'
FILE_NAME = 'm2.pdf'
PASSWORD = 'merged'

# Initialize Dropbox client
dbx = dropbox.Dropbox(ACCESS_TOKEN)

def download_file_from_dropbox(path):
    """Download a file from Dropbox and return it as a bytes-like object."""
    try:
        metadata, res = dbx.files_download(path)
        return io.BytesIO(res.content)
    except dropbox.exceptions.ApiError as e:
        print(f"Error downloading file: {e}")
        raise

def upload_file_to_dropbox(file_stream, path):
    """Upload a file to Dropbox."""
    try:
        dbx.files_upload(file_stream.read(), path, mode=dropbox.files.WriteMode('overwrite'))
    except dropbox.exceptions.ApiError as e:
        print(f"Error uploading file: {e}")
        raise

def add_password_to_pdf(input_pdf_stream, output_pdf_stream, password):
    """Add password protection to the PDF."""
    pdf_reader = PdfReader(input_pdf_stream)
    pdf_writer = PdfWriter()

    for page_num in range(len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page_num])
        print(f'{page_num} completed {len(pdf_reader.pages)}')

    pdf_writer.encrypt(password)
    print("Password writing completed")

    pdf_writer.write(output_pdf_stream)

def main():
    # Construct the file path
    file_path = f"{APP_FOLDER}/{FILE_NAME}"

    # Download the PDF from Dropbox
    pdf_stream = download_file_from_dropbox(file_path)

    # Create a bytes buffer for the protected PDF
    protected_pdf_stream = io.BytesIO()

    # Add password to the PDF
    add_password_to_pdf(pdf_stream, protected_pdf_stream, PASSWORD)

    # Prepare the output file path
    protected_file_name = f"{FILE_NAME.replace('.pdf', '_protected.pdf')}"
    protected_file_path = f"{APP_FOLDER}/{protected_file_name}"

    # Upload the protected PDF back to Dropbox
    protected_pdf_stream.seek(0)
    upload_file_to_dropbox(protected_pdf_stream, protected_file_path)

    print(f"Password-protected PDF saved as '{protected_file_path}'")

if __name__ == "__main__":
    main()
