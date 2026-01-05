#!/usr/bin/env python3
"""
Simple PDF Generator
Creates a PDF with sample content
"""

from fpdf import FPDF
from datetime import datetime

def create_sample_pdf():
    """Create a PDF document with sample content"""
    
    # Create PDF object
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Add a page
    pdf.add_page()
    
    # Add title
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 15, 'PDF Document Example', ln=True, align='C')
    pdf.ln(10)
    
    # Add subtitle and date
    pdf.set_font('Helvetica', 'I', 14)
    pdf.cell(0, 10, 'Generated with Python fpdf2 Library', ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 12)
    current_date = datetime.now().strftime("%B %d, %Y at %H:%M")
    pdf.cell(0, 10, f'Created: {current_date}', ln=True, align='C')
    pdf.ln(20)
    
    # Introduction section
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'Introduction', ln=True)
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 12)
    intro_text = (
        "This document demonstrates how to create PDF files using Python. "
        "PDF generation is useful for creating reports, invoices, documents, "
        "and any other printable content programmatically.\n\n"
        "Python offers several libraries for working with PDFs, including:\n"
        "• fpdf2 - Simple PDF generation\n"
        "• ReportLab - Advanced PDF generation\n"
        "• PyPDF2 - PDF manipulation and merging\n"
        "• pdfkit - HTML to PDF conversion"
    )
    pdf.multi_cell(0, 8, intro_text)
    pdf.ln(15)
    
    # Features section
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'Key Features', ln=True)
    pdf.ln(5)
    
    features = [
        "Automatic text formatting and wrapping",
        "Support for multiple fonts and styles",
        "Image insertion capabilities",
        "Table creation with borders",
        "Page numbering and headers/footers",
        "Multi-page document support",
        "UTF-8 character support",
        "PDF/A compliance options"
    ]
    
    pdf.set_font('Helvetica', '', 12)
    for feature in features:
        pdf.cell(10, 8, '•', ln=0)
        pdf.cell(0, 8, feature, ln=True)
        pdf.ln(2)
    
    pdf.ln(15)
    
    # Sample data section
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'Sample Data', ln=True)
    pdf.ln(5)
    
    # Create a table
    pdf.set_font('Helvetica', 'B', 12)
    
    # Table headers
    col_width = pdf.w / 4.5
    headers = ['Product', 'Category', 'Price', 'In Stock']
    for header in headers:
        pdf.cell(col_width, 10, header, border=1, align='C')
    pdf.ln()
    
    # Table data
    pdf.set_font('Helvetica', '', 12)
    data = [
        ['Laptop', 'Electronics', '$899.99', 'Yes'],
        ['Notebook', 'Office', '$12.50', 'Yes'],
        ['Coffee Mug', 'Home', '$8.99', 'No'],
        ['Headphones', 'Electronics', '$129.99', 'Yes'],
        ['Desk Chair', 'Furniture', '$249.99', 'Yes'],
        ['Smartphone', 'Electronics', '$699.99', 'Yes']
    ]
    
    for row in data:
        for item in row:
            pdf.cell(col_width, 10, item, border=1, align='C')
        pdf.ln()
    
    pdf.ln(20)
    
    # Conclusion section
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'Conclusion', ln=True)
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 12)
    conclusion_text = (
        "Python's PDF generation capabilities make it an excellent choice for "
        "automating document creation tasks. Whether you need to generate "
        "reports, invoices, certificates, or any other type of document, "
        "Python libraries provide the tools you need.\n\n"
        "This simple example shows just a fraction of what's possible. "
        "You can extend this to include images, charts, different fonts, "
        "complex layouts, and much more."
    )
    pdf.multi_cell(0, 8, conclusion_text)
    pdf.ln(15)
    
    # Add page number
    pdf.set_font('Helvetica', 'I', 10)
    pdf.cell(0, 10, 'Page 1 of 1', align='C')
    
    # Save the PDF
    filename = 'sample_document.pdf'
    pdf.output(filename)
    
    return filename

if __name__ == "__main__":
    print("Generating PDF document...")
    try:
        filename = create_sample_pdf()
        print(f"PDF successfully created: {filename}")
        print("The PDF contains:")
        print("- Title page with date")
        print("- Introduction section")
        print("- Key features list")
        print("- Sample data table")
        print("- Conclusion section")
    except Exception as e:
        print(f"Error creating PDF: {e}")
        print("Trying alternative approach...")
        
        # Try a simpler approach if the main one fails
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Helvetica', 'B', 16)
            pdf.cell(0, 10, 'Simple PDF Created', ln=True, align='C')
            pdf.ln(10)
            pdf.set_font('Helvetica', '', 12)
            pdf.multi_cell(0, 10, 'This is a minimal PDF created as a fallback.')
            pdf.output('simple_fallback.pdf')
            print("Created: simple_fallback.pdf")
        except Exception as e2:
            print(f"Even fallback failed: {e2}")