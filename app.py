import streamlit as st
import PyPDF2
import docx
import io
import re
import subprocess
import tempfile
import os
from pathlib import Path

def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    doc = docx.Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_txt(file):
    """Extract text from TXT file"""
    return file.read().decode('utf-8')

def escape_latex_special_chars(text):
    """Escape special LaTeX characters"""
    special_chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
    }
    for char, replacement in special_chars.items():
        text = text.replace(char, replacement)
    return text

def text_to_latex(text, title="Converted Document", author=""):
    """Convert plain text to LaTeX format with basic formatting"""
    
    # Escape special characters
    escaped_text = escape_latex_special_chars(text)
    
    # Split into paragraphs
    paragraphs = escaped_text.split('\n\n')
    
    # Basic formatting improvements
    formatted_paragraphs = []
    for para in paragraphs:
        para = para.strip()
        if para:
            # Check if it looks like a heading (short line, possibly all caps or title case)
            if len(para) < 60 and para.isupper():
                formatted_paragraphs.append(f"\\section{{{para.title()}}}")
            elif len(para) < 60 and para[0].isupper() and '\n' not in para:
                formatted_paragraphs.append(f"\\subsection{{{para}}}")
            else:
                # Regular paragraph
                formatted_paragraphs.append(para)
    
    # Create LaTeX document
    latex_content = f"""\\documentclass[12pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{geometry}}
\\usepackage{{parskip}}
\\geometry{{a4paper, margin=1in}}

\\title{{{escape_latex_special_chars(title)}}}
\\author{{{escape_latex_special_chars(author)}}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

{chr(10).join(formatted_paragraphs)}

\\end{{document}}
"""
    
    return latex_content

def compile_latex_to_pdf(latex_content):
    """Compile LaTeX content to PDF using pdflatex"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write LaTeX content to file
        tex_file = os.path.join(tmpdir, "document.tex")
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        # Compile with pdflatex
        try:
            # Run pdflatex twice for proper references
            for _ in range(2):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', '-output-directory', tmpdir, tex_file],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            
            # Read the generated PDF
            pdf_file = os.path.join(tmpdir, "document.pdf")
            if os.path.exists(pdf_file):
                with open(pdf_file, 'rb') as f:
                    pdf_content = f.read()
                return pdf_content, None
            else:
                return None, "PDF compilation failed. Check LaTeX syntax."
        
        except subprocess.TimeoutExpired:
            return None, "LaTeX compilation timed out."
        except FileNotFoundError:
            return None, "pdflatex not found. Please install TeX Live or MiKTeX."
        except Exception as e:
            return None, f"Error during compilation: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Document to LaTeX Converter", page_icon="📄", layout="wide")

st.title("📄 Document to LaTeX Converter")
st.markdown("Upload PDF, DOC, or TXT files to convert them to LaTeX format and generate a PDF.")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    doc_title = st.text_input("Document Title", "Converted Document")
    doc_author = st.text_input("Author Name", "")
    st.markdown("---")
    st.markdown("### Supported Formats")
    st.markdown("- PDF (.pdf)")
    st.markdown("- Word Document (.docx)")
    st.markdown("- Text File (.txt)")

# File upload
uploaded_file = st.file_uploader(
    "Choose a file", 
    type=['pdf', 'docx', 'txt'],
    help="Upload a PDF, DOCX, or TXT file to convert to LaTeX"
)

if uploaded_file is not None:
    # Display file info
    st.success(f"✅ File uploaded: {uploaded_file.name}")
    
    # Extract text based on file type
    with st.spinner("Extracting text from file..."):
        try:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'pdf':
                extracted_text = extract_text_from_pdf(uploaded_file)
            elif file_extension == 'docx':
                extracted_text = extract_text_from_docx(uploaded_file)
            elif file_extension == 'txt':
                extracted_text = extract_text_from_txt(uploaded_file)
            else:
                st.error("Unsupported file format!")
                st.stop()
            
            if not extracted_text.strip():
                st.warning("⚠️ No text could be extracted from the file.")
                st.stop()
            
            st.success(f"✅ Extracted {len(extracted_text)} characters")
            
        except Exception as e:
            st.error(f"Error extracting text: {str(e)}")
            st.stop()
    
    # Convert to LaTeX
    with st.spinner("Converting to LaTeX format..."):
        latex_content = text_to_latex(extracted_text, title=doc_title, author=doc_author)
        st.success("✅ Converted to LaTeX format")
    
    # Display LaTeX content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 LaTeX Source")
        st.code(latex_content, language='latex')
        
        # Download LaTeX file
        st.download_button(
            label="⬇️ Download LaTeX (.tex)",
            data=latex_content,
            file_name=f"{doc_title.replace(' ', '_')}.tex",
            mime="text/plain"
        )
    
    with col2:
        st.subheader("📄 Generated PDF")
        
        # Compile to PDF
        if st.button("🔄 Compile to PDF", type="primary"):
            with st.spinner("Compiling LaTeX to PDF..."):
                pdf_content, error = compile_latex_to_pdf(latex_content)
                
                if pdf_content:
                    st.success("✅ PDF generated successfully!")
                    
                    # Display PDF
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=pdf_content,
                        file_name=f"{doc_title.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                    
                    # Show PDF preview
                    st.markdown("### PDF Preview")
                    st.write("Download the PDF to view it.")
                    
                else:
                    st.error(f"❌ {error}")
                    st.info("💡 You can still download the LaTeX source and compile it locally.")

else:
    st.info("👆 Please upload a file to get started")
    
    # Show example
    with st.expander("ℹ️ How it works"):
        st.markdown("""
        1. **Upload** a PDF, DOCX, or TXT file
        2. **Configure** the document title and author (optional)
        3. **Review** the generated LaTeX source code
        4. **Download** the LaTeX file or compile it to PDF
        
        ### Requirements for PDF Compilation
        This app requires `pdflatex` to be installed on the server. If compilation fails, 
        you can download the `.tex` file and compile it locally using:
        
        ```bash
        pdflatex document.tex
        ```
        """)
