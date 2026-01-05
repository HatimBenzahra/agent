#!/usr/bin/env python3
"""
Generate a sample PDF to show capabilities
"""

from fpdf import FPDF
from datetime import datetime
import textwrap

class SamplePDFGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        
    def create_sample(self):
        """Create a sample PDF with example content"""
        
        # Title page
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 24)
        self.pdf.cell(0, 40, "", ln=True)
        self.pdf.cell(0, 20, "SAMPLE DOCUMENT", align="C", ln=True)
        
        self.pdf.set_font("Arial", "", 16)
        self.pdf.cell(0, 15, "Example PDF Content", align="C", ln=True)
        
        current_date = datetime.now().strftime("%B %d, %Y")
        self.pdf.set_font("Arial", "I", 12)
        self.pdf.cell(0, 40, "", ln=True)
        self.pdf.cell(0, 10, f"Generated on {current_date}", align="C", ln=True)
        
        # Section 1
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 18)
        self.pdf.cell(0, 10, "What type of PDF would you like?", ln=True)
        self.pdf.ln(5)
        
        self.pdf.set_font("Arial", "", 12)
        content = """This is a sample PDF to demonstrate what can be generated. 
        Please specify what content you want in your PDF:

        1. Business Report - financial data, analysis, recommendations
        2. Resume/CV - personal information, work experience, education  
        3. Invoice/Bill - items, prices, totals, payment information
        4. Manual/Guide - instructions, steps, procedures
        5. Academic Paper - research, citations, data analysis
        6. Newsletter - articles, images, news updates
        7. Presentation Slides - bullet points, diagrams
        8. Catalog/Brochure - product information, prices, images
        
        Or any other specific document type you need."""
        
        lines = textwrap.wrap(content, width=85)
        for line in lines:
            self.pdf.multi_cell(0, 6, line)
            self.pdf.ln(2)
            
        # Bullet points
        self.pdf.ln(10)
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, "What to include in your request:", ln=True)
        self.pdf.ln(5)
        
        self.pdf.set_font("Arial", "", 12)
        items = [
            "The document title and subtitle",
            "Main sections or chapters", 
            "Specific text content for each section",
            "Any tables with headers and data",
            "Bullet point lists",
            "Images or diagrams (provide file paths)",
            "Contact information or footer details",
            "Specific formatting requirements"
        ]
        
        for item in items:
            self.pdf.cell(10, 8, "•", ln=0)
            self.pdf.multi_cell(0, 8, item)
            self.pdf.ln(2)
            
        # Footer
        self.pdf.set_y(-15)
        self.pdf.set_font("Arial", "I", 8)
        self.pdf.cell(0, 10, "Please provide content details for your custom PDF", align="C")
        
        # Save the PDF
        filename = "sample_clarification.pdf"
        self.pdf.output(filename)
        return filename

def main():
    """Generate a sample PDF"""
    print("Generating sample PDF for clarification...")
    generator = SamplePDFGenerator()
    filename = generator.create_sample()
    print(f"Created: {filename}")
    print("\nPlease check the PDF and provide details about the content you want in your custom PDF.")

if __name__ == "__main__":
    main()