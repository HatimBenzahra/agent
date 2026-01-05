#!/usr/bin/env python3
"""
Simple Improved PDF Generator
Creates a PDF with enhanced formatting without complex characters
"""

from fpdf import FPDF
from datetime import datetime

def create_simple_enhanced_pdf():
    """Create a PDF with improved formatting"""
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Page 1: Title Page
    pdf.add_page()
    
    # Title
    pdf.set_font('helvetica', 'B', 24)
    pdf.cell(0, 30, "", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 20, "ENHANCED PDF DOCUMENT", align='C', new_x="LMARGIN", new_y="NEXT")
    
    # Subtitle
    pdf.set_font('helvetica', 'I', 16)
    pdf.cell(0, 15, "Improved Formatting Example", align='C', new_x="LMARGIN", new_y="NEXT")
    
    # Date
    current_date = datetime.now().strftime("%B %d, %Y")
    pdf.set_font('helvetica', '', 14)
    pdf.cell(0, 40, "", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Generated: {current_date}", align='C', new_x="LMARGIN", new_y="NEXT")
    
    # Version
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 60, "", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, "Version 3.0 - Enhanced Generator", align='C', new_x="LMARGIN", new_y="NEXT")
    
    # Page 2: Introduction
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 20)
    pdf.cell(0, 15, "1. Introduction", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    pdf.set_font('helvetica', '', 12)
    intro_text = """
This PDF demonstrates improved document generation techniques with better formatting,
structure, and professional appearance. The enhancements include:

- Better page layout and spacing
- Professional headers and sections
- Structured content organization
- Clean typography and formatting
- Automatic page management
- Consistent styling throughout
    """
    pdf.multi_cell(0, 8, intro_text)
    pdf.ln(10)
    
    # Page 3: Features
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 20)
    pdf.cell(0, 15, "2. Key Features", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    features = [
        "Multi-page document support",
        "Automatic page breaks",
        "Consistent formatting",
        "Clean typography",
        "Easy customization",
        "Cross-platform compatibility",
        "Memory efficient",
        "Fast generation"
    ]
    
    pdf.set_font('helvetica', '', 12)
    for feature in features:
        pdf.cell(10, 8, "-", new_x="RIGHT", new_y="TOP")
        pdf.cell(0, 8, f" {feature}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
    
    pdf.ln(10)
    
    # Page 4: Performance Data
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 20)
    pdf.cell(0, 15, "3. Performance Metrics", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Table header
    pdf.set_font('helvetica', 'B', 12)
    col_width = pdf.w / 5
    headers = ["Quarter", "Revenue", "Growth", "Profit", "Users"]
    
    for header in headers:
        pdf.cell(col_width, 10, header, border=1, align='C')
    pdf.ln()
    
    # Table data
    pdf.set_font('helvetica', '', 11)
    data = [
        ["Q1 2024", "$2.5M", "+12.5%", "$450K", "1.2M"],
        ["Q2 2024", "$2.8M", "+15.2%", "$520K", "1.4M"],
        ["Q3 2024", "$3.1M", "+18.4%", "$590K", "1.6M"],
        ["Q4 2024", "$3.5M", "+21.7%", "$670K", "1.9M"],
        ["Total", "$11.9M", "+16.9%", "$2.23M", "6.1M"]
    ]
    
    for row in data:
        for item in row:
            pdf.cell(col_width, 10, item, border=1, align='C')
        pdf.ln()
    
    pdf.ln(15)
    
    # Page 5: Summary
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 20)
    pdf.cell(0, 15, "4. Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    pdf.set_font('helvetica', '', 12)
    summary_text = """
This improved PDF generator provides professional document creation with:
    
1. Structured content organization
2. Professional formatting throughout
3. Easy customization options
4. Automatic page management
5. Clean typography

The system generates documents suitable for business reports, 
technical documentation, academic papers, and professional presentations.
    
Key advantages include:
- Fast generation time
- Consistent output quality
- Easy to modify and extend
- No special software required
- Compatible with all PDF viewers
    """
    pdf.multi_cell(0, 8, summary_text)
    
    # Add page numbers
    total_pages = pdf.page_no()
    for i in range(1, total_pages + 1):
        pdf.page = i
        pdf.set_y(-15)
        pdf.set_font('helvetica', 'I', 10)
        pdf.cell(0, 10, f"Page {i} of {total_pages}", align='C')
    
    # Save PDF
    filename = "simple_enhanced_report.pdf"
    pdf.output(filename)
    
    return filename, total_pages

if __name__ == "__main__":
    print("Generating Simple Enhanced PDF...")
    print("=" * 50)
    
    try:
        filename, pages = create_simple_enhanced_pdf()
        print(f"✓ Successfully created: {filename}")
        print(f"✓ Pages generated: {pages}")
        print(f"✓ Formatting: Professional with tables and lists")
        
        # Get file info
        import os
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✓ File size: {size:,} bytes ({size/1024:.1f} KB)")
        
        print("\n✅ PDF generation completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nCreating minimal fallback...")
        
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('helvetica', 'B', 16)
            pdf.cell(0, 10, 'Minimal PDF', new_x="LMARGIN", new_y="NEXT", align='C')
            pdf.ln(10)
            pdf.set_font('helvetica', '', 12)
            pdf.multi_cell(0, 10, 'This is a minimal fallback PDF.')
            pdf.output('minimal_fallback.pdf')
            print("✓ Created minimal fallback: minimal_fallback.pdf")
        except:
            print("❌ Could not create any PDF")