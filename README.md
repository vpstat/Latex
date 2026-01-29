# Document to LaTeX Converter

A Streamlit web application that converts PDF, DOC, and text files to LaTeX format and generates PDFs.

## Features

- 📄 Upload PDF, DOCX, or TXT files
- 🔄 Automatic conversion to LaTeX format
- 📝 View and download LaTeX source code
- 🎨 Customizable document title and author
- ⬇️ Download generated LaTeX files
- 📄 Compile to PDF (requires pdflatex)

## Installation

### Local Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Deployment to Streamlit Cloud

1. **Create a GitHub Repository**
   - Create a new repository on GitHub
   - Upload `app.py` and `requirements.txt`

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository, branch, and `app.py`
   - Click "Deploy"

3. **Note on PDF Compilation**
   - PDF compilation requires `pdflatex` to be installed on the server
   - Streamlit Cloud may not have LaTeX installed by default
   - Users can still download the `.tex` file and compile locally
   - For full PDF functionality on cloud deployment, you may need to use a custom Docker container with LaTeX installed

## Alternative Deployment with LaTeX Support

To enable PDF compilation on Streamlit Cloud, you can use a custom packages configuration:

1. Create a `packages.txt` file:
```
texlive-latex-base
texlive-latex-extra
texlive-fonts-recommended
```

2. Add this file to your repository alongside `app.py` and `requirements.txt`

## Usage

1. Upload a PDF, DOCX, or TXT file
2. (Optional) Configure document title and author in the sidebar
3. View the generated LaTeX source code
4. Download the LaTeX file or compile to PDF

## Supported File Formats

- **PDF** (.pdf) - Extracts text from PDF documents
- **Word Document** (.docx) - Extracts text from Word documents
- **Text File** (.txt) - Reads plain text files

## LaTeX Features

The converter automatically:
- Escapes special LaTeX characters
- Formats paragraphs
- Detects potential headings
- Creates a properly structured LaTeX document

## Local PDF Compilation

If PDF compilation doesn't work in the cloud, download the `.tex` file and compile locally:

```bash
pdflatex document.tex
```

This requires a LaTeX distribution:
- **Windows**: MiKTeX or TeX Live
- **macOS**: MacTeX
- **Linux**: TeX Live

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
