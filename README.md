# Document to LaTeX Converter

A Streamlit web application that converts PDF, DOC, and text files to LaTeX format and generates PDFs.

# URL:

https://latexformatter.streamlit.app/

## Features

- 📄 Upload PDF, DOCX, or TXT files
- 🔄 Automatic conversion to LaTeX format
- 📝 View and download LaTeX source code
- 🎨 Customizable document title and author
- ⬇️ Download generated LaTeX files
- 📄 Compile to PDF (requires pdflatex)

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
