#!/usr/bin/env python3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def test_pdf_creation():
    # Create a simple PDF to test
    filename = "test_output.pdf"
    
    try:
        # Create a new PDF
        c = canvas.Canvas(filename, pagesize=letter)
        
        # Add some content
        c.drawString(100, 750, "PDF Generation Test")
        c.drawString(100, 730, "ReportLab is working correctly!")
        c.drawString(100, 700, f"Version: 4.4.7")
        
        # Save the PDF
        c.save()
        
        # Check if file was created
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"✓ PDF file created successfully: {filename}")
            print(f"  File size: {file_size} bytes")
            
            # Clean up
            os.remove(filename)
            print(f"  Test file cleaned up")
            return True
        else:
            print("✗ PDF file was not created")
            return False
            
    except Exception as e:
        print(f"✗ Error creating PDF: {e}")
        return False

if __name__ == "__main__":
    success = test_pdf_creation()
    if success:
        print("\n✅ All libraries are working correctly!")
    else:
        print("\n❌ There was an issue with PDF generation")