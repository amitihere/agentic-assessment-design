from fpdf import FPDF
import io

def create_pdf_report(report_text: str) -> bytes:
    \"\"\"
    Converts a Markdown-like report text into a PDF and returns its bytes.
    Uses 'fpdf2'.
    \"\"\"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)
    
    # Title
    pdf.cell(0, 10, txt="Assessment Quality Report", ln=True, align="C")
    pdf.ln(10)
    
    # Clean up simple markdown features for FPDF (remove #'s and convert lists partially)
    lines = report_text.split('\\n')
    
    for line in lines:
        if line.startswith('# '):
            pdf.set_font("Arial", style="B", size=16)
            pdf.multi_cell(0, 10, txt=line.replace('# ', '').strip())
        elif line.startswith('## '):
            pdf.ln(4)
            pdf.set_font("Arial", style="B", size=12)
            pdf.multi_cell(0, 8, txt=line.replace('## ', '').strip())
        elif line.startswith('- '):
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 6, txt="    \u2022 " + line.replace('- ', '').strip())
        elif line.startswith('*') and line.endswith('*'):
            pdf.set_font("Arial", style="I", size=10)
            pdf.multi_cell(0, 6, txt=line.replace('*', '').strip())
        else:
            pdf.set_font("Arial", size=11)
            if line.strip():
                pdf.multi_cell(0, 6, txt=line.strip())
            else:
                pdf.ln(2)
                
    return pdf.output(dest="S")
