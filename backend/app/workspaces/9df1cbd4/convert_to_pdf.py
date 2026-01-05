#!/usr/bin/env python3
"""
Script to convert Markdown documentation to PDF for transfer.
Uses ReportLab for PDF generation.
"""

import os
import re
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.colors import black, blue, darkblue
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def clean_markdown_content(content):
    """
    Clean and prepare markdown content for PDF conversion.
    """
    # Remove code block markers
    content = re.sub(r'```[\w]*\n', '', content)
    content = re.sub(r'```', '', content)
    
    # Convert headers
    content = re.sub(r'^### (.*?)$', r'<b>\1</b>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.*?)$', r'<font size="14"><b>\1</b></font>', content, flags=re.MULTILINE)
    content = re.sub(r'^# (.*?)$', r'<font size="16"><b>\1</b></font>', content, flags=re.MULTILINE)
    
    # Convert bold and italic
    content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', content)
    content = re.sub(r'\*(.*?)\*', r'<i>\1</i>', content)
    
    # Convert lists
    content = re.sub(r'^\s*[-*]\s+(.*?)$', r'• \1', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*\d+\.\s+(.*?)$', r'\1', content, flags=re.MULTILINE)
    
    # Convert tables (simple approach)
    content = re.sub(r'\|', ' | ', content)
    
    # Clean up extra whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content


def create_pdf_from_markdown(markdown_file, pdf_file):
    """
    Create a PDF file from Markdown content.
    """
    print(f"Reading markdown file: {markdown_file}")
    
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File {markdown_file} not found.")
        return False
    except Exception as e:
        print(f"Error reading file: {e}")
        return False
    
    # Clean the markdown content
    cleaned_content = clean_markdown_content(content)
    
    # Split into paragraphs
    paragraphs = cleaned_content.split('\n\n')
    
    print(f"Creating PDF file: {pdf_file}")
    
    try:
        # Create PDF document
        doc = SimpleDocTemplate(
            pdf_file,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Get default styles
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=darkblue
        )
        
        heading1_style = ParagraphStyle(
            'CustomHeading1',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            textColor=blue
        )
        
        heading2_style = ParagraphStyle(
            'CustomHeading2',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            textColor=blue
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        )
        
        code_style = ParagraphStyle(
            'CustomCode',
            parent=styles['Code'],
            fontSize=9,
            fontName='Courier',
            spaceAfter=6,
            leftIndent=20,
            backColor='#f5f5f5'
        )
        
        # Build story (content)
        story = []
        
        # Add title
        title = "Documentation Complète de l'API Notion et Plan d'Amélioration"
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 24))
        
        # Add metadata
        metadata = f"<b>Fichier Source:</b> {markdown_file}<br/>"
        metadata += f"<b>Date de Génération:</b> {os.path.basename(pdf_file)}<br/>"
        metadata += f"<b>Pages:</b> PDF optimisé pour transfert<br/>"
        story.append(Paragraph(metadata, normal_style))
        story.append(Spacer(1, 20))
        
        # Add content paragraphs
        for i, para in enumerate(paragraphs):
            if not para.strip():
                continue
                
            # Determine style based on content
            if para.startswith('<font size="16"><b>'):
                story.append(Paragraph(para, heading1_style))
            elif para.startswith('<font size="14"><b>'):
                story.append(Paragraph(para, heading2_style))
            elif para.startswith('<b>') and not para.startswith('<font'):
                story.append(Paragraph(para, heading2_style))
            elif '```' in para or '    ' in para[:4]:  # Code block
                # Clean code blocks
                code_text = para.replace('```', '').strip()
                story.append(Paragraph(f'<font face="Courier">{code_text}</font>', code_style))
            else:
                story.append(Paragraph(para, normal_style))
            
            # Add page break for major sections
            if i > 0 and i % 50 == 0:
                story.append(PageBreak())
        
        # Build PDF
        doc.build(story)
        print(f"PDF created successfully: {pdf_file}")
        
        # Get file size
        file_size = os.path.getsize(pdf_file)
        print(f"File size: {file_size / 1024:.2f} KB")
        
        return True
        
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return False


def compress_pdf(input_pdf, output_pdf):
    """
    Compress PDF file if needed.
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        
        print(f"Compressing PDF: {input_pdf} -> {output_pdf}")
        
        reader = PdfReader(input_pdf)
        writer = PdfWriter()
        
        # Copy all pages
        for page in reader.pages:
            writer.add_page(page)
        
        # Add metadata
        writer.add_metadata({
            '/Title': "Documentation API Notion",
            '/Author': "AI Documentation Assistant",
            '/Subject': "Documentation complète en français de l'API Notion",
            '/Keywords': "API, Notion, Documentation, Français, Développeur",
            '/Creator': "Python ReportLab & PyPDF2"
        })
        
        # Write compressed PDF
        with open(output_pdf, 'wb') as f:
            writer.write(f)
        
        original_size = os.path.getsize(input_pdf)
        compressed_size = os.path.getsize(output_pdf)
        
        print(f"Original size: {original_size / 1024:.2f} KB")
        print(f"Compressed size: {compressed_size / 1024:.2f} KB")
        print(f"Compression ratio: {(1 - compressed_size/original_size) * 100:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"Error compressing PDF: {e}")
        return False


def main():
    """Main function to prepare PDF for transfer."""
    
    # Configuration
    markdown_file = "documentation-complete-compiled.md"
    pdf_file = "documentation-api-notion.pdf"
    compressed_pdf_file = "documentation-api-notion-compressed.pdf"
    
    print("=" * 60)
    print("Préparation du PDF pour transfert")
    print("=" * 60)
    
    # Step 1: Create PDF from markdown
    if not os.path.exists(markdown_file):
        print(f"Error: Markdown file '{markdown_file}' not found.")
        return
    
    success = create_pdf_from_markdown(markdown_file, pdf_file)
    
    if not success:
        print("Failed to create PDF.")
        return
    
    # Step 2: Compress PDF
    if os.path.exists(pdf_file):
        compress_pdf(pdf_file, compressed_pdf_file)
        
        # Check if compression was beneficial
        if os.path.exists(compressed_pdf_file):
            original_size = os.path.getsize(pdf_file)
            compressed_size = os.path.getsize(compressed_pdf_file)
            
            if compressed_size < original_size:
                print(f"\n✓ PDF compressé prêt pour transfert: {compressed_pdf_file}")
                print(f"✓ Taille optimisée: {compressed_size / 1024:.2f} KB")
            else:
                print(f"\n✓ PDF prêt pour transfert: {pdf_file}")
                print(f"✓ Taille: {original_size / 1024:.2f} KB")
                
                # Remove compressed file if it's larger
                os.remove(compressed_pdf_file)
        else:
            print(f"\n✓ PDF prêt pour transfert: {pdf_file}")
            print(f"✓ Taille: {os.path.getsize(pdf_file) / 1024:.2f} KB")
    
    print("\n" + "=" * 60)
    print("Résumé:")
    
    # List all PDF files
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    for pdf in pdf_files:
        size = os.path.getsize(pdf)
        print(f"  • {pdf}: {size / 1024:.2f} KB")
    
    print("=" * 60)


if __name__ == "__main__":
    main()