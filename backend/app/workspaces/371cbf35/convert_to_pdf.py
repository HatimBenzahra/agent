#!/usr/bin/env python3
"""
Script pour convertir le fichier Markdown en PDF
"""

import markdown
from fpdf import FPDF
import os

def markdown_to_pdf(md_file_path, pdf_file_path):
    """
    Convertit un fichier Markdown en PDF
    """
    # Lire le contenu Markdown
    with open(md_file_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convertir Markdown en HTML simple
    html_content = markdown.markdown(markdown_content)
    
    # Créer un PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Configurer la police
    pdf.set_font('Arial', '', 12)
    
    # Ajouter le titre
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Vélizy-Villacoublay - Wikipédia', ln=True)
    pdf.ln(10)
    
    # Convertir HTML simplifié en texte pour PDF
    pdf.set_font('Arial', '', 12)
    
    # Traiter le contenu ligne par ligne
    lines = markdown_content.split('\n')
    
    for line in lines:
        # Nettoyer et formater les lignes
        if line.startswith('# '):
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, line[2:], ln=True)
            pdf.set_font('Arial', '', 12)
        elif line.startswith('## '):
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, line[3:], ln=True)
            pdf.set_font('Arial', '', 12)
        elif line.startswith('### '):
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, line[4:], ln=True)
            pdf.set_font('Arial', '', 12)
        elif line.startswith('#### '):
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(0, 10, line[5:], ln=True)
            pdf.set_font('Arial', '', 12)
        elif line.strip() == '':
            pdf.ln(5)
        else:
            # Gérer les listes
            if line.strip().startswith('- '):
                line = '• ' + line.strip()[2:]
            
            # Ajouter le texte normal
            pdf.multi_cell(0, 10, line)
    
    # Sauvegarder le PDF
    pdf.output(pdf_file_path)
    
    print(f"PDF créé avec succès : {pdf_file_path}")

def main():
    md_file = "velizy_villacoublay.md"
    pdf_file = "velizy_villacoublay.pdf"
    
    # Vérifier si le fichier Markdown existe
    if not os.path.exists(md_file):
        print(f"Fichier {md_file} non trouvé!")
        return
    
    try:
        markdown_to_pdf(md_file, pdf_file)
        print(f"Conversion terminée! PDF disponible dans {pdf_file}")
    except Exception as e:
        print(f"Erreur lors de la conversion : {e}")

if __name__ == "__main__":
    main()