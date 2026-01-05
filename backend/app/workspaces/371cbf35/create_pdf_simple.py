#!/usr/bin/env python3
"""
Script pour créer un PDF simple sans problèmes d'encodage
"""

from fpdf import FPDF
import os

def create_simple_pdf(md_file_path, pdf_file_path):
    """
    Crée un PDF simple à partir d'un fichier Markdown
    """
    # Lire le contenu Markdown
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Nettoyer le contenu des caractères non-ASCII
    content_clean = ""
    for char in content:
        # Garder seulement les caractères ASCII et quelques caractères communs
        if ord(char) < 128:
            content_clean += char
        else:
            # Remplacer les caractères spéciaux
            replacements = {
                'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
                'à': 'a', 'â': 'a', 'ä': 'a',
                'î': 'i', 'ï': 'i',
                'ô': 'o', 'ö': 'o',
                'ù': 'u', 'û': 'u', 'ü': 'u',
                'ç': 'c',
                'É': 'E', 'È': 'E',
                'À': 'A', 'Â': 'A',
                'Î': 'I',
                'Ô': 'O',
                'Ù': 'U',
                'Ç': 'C',
                '€': 'EUR', '°': 'deg', '•': '-', '→': '->',
                '«': '"', '»': '"', "'": "'", '"': '"'
            }
            content_clean += replacements.get(char, ' ')
    
    # Créer un PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Titre
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'VELIZY-VILLACOUBLAY', ln=True, align='C')
    pdf.ln(10)
    
    # Contenu
    pdf.set_font('Arial', '', 12)
    
    # Diviser en lignes et traiter
    lines = content_clean.split('\n')
    for line in lines:
        if not line.strip():
            pdf.ln(5)
            continue
            
        # Titres
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
        else:
            # Texte normal
            # Tronquer les lignes trop longues
            if len(line) > 100:
                parts = []
                while len(line) > 100:
                    # Trouver un espace pour couper
                    cut_pos = line[:100].rfind(' ')
                    if cut_pos == -1:
                        cut_pos = 100
                    parts.append(line[:cut_pos])
                    line = line[cut_pos:].strip()
                if line:
                    parts.append(line)
                
                for part in parts:
                    pdf.multi_cell(0, 10, part)
            else:
                pdf.multi_cell(0, 10, line)
    
    # Sauvegarder
    pdf.output(pdf_file_path)
    print(f"PDF créé avec succès: {pdf_file_path}")
    return True

def main():
    md_file = "velizy_villacoublay.md"
    pdf_file = "velizy_villacoublay.pdf"
    
    if not os.path.exists(md_file):
        print(f"Fichier {md_file} non trouvé!")
        return
    
    try:
        if create_simple_pdf(md_file, pdf_file):
            print(f"\n=== RÉSUMÉ ===")
            print(f"✓ Fichier Markdown extrait: {md_file}")
            print(f"✓ Fichier PDF généré: {pdf_file}")
            print(f"✓ Tâche terminée avec succès!")
    except Exception as e:
        print(f"Erreur: {e}")
        print("\nSolution alternative: Le fichier Markdown a été créé avec succès.")
        print("Vous pouvez le convertir manuellement avec un autre outil.")

if __name__ == "__main__":
    main()