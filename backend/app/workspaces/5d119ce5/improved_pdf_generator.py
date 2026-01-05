#!/usr/bin/env python3
"""
Improved PDF Generator - Enhanced version with better formatting
Creates a multi-page PDF with improved layout and content
"""

from fpdf import FPDF
from datetime import datetime

class ImprovedPDFGenerator:
    def __init__(self, title="Improved PDF Document"):
        """Initialize the PDF generator"""
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.set_margins(left=15, top=15, right=15)
        self.title = title
        
    def add_title_page(self):
        """Add a formatted title page"""
        self.pdf.add_page()
        
        # Title
        self.pdf.set_font('helvetica', 'B', 24)
        self.pdf.cell(0, 30, "", new_x="LMARGIN", new_y="NEXT")  # Spacing
        self.pdf.cell(0, 20, "IMPROVED PDF REPORT", align='C', new_x="LMARGIN", new_y="NEXT")
        
        # Subtitle
        self.pdf.set_font('helvetica', 'I', 16)
        self.pdf.cell(0, 15, "Advanced Document Generation", align='C', new_x="LMARGIN", new_y="NEXT")
        
        # Date
        current_date = datetime.now().strftime("%B %d, %Y")
        self.pdf.set_font('helvetica', '', 14)
        self.pdf.cell(0, 40, "", new_x="LMARGIN", new_y="NEXT")  # Spacing
        self.pdf.cell(0, 10, f"Generated on: {current_date}", align='C', new_x="LMARGIN", new_y="NEXT")
        
        # Version
        self.pdf.set_font('helvetica', '', 10)
        self.pdf.cell(0, 60, "", new_x="LMARGIN", new_y="NEXT")  # Spacing
        self.pdf.cell(0, 10, "Improved PDF Generator v2.0", align='C', new_x="LMARGIN", new_y="NEXT")
        
    def add_content_section(self, title, content, level=1):
        """Add a content section with proper formatting"""
        # Add new page if needed
        if self.pdf.get_y() > 250:
            self.pdf.add_page()
            
        # Format title based on level
        if level == 1:
            self.pdf.set_font('helvetica', 'B', 18)
            self.pdf.cell(0, 15, title, new_x="LMARGIN", new_y="NEXT")
        elif level == 2:
            self.pdf.set_font('helvetica', 'B', 16)
            self.pdf.cell(0, 12, title, new_x="LMARGIN", new_y="NEXT")
        else:
            self.pdf.set_font('helvetica', 'B', 14)
            self.pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
            
        # Add content
        self.pdf.set_font('helvetica', '', 12)
        self.pdf.multi_cell(0, 8, content)
        self.pdf.ln(10)
        
    def add_bullet_list(self, title, items):
        """Add a bulleted list"""
        self.add_content_section(title, "")
        
        self.pdf.set_font('helvetica', '', 12)
        for item in items:
            self.pdf.cell(10, 8, "•", new_x="RIGHT", new_y="TOP")
            self.pdf.multi_cell(0, 8, f" {item}")
            self.pdf.ln(2)
            
        self.pdf.ln(5)
        
    def add_table(self, title, headers, data):
        """Add a formatted table"""
        self.add_content_section(title, "")
        
        # Table header
        self.pdf.set_font('helvetica', 'B', 12)
        col_width = self.pdf.w / (len(headers) + 1)
        
        for header in headers:
            self.pdf.cell(col_width, 10, header, border=1, align='C')
        self.pdf.ln()
        
        # Table data
        self.pdf.set_font('helvetica', '', 11)
        for row in data:
            for item in row:
                self.pdf.cell(col_width, 10, str(item), border=1, align='C')
            self.pdf.ln()
            
        self.pdf.ln(10)
        
    def add_summary_box(self, title, items):
        """Add a summary box with key points"""
        self.pdf.add_page()
        
        # Box background
        self.pdf.set_fill_color(240, 240, 245)
        self.pdf.rect(10, 10, 190, 80, 'F')
        
        # Title
        self.pdf.set_xy(15, 20)
        self.pdf.set_font('helvetica', 'B', 16)
        self.pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        
        # Items
        self.pdf.set_xy(20, 35)
        self.pdf.set_font('helvetica', '', 12)
        for i, item in enumerate(items):
            self.pdf.cell(0, 8, f"{i+1}. {item}", new_x="LMARGIN", new_y="NEXT")
            
        self.pdf.ln(15)
        
    def add_page_number(self):
        """Add page number to current page"""
        self.pdf.set_y(-15)
        self.pdf.set_font('helvetica', 'I', 10)
        page_num = self.pdf.page_no()
        self.pdf.cell(0, 10, f"Page {page_num}", align='C')
        
    def generate(self, filename="improved_document.pdf"):
        """Generate and save the PDF"""
        self.pdf.output(filename)
        return filename


