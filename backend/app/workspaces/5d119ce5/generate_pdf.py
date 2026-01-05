#!/usr/bin/env python3
"""
Generate PDF file with fpdf2 library
"""

from fpdf import FPDF
from datetime import datetime

def generate_pdf():
    """Generate a PDF document with sample content"""
    
    # Create PDF object
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Add a page
    pdf.add_page()
    
    # Set font for title
    pdf.set_font('Arial', 'B', 16)
    
    # Add title
    pdf.cell(0, 10, 'Document PDF Généré avec Python', ln=True, align='C')
    pdf.ln(10)
    
    # Add date
    pdf.set_font('Arial', '', 12)
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 10, f'Généré le: {current_date}', ln=True, align='C')
    pdf.ln(20)
    
    # Add content sections in French
    sections = [
        ("Introduction", 
         "Ce document PDF a été généré en utilisant Python et la bibliothèque fpdf2. "
         "Il démontre comment créer des PDFs professionnels de manière programmatique."),
        
        ("Pourquoi générer des PDFs avec Python?",
         "Python offre plusieurs bibliothèques pour la génération de PDFs, incluant fpdf2, ReportLab, "
         "et PyPDF2. Ces bibliothèques permettent de créer, modifier et manipuler des documents PDF "
         "automatiquement, ce qui est utile pour générer des rapports, factures, documents, et plus."),
        
        ("Cas d'utilisation courants",
         "1. Génération automatique de rapports\n"
         "2. Création de factures\n"
         "3. Modèles de documents\n"
         "4. Rapports de visualisation de données\n"
         "5. Traitement de documents en lot"),
        
        ("Exemple de Table",
         "Voici un tableau de démonstration avec des données fictives.")
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
    pdf.cell(0, 10, 'Tableau de Données Exemple', ln=True)
    pdf.ln(5)
    
    # Table headers
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(50, 10, 'Produit', border=1)
    pdf.cell(40, 10, 'Quantité', border=1)
    pdf.cell(40, 10, 'Prix', border=1)
    pdf.cell(40, 10, 'Total', border=1)
    pdf.ln()
    
    # Table data
    pdf.set_font('Arial', '', 12)
    data = [
        ('Produit A', '2', '10.00 €', '20.00 €'),
        ('Produit B', '3', '15.00 €', '45.00 €'),
        ('Produit C', '1', '25.00 €', '25.00 €'),
        ('Produit D', '5', '8.00 €', '40.00 €'),
        ('Produit E', '4', '12.50 €', '50.00 €')
    ]
    
    for item, qty, price, total in data:
        pdf.cell(50, 10, item, border=1)
        pdf.cell(40, 10, qty, border=1)
        pdf.cell(40, 10, price, border=1)
        pdf.cell(40, 10, total, border=1)
        pdf.ln()
    
    # Calculate total
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(130, 10, 'Total Général', border=1)
    pdf.cell(40, 10, '180.00 €', border=1)
    pdf.ln()
    
    pdf.ln(20)
    
    # Add footer
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, 'Document généré automatiquement avec Python - Page 1/1', align='C')
    
    # Save PDF file
    output_file = 'document_généré.pdf'
    pdf.output(output_file)
    
    print(f"PDF créé avec succès: {output_file}")
    return output_file

def main():
    """Main function to generate PDF"""
    print("Génération du document PDF...")
    print("=" * 40)
    
    try:
        filename = generate_pdf()
        print(f"✅ Document PDF créé: {filename}")
        print(f"Le fichier contient plusieurs sections et un tableau de données.")
        
        # Try to get file size
        import os
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"📄 Taille du fichier: {size} octets")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération du PDF: {e}")
        print("Tentative de création d'un PDF minimal...")
        
        # Try to create minimal PDF as fallback
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, 'PDF Minimal', ln=True, align='C')
            pdf.ln(10)
            pdf.set_font('Arial', '', 12)
            pdf.multi_cell(0, 10, 'Document PDF de secours généré avec Python.')
            pdf.output('pdf_minimal.pdf')
            print("✅ PDF minimal créé: pdf_minimal.pdf")
        except Exception as e2:
            print(f"❌ Échec complet: {e2}")

if __name__ == "__main__":
    main()