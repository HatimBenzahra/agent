#!/usr/bin/env python3
"""
Simple PDF Generator using ReportLab
Creates a basic PDF with sample content
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from datetime import datetime

def create_simple_pdf(filename="simple_sample.pdf"):
    """Create a simple PDF document"""
    
    # Create document with letter size
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create story (list of elements)
    story = []
    
    # Title
    title = Paragraph("Simple PDF Document", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Date
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_text = Paragraph(f"Generated on: {current_date}", styles['Normal'])
    story.append(date_text)
    story.append(Spacer(1, 24))
    
    # Introduction
    intro = Paragraph("This is a simple PDF document generated using Python's ReportLab library.", 
                     styles['Heading2'])
    story.append(intro)
    story.append(Spacer(1, 12))
    
    # Content
    content_text = """
    ReportLab is a powerful PDF generation library for Python that allows you to:
    
    • Create complex documents programmatically
    • Format text with different fonts, sizes, and colors
    • Add tables and images
    • Control page layout and margins
    • Generate multi-page documents
    
    This is a basic example showing how to create a simple PDF with text content.
    You can extend this to include more advanced features like tables, charts, and images.
    """
    content = Paragraph(content_text, styles['Normal'])
    story.append(content)
    story.append(Spacer(1, 24))
    
    # Conclusion
    conclusion = Paragraph("Conclusion", styles['Heading2'])
    story.append(conclusion)
    story.append(Spacer(1, 12))
    
    conclusion_text = """
    This demonstrates the basic usage of ReportLab. To learn more:
    
    1. Check the official ReportLab documentation
    2. Experiment with different styles and layouts
    3. Try adding tables using the Table class
    4. Add images with the Image class
    5. Explore page templates for headers and footers
    """
    conclusion_para = Paragraph(conclusion_text, styles['Normal'])
    story.append(conclusion_para)
    story.append(Spacer(1, 24))
    
    # Footer
    footer = Paragraph("End of document - Simple PDF Generator", 
                      styles['Normal'])
    story.append(footer)
    
    # Build the PDF
    doc.build(story)
    
    return filename

def main():
    """Main function"""
    print("Creating simple PDF document...")
    
    try:
        filename = create_simple_pdf()
        print(f"PDF created successfully: {filename}")
        print("\nContents:")
        print("- Title page")
        print("- Generation timestamp")
        print("- Introduction")
        print("- Key features")
        print("- Conclusion with recommendations")
        print("- Footer")
        
    except Exception as e:
        print(f"Error creating PDF: {e}")
        print("\nMake sure reportlab is installed:")
        print("pip install reportlab")
        return 1
    
    return 0

if __name__ == "__main__":
    main()