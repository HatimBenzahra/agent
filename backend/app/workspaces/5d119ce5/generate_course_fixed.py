#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import os
import datetime

def create_course_pdf(filename):
    """Create a comprehensive Python programming course PDF"""
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12,
        spaceBefore=24,
        textColor=colors.HexColor('#2E86C1')
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=6,
        spaceBefore=12,
        textColor=colors.HexColor('#3498DB')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=6,
        leading=16
    )
    
    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontSize=10,
        spaceAfter=6,
        spaceBefore=6,
        fontName='Courier',
        backColor=colors.HexColor('#F2F3F4'),
        borderPadding=5,
        leftIndent=20
    )
    
    # Create story (list of flowables)
    story = []
    
    # Add title
    story.append(Paragraph("Cours Complet de Programmation Python", title_style))
    story.append(Spacer(1, 12))
    
    # Add date and author
    today = datetime.datetime.now().strftime("%d/%m/%Y")
    story.append(Paragraph(f"<i>Créé le {today} - Par votre Assistant IA</i>", styles['Italic']))
    story.append(Spacer(1, 24))
    
    # Add introduction
    story.append(Paragraph("Introduction à Python", heading1_style))
    story.append(Paragraph(
        "Python est un langage de programmation interprété, de haut niveau, polyvalent et open source. "
        "Il est conçu pour être facile à lire et à écrire. Sa syntaxe claire en fait un excellent choix "
        "pour les débutants en programmation, tout en étant suffisamment puissant pour les applications "
        "professionnelles.",
        normal_style
    ))
    
    # Section 1: Pourquoi Python?
    story.append(Paragraph("1. Pourquoi apprendre Python?", heading1_style))
    
    advantages = [
        "Syntaxe claire et lisible",
        "Communauté active et vaste",
        "Large écosystème de bibliothèques",
        "Polyvalent (web, data science, IA, automation, etc.)",
        "Excellent pour les débutants",
        "Demandé sur le marché du travail"
    ]
    
    for advantage in advantages:
        story.append(Paragraph(f"• {advantage}", normal_style))
    
    story.append(Spacer(1, 12))
    
    # Section 2: Installation
    story.append(Paragraph("2. Installation de Python", heading1_style))
    story.append(Paragraph(
        "Pour commencer avec Python, vous devez d'abord l'installer sur votre ordinateur. "
        "Voici les étapes de base:",
        normal_style
    ))
    
    installation_steps = [
        ("Windows", "Téléchargez l'installateur depuis python.org et suivez les instructions"),
        ("macOS", "Utilisez Homebrew (brew install python) ou téléchargez depuis python.org"),
        ("Linux", "Utilisez le gestionnaire de paquets (sudo apt-get install python3)"),
        ("Vérification", "Ouvrez un terminal et tapez python3 --version pour vérifier")
    ]
    
    # Create installation table
    table_data = [["Système", "Instructions"]] + installation_steps
    installation_table = Table(table_data, colWidths=[1.5*inch, 4*inch])
    installation_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86C1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8F9F9')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D5D8DC'))
    ]))
    story.append(installation_table)
    story.append(Spacer(1, 12))
    
    # Section 3: Concepts de base
    story.append(Paragraph("3. Concepts fondamentaux de Python", heading1_style))
    
    story.append(Paragraph("3.1 Variables et types de données", heading2_style))
    story.append(Paragraph(
        "Les variables sont des conteneurs pour stocker des données. Python est typé dynamiquement, "
        "ce qui signifie que vous n'avez pas besoin de déclarer le type de variable explicitement.",
        normal_style
    ))
    
    # Add code example
    code_example = """# Déclaration de variables
nom = "Alice"          # Chaîne de caractères (string)
age = 25               # Entier (integer)
taille = 1.75          # Nombre à virgule flottante (float)
est_etudiant = True    # Booléen (boolean)

# Affichage des valeurs
print(f"Nom: {nom}")
print(f"Âge: {age}")
print(f"Taille: {taille}")
print(f"Étudiant: {est_etudiant}")"""
    
    story.append(Paragraph(code_example, code_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("3.2 Structures de contrôle", heading2_style))
    story.append(Paragraph(
        "Les structures de contrôle permettent d'exécuter du code de manière conditionnelle ou répétitive.",
        normal_style
    ))
    
    control_example = """# Instruction if/elif/else
note = 85

if note >= 90:
    print("Excellent!")
elif note >= 70:
    print("Bien!")
else:
    print("Peut mieux faire")

# Boucle for
for i in range(5):
    print(f"Compteur: {i}")

# Boucle while
compteur = 0
while compteur < 3:
    print(f"Boucle while: {compteur}")
    compteur += 1"""
    
    story.append(Paragraph(control_example, code_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("3.3 Fonctions", heading2_style))
    story.append(Paragraph(
        "Les fonctions permettent d'organiser le code en blocs réutilisables.",
        normal_style
    ))
    
    function_example = """# Définition d'une fonction
def saluer(nom, message="Bonjour"):
    \"\"\"Fonction qui salue une personne\"\"\"
    return f"{message}, {nom}!"

# Appel de la fonction
resultat = saluer("Alice")
print(resultat)  # Affiche: Bonjour, Alice!

resultat2 = saluer("Bob", "Salut")
print(resultat2)  # Affiche: Salut, Bob!"""
    
    story.append(Paragraph(function_example, code_style))
    story.append(Spacer(1, 12))
    
    # Section 4: Structures de données
    story.append(Paragraph("4. Structures de données en Python", heading1_style))
    
    data_structures = [
        ("Listes", "Collection ordonnée et modifiable", "[1, 2, 3, 'a', 'b']"),
        ("Tuples", "Collection ordonnée et immuable", "(1, 2, 3, 'a', 'b')"),
        ("Dictionnaires", "Collection de paires clé-valeur", "{'nom': 'Alice', 'âge': 25}"),
        ("Ensembles", "Collection non ordonnée d'éléments uniques", "{1, 2, 3, 4}"),
        ("Chaînes", "Séquence de caractères", "'Bonjour le monde'")
    ]
    
    table_data2 = [["Structure", "Description", "Exemple"]] + data_structures
    ds_table = Table(table_data2, colWidths=[1.5*inch, 2.5*inch, 2*inch])
    ds_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F2F3F4')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D5D8DC'))
    ]))
    story.append(ds_table)
    story.append(Spacer(1, 12))
    
    # Section 5: Projets pratiques
    story.append(Paragraph("5. Projets pratiques pour débutants", heading1_style))
    
    projects = [
        ("Calculateur simple", "Programme qui effectue des opérations mathématiques de base"),
        ("Générateur de mot de passe", "Crée des mots de passe sécurisés aléatoires"),
        ("Todo List", "Application pour gérer une liste de tâches"),
        ("Jeu du pendu", "Jeu classique du pendu avec mots aléatoires"),
        ("Analyseur de texte", "Compte les mots et caractères dans un texte"),
        ("Convertisseur d'unités", "Convertit entre différentes unités de mesure")
    ]
    
    for i, (project, description) in enumerate(projects, 1):
        story.append(Paragraph(f"5.{i} {project}", heading2_style))
        story.append(Paragraph(description, normal_style))
        story.append(Spacer(1, 6))
    
    # Section 6: Ressources d'apprentissage
    story.append(Paragraph("6. Ressources pour continuer à apprendre", heading1_style))
    
    resources = [
        ("Documentation officielle", "https://docs.python.org/3/"),
        ("Cours en ligne gratuits", "https://www.freecodecamp.org/"),
        ("Problèmes de programmation", "https://leetcode.com/"),
        ("Tutoriels vidéo", "https://www.youtube.com/c/Coreyms"),
        ("Communauté française", "https://www.python.org/community/fr/"),
        ("Livres recommandés", "Apprendre Python de Mark Lutz")
    ]
    
    for resource, link in resources:
        if link.startswith("http"):
            story.append(Paragraph(f"• <link href='{link}' color='blue'>{resource}</link>", normal_style))
        else:
            story.append(Paragraph(f"• {resource} ({link})", normal_style))
    
    story.append(Spacer(1, 12))
    
    # Conclusion
    story.append(Paragraph("Conclusion", heading1_style))
    story.append(Paragraph(
        "Python est un langage puissant et accessible qui ouvre les portes à de nombreux domaines "
        "de l'informatique moderne. En maîtrisant les concepts de base présentés dans ce cours, "
        "vous avez les fondations nécessaires pour explorer des sujets plus avancés comme le développement web, "
        "la science des données, l'intelligence artificielle ou l'automatisation.",
        normal_style
    ))
    
    story.append(Spacer(1, 24))
    
    # Final message
    story.append(Paragraph(
        "<b>Bonne chance dans votre apprentissage de Python !</b>",
        ParagraphStyle(
            'FinalMessage',
            parent=styles['Normal'],
            fontSize=14,
            alignment=1,  # Center
            spaceBefore=12,
            spaceAfter=24
        )
    ))
    
    # Build the PDF
    doc.build(story)
    print(f"PDF créé avec succès: {filename}")

def main():
    """Main function"""
    pdf_filename = "cours_python_complet_fixed.pdf"
    
    try:
        create_course_pdf(pdf_filename)
        print("Le cours a été généré avec succès!")
        print(f"Taille du fichier: {os.path.getsize(pdf_filename)} octets")
    except Exception as e:
        print(f"Erreur lors de la création du PDF: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    main()