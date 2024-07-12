import PyPDF2
from flask import Flask, request, redirect, url_for, render_template, send_file
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MERGED_FOLDER'] = 'merged/'

# Ensure the upload and merged directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MERGED_FOLDER'], exist_ok=True)

def merge_pdfs(pdf_list, output_filename):
    # Create a PdfMerger object
    pdf_merger = PyPDF2.PdfMerger()

    # Iterate through the list of PDF filenames
    for pdf in pdf_list:
        try:
            # Append each PDF file to the merger object
            pdf_merger.append(pdf)
            print(f"Added {pdf} to merger")
        except Exception as e:
            print(f"Error reading {pdf}: {e}")
            continue

    output_path = os.path.join(app.config['MERGED_FOLDER'], output_filename)
    try:
        # Write the collected pages to the output PDF file
        with open(output_path, 'wb') as output_pdf:
            pdf_merger.write(output_pdf)
        print(f"PDF files {pdf_list} merged into {output_path}")
    except Exception as e:
        print(f"Error writing {output_path}: {e}")

    return output_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('pdfs')
        pdf_list = []
        for file in uploaded_files:
            if file.filename.endswith('.pdf'):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                print(f"Saved {file_path}")
                pdf_list.append(file_path)
        print(f"Uploaded files: {pdf_list}")
        if pdf_list:
            output_filename = 'merged.pdf'
            merged_pdf_path = merge_pdfs(pdf_list, output_filename)
            return redirect(url_for('result', filename=output_filename))
    return render_template('index.html')

@app.route('/result')
def result():
    filename = request.args.get('filename')
    return render_template('result.html', filename=filename)

@app.route('/downloads/<filename>')
def download_file(filename):
    merged_file_path = os.path.join(app.config['MERGED_FOLDER'], filename)
    if not os.path.exists(merged_file_path):
        return f"Error: File {filename} not found at {merged_file_path}", 404
    return send_file(merged_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

