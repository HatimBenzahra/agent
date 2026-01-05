#!/usr/bin/env python3
"""
Create a simple PDF document
"""

from fpdf import FPDF
from datetime import datetime

def create_pdf():
    """Create a PDF document"""
    
    # Create PDF object
    pdf = FPDF()
    
    # Add a page
    pdf.add_page()
    
    # Set font
    pdf.set_font("Arial", size=16)
    
    # Add title
    pdf.cell(200, 10, txt="PDF Document Generated with Python", ln=1, align='C')
    
    # Add subtitle
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Created using fpdf2 library", ln=1, align='C')
    
    # Add date
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(200, 10, txt=f"Generated on: {current_time}", ln=1, align='C')
    
    # Add some content
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    
    # Section 1
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Section 1: Introduction", ln=1)
    
    pdf.set_font("Arial", size=12)
    intro_text = """This PDF was created programmatically using Python. 
Python is a powerful programming language that can be used for many tasks, 
including document generation, data analysis, web development, and more.
"""
    pdf.multi_cell(0, 10, intro_text)
    
    # Section 2
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Section 2: Key Points", ln=1)
    
    pdf.set_font("Arial", size=12)
    points = [
        "Easy to create PDFs programmatically",
        "Supports text formatting and styling",
        "Can include tables and images",
        "Multi-page document support",
        "UTF-8 character support"
    ]
    
    for point in points:
        pdf.cell(0, 10, f"• {point}", ln=1)
    
    # Section 3 - Sample table
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Section 3: Sample Data", ln=1)
    
    # Create a simple table
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(50, 10, "Item", border=1)
    pdf.cell(40, 10, "Quantity", border=1)
    pdf.cell(40, 10, "Price", border=1)
    pdf.cell(40, 10, "Total", border=1)
    pdf.ln()
    
    data = [
        ["Laptop", "1", "$899.99", "$899.99"],
        ["Mouse", "2", "$24.99", "$49.98"],
        ["Keyboard", "1", "$79.99", "$79.99"],
        ["Monitor", "1", "$249.99", "$249.99"]
    ]
    
    pdf.set_font("Arial", size=12)
    for row in data:
        pdf.cell(50, 10, row[0], border=1)
        pdf.cell(40, 10, row[1], border=1)
        pdf.cell(40, 10, row[2], border=1)
        pdf.cell(40, 10, row[3], border=1)
        pdf.ln()
    
    # Footer
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt="End of document - Page 1", ln=1, align='C')
    
    # Save PDF
    filename = "final_generated_pdf.pdf"
    pdf.output(filename)
    
    return filename

if __name__ == "__main__":
    print("Creating PDF document...")
    try:
        filename = create_pdf()
        print(f"✓ PDF successfully created: {filename}")
        
        # Get file size
        import os
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"File size: {size} bytes")
            print("PDF generation completed successfully!")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure fpdf2 is installed: pip install fpdf2")