#!/usr/bin/env python3
"""
Generate a PDF using reportlab library with sample content
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import os

class PDFGenerator:
    def __init__(self, filename="sample_reportlab.pdf"):
        self.filename = filename
        self.doc = SimpleDocTemplate(
            filename, 
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        self.story = []
        self.styles = getSampleStyleSheet()
        
        # Add custom styles with unique names
        self.custom_styles()
        
    def custom_styles(self):
        """Create custom paragraph styles"""
        # Title style
        if not hasattr(self.styles, 'CustomTitle'):
            self.styles.add(ParagraphStyle(
                name='CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#2c3e50'),
                alignment=TA_CENTER,
                spaceAfter=30
            ))
        
        # Subtitle style
        if not hasattr(self.styles, 'CustomSubtitle'):
            self.styles.add(ParagraphStyle(
                name='CustomSubtitle',
                parent=self.styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#34495e'),
                alignment=TA_CENTER,
                spaceAfter=20
            ))
        
        # Section header style
        if not hasattr(self.styles, 'SectionHeader'):
            self.styles.add(ParagraphStyle(
                name='SectionHeader',
                parent=self.styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#2980b9'),
                spaceBefore=20,
                spaceAfter=10
            ))
        
        # MyBodyText style (using different name)
        if not hasattr(self.styles, 'MyBodyText'):
            self.styles.add(ParagraphStyle(
                name='MyBodyText',
                parent=self.styles['Normal'],
                fontSize=11,
                leading=14,
                spaceAfter=6
            ))
        
        # Footer style
        if not hasattr(self.styles, 'MyFooter'):
            self.styles.add(ParagraphStyle(
                name='MyFooter',
                parent=self.styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#7f8c8d'),
                alignment=TA_CENTER
            ))
    
    def add_title_page(self):
        """Add title page content"""
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Title
        title = Paragraph("Sample PDF Document", self.styles['CustomTitle'])
        self.story.append(title)
        
        # Subtitle
        subtitle = Paragraph("Generated with ReportLab Library", self.styles['CustomSubtitle'])
        self.story.append(subtitle)
        
        # Spacer
        self.story.append(Spacer(1, 60))
        
        # Creation date
        date_text = Paragraph(f"Created on: {current_date}", self.styles['CustomSubtitle'])
        self.story.append(date_text)
        
        # Spacer for page break
        self.story.append(Spacer(1, 200))
        
    def add_content_sections(self):
        """Add main content sections"""
        # Introduction section
        self.story.append(Paragraph("Introduction", self.styles['SectionHeader']))
        
        intro_text = """
        This is a sample PDF document generated using the ReportLab library for Python.
        ReportLab is a powerful PDF generation toolkit that allows you to create complex
        documents with text, tables, images, and various formatting options.
        """
        self.story.append(Paragraph(intro_text, self.styles['MyBodyText']))
        
        # Features section
        self.story.append(Paragraph("Key Features", self.styles['SectionHeader']))
        
        features = [
            "Text formatting with different fonts, sizes, and colors",
            "Table creation with custom styling",
            "Image insertion and manipulation",
            "Page layout control including margins and page sizes",
            "Paragraph styling with indentation and alignment",
            "Header and footer management",
            "Multi-page document support",
            "PDF compression and optimization"
        ]
        
        for feature in features:
            bullet_text = Paragraph(f"• {feature}", self.styles['MyBodyText'])
            self.story.append(bullet_text)
        
        # Sample table
        self.story.append(Paragraph("Sample Data Table", self.styles['SectionHeader']))
        
        # Create table data
        data = [
            ["ID", "Product", "Category", "Price", "Quantity"],
            ["001", "Laptop", "Electronics", "$999.99", "45"],
            ["002", "Mouse", "Electronics", "$29.99", "120"],
            ["003", "Notebook", "Office", "$12.50", "200"],
            ["004", "Pen", "Office", "$2.99", "500"],
            ["005", "Coffee Mug", "Kitchen", "$15.75", "85"]
        ]
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#2c3e50')),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 20))
        
        # Additional content
        self.story.append(Paragraph("Document Structure", self.styles['SectionHeader']))
        
        structure_text = """
        A typical PDF document generated with ReportLab consists of:
        
        1. Flowables - These are the elements that make up the document (text, images, tables)
        2. Styles - Predefined formatting rules for different elements
        3. Document Template - Defines the page layout and properties
        4. Build Process - The flowables are assembled into pages
        
        The document is built by creating a list of flowables and then passing them to
        the document's build() method, which handles pagination automatically.
        """
        self.story.append(Paragraph(structure_text, self.styles['MyBodyText']))
        
    def add_footer(self):
        """Add footer to each page"""
        # For demonstration, we'll add a simple footer at the end
        self.story.append(Spacer(1, 30))
        footer_text = "Sample PDF Document • Generated with ReportLab • Page information available"
        footer = Paragraph(footer_text, self.styles['MyFooter'])
        self.story.append(footer)
    
    def generate(self):
        """Generate the PDF document"""
        print(f"Creating PDF: {self.filename}")
        
        # Add content
        self.add_title_page()
        self.add_content_sections()
        self.add_footer()
        
        # Build the PDF
        self.doc.build(self.story)
        print(f"PDF created successfully: {self.filename}")
        
        # Check file size
        if os.path.exists(self.filename):
            file_size = os.path.getsize(self.filename)
            print(f"File size: {file_size / 1024:.2f} KB")
        
        return self.filename

def main():
    """Main function to generate the PDF"""
    print("=" * 50)
    print("PDF Generator using ReportLab")
    print("=" * 50)
    
    try:
        # Check if reportlab is available
        import reportlab
        print("ReportLab library is available.")
        
        # Generate PDF
        generator = PDFGenerator()
        pdf_file = generator.generate()
        
        print("\n" + "=" * 50)
        print(f"Successfully generated: {pdf_file}")
        print("The PDF contains:")
        print("- Title page with creation date")
        print("- Introduction section")
        print("- Features list with bullet points")
        print("- Sample data table with styling")
        print("- Document structure explanation")
        print("- Footer with page information")
        
    except ImportError:
        print("Error: ReportLab library not found.")
        print("Install it using: pip install reportlab")
        return 1
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    main()