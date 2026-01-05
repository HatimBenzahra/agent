#!/usr/bin/env python3
"""
Simple script to create a PDF without user input
"""

from fpdf import FPDF
from datetime import datetime

def create_pdf():
    """Create a PDF document with some content"""
    
    # Create PDF object
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Add a page
    pdf.add_page()
    
    # Set font for title
    pdf.set_font('Arial', 'B', 16)
    
    # Add title
    pdf.cell(0, 10, 'PDF Document Generated with Python', ln=True, align='C')
    pdf.ln(10)
    
    # Add date
    pdf.set_font('Arial', '', 12)
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 10, f'Generated on: {current_date}', ln=True, align='C')
    pdf.ln(20)
    
    # Add content sections
    sections = [
        ("Introduction", 
         "This is a PDF document generated using Python and the fpdf2 library. "
         "It demonstrates how to create professional-looking PDFs programmatically."),
        
        ("Why Generate PDFs with Python?",
         "Python offers several libraries for PDF generation, including fpdf2, ReportLab, "
         "and PyPDF2. These libraries allow you to create, modify, and manipulate PDF documents "
         "automatically, which is useful for generating reports, invoices, documents, and more."),
        
        ("Common Use Cases",
         "1. Automated report generation\n"
         "2. Invoice creation\n"
         "3. Document templates\n"
         "4. Data visualization reports\n"
         "5. Batch document processing"),
        
        ("Sample Content",
         "Here is some sample text to demonstrate text formatting in PDFs. "
         "You can add paragraphs, change fonts, add images, create tables, "
         "and include various types of content in your PDF documents."),
        
        ("Conclusion",
         "PDF generation with Python is a powerful tool for automating document creation. "
         "With just a few lines of code, you can create professional documents that "
         "would otherwise require manual effort.")
    ]
    
    # Add each section
    for title, content in sections:
        # Section title
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, title, ln=True)
        pdf.ln(5)
        
        # Section content
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 8, content)
        pdf.ln(10)
    
    # Add a simple table
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Sample Data Table', ln=True)
    pdf.ln(5)
    
    # Table headers
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'Item', border=1)
    pdf.cell(40, 10, 'Quantity', border=1)
    pdf.cell(40, 10, 'Price', border=1)
    pdf.cell(40, 10, 'Total', border=1)
    pdf.ln()
    
    # Table data
    pdf.set_font('Arial', '', 12)
    data = [
        ('Product A', '2', '$10.00', '$20.00'),
        ('Product B', '3', '$15.00', '$45.00'),
        ('Product C', '1', '$25.00', '$25.00'),
        ('Product D', '5', '$8.00', '$40.00')
    ]
    
    for item, qty, price, total in data:
        pdf.cell(40, 10, item, border=1)
        pdf.cell(40, 10, qty, border=1)
        pdf.cell(40, 10, price, border=1)
        pdf.cell(40, 10, total, border=1)
        pdf.ln()
    
    pdf.ln(20)
    
    # Add footer
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, 'Page 1', align='C')
    
    # Save PDF file
    output_file = 'generated_document.pdf'
    pdf.output(output_file)
    
    print(f"PDF created successfully: {output_file}")
    return output_file

if __name__ == "__main__":
    try:
        print("Creating PDF document...")
        output_file = create_pdf()
        print(f"Done! PDF file: {output_file}")
    except Exception as e:
        print(f"Error: {e}")