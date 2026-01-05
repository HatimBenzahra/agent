#!/usr/bin/env python3
"""
Structured PDF Generator using fpdf2
This script creates a well-structured PDF with proper formatting
"""

from fpdf import FPDF
from datetime import datetime
import textwrap

class StructuredPDFGenerator:
    def __init__(self, title="Document"):
        """Initialize the PDF generator with default settings"""
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.title = title
        self.setup_fonts()
        
    def setup_fonts(self):
        """Setup default fonts"""
        self.pdf.add_font("Helvetica", "", "")
        self.pdf.add_font("Helvetica", "B", "")
        self.pdf.set_font("Helvetica", size=12)
        
    def add_title_page(self, title, subtitle=None, author=None):
        """Add a title page with centered content"""
        self.pdf.add_page()
        self.pdf.set_font("Helvetica", "B", 24)
        self.pdf.cell(0, 40, "", ln=True)  # Add some space
        
        # Title
        self.pdf.cell(0, 20, title, align="C", ln=True)
        
        # Subtitle if provided
        if subtitle:
            self.pdf.set_font("Helvetica", "", 16)
            self.pdf.cell(0, 15, subtitle, align="C", ln=True)
            
        # Author if provided
        if author:
            self.pdf.set_font("Helvetica", "I", 14)
            self.pdf.cell(0, 40, "", ln=True)  # Add space
            self.pdf.cell(0, 10, f"by {author}", align="C", ln=True)
            
        # Date
        current_date = datetime.now().strftime("%B %d, %Y")
        self.pdf.set_font("Helvetica", "", 12)
        self.pdf.cell(0, 60, "", ln=True)  # Add space
        self.pdf.cell(0, 10, current_date, align="C", ln=True)
        
    def add_section(self, title, content):
        """Add a section with title and content"""
        self.pdf.add_page()
        
        # Section title
        self.pdf.set_font("Helvetica", "B", 16)
        self.pdf.cell(0, 10, title, ln=True)
        self.pdf.ln(5)  # Add spacing
        
        # Section content
        self.pdf.set_font("Helvetica", "", 12)
        
        # Wrap text to fit page width
        lines = textwrap.wrap(content, width=85)
        for line in lines:
            self.pdf.multi_cell(0, 6, line)
            self.pdf.ln(2)
            
        self.pdf.ln(10)  # Add spacing after section
        
    def add_table_of_contents(self, sections):
        """Add a table of contents"""
        self.pdf.add_page()
        
        # Table of contents title
        self.pdf.set_font("Helvetica", "B", 18)
        self.pdf.cell(0, 10, "Table of Contents", ln=True)
        self.pdf.ln(10)
        
        # List sections with page numbers
        self.pdf.set_font("Helvetica", "", 14)
        for i, section in enumerate(sections, 1):
            self.pdf.cell(0, 10, f"{i}. {section}", ln=True)
            self.pdf.ln(2)
            
    def add_data_table(self, headers, data, title="Data Table"):
        """Add a structured data table"""
        self.pdf.add_page()
        
        # Table title
        self.pdf.set_font("Helvetica", "B", 16)
        self.pdf.cell(0, 10, title, ln=True)
        self.pdf.ln(5)
        
        # Define column widths
        col_width = self.pdf.w / (len(headers) + 1)
        
        # Header row
        self.pdf.set_font("Helvetica", "B", 12)
        for header in headers:
            self.pdf.cell(col_width, 10, header, border=1, align="C")
        self.pdf.ln()
        
        # Data rows
        self.pdf.set_font("Helvetica", "", 12)
        for row in data:
            for item in row:
                self.pdf.cell(col_width, 10, str(item), border=1, align="C")
            self.pdf.ln()
            
        self.pdf.ln(10)  # Add spacing after table
        
    def add_bullet_points(self, title, items):
        """Add a list with bullet points"""
        self.pdf.add_page()
        
        # Section title
        self.pdf.set_font("Helvetica", "B", 16)
        self.pdf.cell(0, 10, title, ln=True)
        self.pdf.ln(5)
        
        # Bullet points
        self.pdf.set_font("Helvetica", "", 12)
        for item in items:
            # Bullet character and item
            self.pdf.cell(10, 8, "•", ln=0)
            self.pdf.multi_cell(0, 8, item)
            self.pdf.ln(2)
            
    def add_footer(self):
        """Add footer with page numbers"""
        self.pdf.set_y(-15)
        self.pdf.set_font("Helvetica", "I", 8)
        self.pdf.cell(0, 10, f"Page {self.pdf.page_no()}", align="C")
        
    def generate(self, filename="output.pdf"):
        """Generate and save the PDF file"""
        self.pdf.output(filename)
        print(f"PDF generated successfully: {filename}")