def create_improved_pdf():
    """Create an improved PDF with enhanced features"""
    
    print("Creating Improved PDF Document...")
    print("=" * 50)
    
    generator = ImprovedPDFGenerator("Enhanced Report")
    
    # Add title page
    generator.add_title_page()
    
    # Section 1: Introduction
    generator.add_content_section("1. Introduction", """
This document represents an improved PDF generation approach with enhanced 
formatting capabilities. It demonstrates advanced features for creating 
professional documents programmatically.

Key improvements include:
- Better page layout management
- Structured content organization
- Enhanced table formatting
- Improved bullet point lists
- Professional title page design
- Consistent styling throughout
    """)
    
    # Section 2: Key Features
    features = [
        "Multi-page document support with auto-pagination",
        "Professional title page with date and versioning",
        "Hierarchical section headings (H1, H2, H3)",
        "Formatted tables with proper alignment",
        "Bulleted lists with custom styling",
        "Automatic content flow management",
        "Page numbering and consistent margins",
        "Clean typography with Helvetica font",
        "Optimized for both screen and print"
    ]
    generator.add_bullet_list("2. Key Features", features)
    
    # Section 3: Performance Metrics
    performance_headers = ["Metric", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"]
    performance_data = [
        ["Revenue Growth", "12.5%", "15.2%", "18.4%", "21.7%"],
        ["Customer Satisfaction", "88.2%", "90.1%", "91.8%", "93.4%"],
        ["Operational Efficiency", "85.6%", "88.9%", "92.3%", "94.7%"],
        ["Market Share", "22.4%", "24.1%", "26.8%", "29.3%"],
        ["Employee Retention", "89.3%", "90.8%", "92.1%", "93.6%"]
    ]
    generator.add_table("3. Performance Metrics", performance_headers, performance_data)
    
    # Section 4: Technical Implementation
    generator.add_content_section("4. Technical Implementation", """
This improved PDF generator is built using the fpdf2 library with Python. 
The implementation focuses on:

• Clean separation of concerns between document structure and content
• Reusable components for tables, lists, and sections
• Proper error handling and fallback mechanisms
• Memory-efficient document generation
• Cross-platform compatibility

The generator automatically handles page breaks, ensures consistent 
formatting across all pages, and provides professional document output.
    """)
    
    # Section 5: Data Analysis
    analysis_headers = ["Data Point", "Value", "Target", "Variance", "Status"]
    analysis_data = [
        ["Monthly Active Users", "2.5M", "2.3M", "+8.7%", "✓ Exceeded"],
        ["Conversion Rate", "4.8%", "4.5%", "+6.7%", "✓ Exceeded"],
        ["Customer Acquisition Cost", "$45", "$50", "-10.0%", "✓ Below Target"],
        ["Lifetime Value", "$850", "$800", "+6.3%", "✓ Exceeded"],
        ["Churn Rate", "2.1%", "2.5%", "-16.0%", "✓ Below Target"],
        ["Net Promoter Score", "72", "70", "+2.9%", "✓ Exceeded"]
    ]
    generator.add_table("5. Data Analysis Results", analysis_headers, analysis_data)
    
    # Section 6: Summary Box
    summary_items = [
        "Document contains 6+ pages of structured content",
        "All formatting is handled programmatically",
        "Tables include proper headers and alignment",
        "Automatic page management prevents overflow",
        "Professional styling with consistent margins",
        "Optimized for readability and presentation"
    ]
    generator.add_summary_box("Document Summary", summary_items)
    
    # Add conclusion
    generator.add_content_section("6. Conclusion", """
This improved PDF generator demonstrates the capabilities of automated 
document creation with Python. The enhanced features provide:

1. Professional document formatting that matches manual creation
2. Consistent styling across all pages and sections
3. Advanced layout capabilities for complex documents
4. Efficient generation of multi-page reports
5. Easy customization for different use cases

The system is scalable and can be extended with additional features 
such as charts, images, and custom templates as needed.
    """)
    
    # Add page numbers to all pages
    for i in range(1, generator.pdf.page_no() + 1):
        generator.pdf.page = i
        generator.add_page_number()
    
    # Generate the PDF
    filename = generator.generate("improved_advanced_report.pdf")
    
    print(f"✓ Successfully created: {filename}")
    print(f"✓ Pages generated: {generator.pdf.page_no()}")
    print(f"✓ Features included: Advanced formatting, tables, lists, summaries")
    
    return filename


if __name__ == "__main__":
    try:
        filename = create_improved_pdf()
        print("\n✅ Enhanced PDF generation completed successfully!")
        print("=" * 50)
        
        # Show file info
        import os
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"File size: {size:,} bytes ({size/1024:.1f} KB)")
            
    except Exception as e:
        print(f"\n❌ Error creating PDF: {e}")
        print("Creating simple fallback...")
        
        # Simple fallback
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('helvetica', 'B', 16)
            pdf.cell(0, 10, 'Simple Fallback PDF', new_x="LMARGIN", new_y="NEXT", align='C')
            pdf.ln(10)
            pdf.set_font('helvetica', '', 12)
            pdf.multi_cell(0, 10, 'The enhanced PDF generator encountered an error.')
            pdf.output('simple_fallback_improved.pdf')
            print("✓ Created fallback PDF: simple_fallback_improved.pdf")
        except Exception as e2:
            print(f"❌ Fallback also failed: {e2}")