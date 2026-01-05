#!/usr/bin/env python3
"""
Script pour convertir le fichier Markdown en PDF (version corrigée)
"""

from fpdf import FPDF
import os

def markdown_to_pdf(md_file_path, pdf_file_path):
    """
    Convertit un fichier Markdown en PDF (version simplifiée)
    """
    # Lire le contenu Markdown
    with open(md_file_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Créer un PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Configurer la police UTF-8 compatible
    pdf.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
    pdf.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', uni=True)
    pdf.add_font('DejaVu', 'I', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf', uni=True)
    pdf.add_font('DejaVu', 'BI', '/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf', uni=True)
    
    # Titre principal
    pdf.set_font('DejaVu', 'B', 16)
    pdf.cell(0, 10, 'Vélizy-Villacoublay', ln=True, align='C')
    pdf.ln(10)
    
    # Traiter le contenu ligne par ligne
    pdf.set_font('DejaVu', '', 12)
    
    lines = markdown_content.split('\n')
    for line in lines:
        if not line.strip():
            pdf.ln(5)
            continue
            
        # Nettoyer la ligne
        line = line.replace('•', '-').replace('**', '').replace('*', '')
        
        # Déterminer le style
        if line.startswith('# '):
            pdf.set_font('DejaVu', 'B', 16)
            pdf.cell(0, 10, line[2:], ln=True)
            pdf.set_font('DejaVu', '', 12)
            pdf.ln(2)
        elif line.startswith('## '):
            pdf.set_font('DejaVu', 'B', 14)
            pdf.cell(0, 10, line[3:], ln=True)
            pdf.set_font('DejaVu', '', 12)
            pdf.ln(2)
        elif line.startswith('### '):
            pdf.set_font('DejaVu', 'B', 12)
            pdf.cell(0, 10, line[4:], ln=True)
            pdf.set_font('DejaVu', '', 12)
            pdf.ln(2)
        elif line.startswith('#### '):
            pdf.set_font('DejaVu', 'B', 11)
            pdf.cell(0, 10, line[5:], ln=True)
            pdf.set_font('DejaVu', '', 12)
            pdf.ln(2)
        elif line.strip().startswith('- '):
            # Élément de liste
            pdf.set_font('DejaVu', '', 12)
            pdf.cell(5)
            pdf.multi_cell(0, 10, "• " + line.strip()[2:])
        else:
            # Texte normal
            pdf.set_font('DejaVu', '', 12)
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
        print("Essai d'une méthode alternative...")
        
        # Méthode alternative sans Unicode
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Nettoyer les caractères problématiques
        content = content.replace('•', '-').replace('€', 'EUR').replace('°', 'deg')
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Velizy-Villacoublay - Wikipedia', ln=True, align='C')
        pdf.ln(10)
        pdf.set_font('Arial', '', 12)
        
        # Ajouter le contenu nettoyé
        for line in content.split('\n'):
            if line.strip():
                pdf.multi_cell(0, 10, line[:200])  # Limiter la longueur
        
        pdf.output(pdf_file)
        print(f"PDF créé avec méthode alternative: {pdf_file}")

if __name__ == "__main__":
    main()