def create_sample_pdf():
    """Create a sample structured PDF with various elements"""
    
    # Initialize generator
    generator = StructuredPDFGenerator("Sample Report")
    
    # Add title page
    generator.add_title_page(
        title="Annual Report 2024",
        subtitle="A Comprehensive Analysis",
        author="John Doe"
    )
    
    # Table of contents
    sections = [
        "Executive Summary",
        "Financial Performance", 
        "Market Analysis",
        "Key Findings",
        "Recommendations",
        "Appendices"
    ]
    generator.add_table_of_contents(sections)
    
    # Section 1: Executive Summary
    generator.add_section(
        "Executive Summary",
        "This report provides a comprehensive analysis of the company's performance in 2024. "
        "The year has been marked by significant growth in key markets, improved operational "
        "efficiency, and successful product launches. Revenue increased by 15% compared to "
        "the previous year, while operating costs were reduced by 8% through strategic "
        "optimization initiatives. The company successfully expanded into three new markets "
        "and launched two innovative products that received positive customer feedback."
    )
    
    # Section 2: Data table
    headers = ["Quarter", "Revenue", "Expenses", "Profit", "Growth %"]
    data = [
        ["Q1 2024", "$1.2M", "$0.8M", "$0.4M", "12%"],
        ["Q2 2024", "$1.5M", "$0.9M", "$0.6M", "15%"],
        ["Q3 2024", "$1.8M", "$1.0M", "$0.8M", "18%"],
        ["Q4 2024", "$2.1M", "$1.1M", "$1.0M", "20%"]
    ]
    generator.add_data_table(headers, data, "Quarterly Financial Performance")
    
    # Section 3: Bullet points
    key_achievements = [
        "Successfully launched Product X in Q2, exceeding sales targets by 25%",
        "Expanded to European markets with successful integration into local distribution networks",
        "Implemented new CRM system, improving customer satisfaction by 30%",
        "Reduced carbon footprint by 15% through sustainability initiatives",
        "Achieved ISO 9001 certification for quality management systems",
        "Recruited 50 new employees across technical and marketing departments"
    ]
    generator.add_bullet_points("Key Achievements 2024", key_achievements)
    
    # Section 4: Detailed analysis
    generator.add_section(
        "Market Analysis",
        "The market analysis reveals several key trends that have shaped the industry in 2024. "
        "Digital transformation continues to accelerate, with companies investing heavily in "
        "cloud infrastructure and AI technologies. Consumer preferences have shifted towards "
        "sustainable products, with 68% of survey respondents indicating willingness to pay "
        "premium prices for eco-friendly options. Competition has intensified, particularly "
        "from emerging startups leveraging innovative business models. However, our brand "
        "recognition remains strong, with customer loyalty scores increasing by 22% year-over-year."
    )
    
    # Section 5: Another data table
    region_headers = ["Region", "Market Share", "Revenue", "Growth", "Competitors"]
    region_data = [
        ["North America", "35%", "$2.8M", "18%", "8"],
        ["Europe", "25%", "$2.0M", "22%", "12"],
        ["Asia Pacific", "20%", "$1.6M", "25%", "15"],
        ["Latin America", "12%", "$0.96M", "30%", "10"],
        ["Middle East", "8%", "$0.64M", "35%", "7"]
    ]
    generator.add_data_table(region_headers, region_data, "Regional Performance Analysis")
    
    # Section 6: Recommendations with bullet points
    recommendations = [
        "Increase investment in R&D by 20% to maintain competitive edge in innovation",
        "Expand sustainability initiatives to target 25% carbon reduction by 2025",
        "Develop strategic partnerships in emerging markets to accelerate growth",
        "Enhance digital customer experience through mobile app development",
        "Implement AI-driven analytics for improved decision making",
        "Establish employee training programs for skill development and retention"
    ]
    generator.add_bullet_points("Strategic Recommendations", recommendations)
    
    # Generate PDF
    generator.generate("structured_report.pdf")


def create_simple_pdf():
    """Create a simpler example for basic PDF generation"""
    
    generator = StructuredPDFGenerator("Simple Document")
    
    # Title page
    generator.add_title_page(
        title="My First PDF",
        subtitle="Generated with Python",
        author="PDF Generator Script"
    )
    
    # Add content sections
    generator.add_section(
        "Introduction",
        "This document demonstrates the capabilities of the structured PDF generator. "
        "With just a few lines of Python code, you can create professional-looking PDFs "
        "with titles, sections, tables, and bullet points."
    )
    
    # Add a simple table
    headers = ["Item", "Quantity", "Price", "Total"]
    data = [
        ["Notebook", "3", "$5.00", "$15.00"],
        ["Pen", "10", "$1.50", "$15.00"],
        ["Folder", "2", "$3.50", "$7.00"],
        ["Total", "", "", "$37.00"]
    ]
    generator.add_data_table(headers, data, "Sample Shopping List")
    
    # Add bullet points
    features = [
        "Easy to use Python interface",
        "Automatic text wrapping and formatting",
        "Support for tables and lists",
        "Customizable fonts and styles",
        "Automatic page numbering",
        "Professional document structure"
    ]
    generator.add_bullet_points("Key Features", features)
    
    generator.generate("simple_document.pdf")


if __name__ == "__main__":
    print("Structured PDF Generator")
    print("=" * 40)
    print("1. Create sample PDF (structured_report.pdf)")
    print("2. Create simple PDF (simple_document.pdf)")
    print("3. Create custom PDF")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print("Generating sample PDF...")
        create_sample_pdf()
    elif choice == "2":
        print("Generating simple PDF...")
        create_simple_pdf()
    elif choice == "3":
        print("\nCustom PDF generation - coming soon!")
        print("Modify the script to create your own PDF structure.")
    else:
        print("Invalid choice. Generating sample PDF by default...")
        create_sample_pdf()
    
    print("\nPDF generation complete! Check the output files.")