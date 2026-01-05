#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script final pour générer un PDF complet sur Vélizy-Villacoublay
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import os
from datetime import datetime

def create_final_pdf(filename='Velizy_Villacoublay_Final.pdf'):
    """Créer un PDF final sur Vélizy-Villacoublay"""
    
    # Créer le document PDF
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        title='Vélizy-Villacoublay - Dossier Complet',
        author='Informations Wikipedia'
    )
    
    # Récupérer les styles par défaut et créer des styles personnalisés
    styles = getSampleStyleSheet()
    
    # Styles personnalisés (avec des noms uniques)
    custom_styles = {}
    
    custom_styles['MainTitle'] = ParagraphStyle(
        name='CustomMainTitle',
        parent=styles['Title'],
        fontSize=22,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    custom_styles['SectionTitle'] = ParagraphStyle(
        name='CustomSectionTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=12,
        textColor=colors.navy,
        fontName='Helvetica-Bold'
    )
    
    custom_styles['SubSection'] = ParagraphStyle(
        name='CustomSubSection',
        parent=styles['Heading2'],
        fontSize=12,
        spaceBefore=10,
        spaceAfter=6,
        textColor=colors.darkblue
    )
    
    custom_styles['BodyJustified'] = ParagraphStyle(
        name='CustomBodyJustified',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    custom_styles['BulletPoint'] = ParagraphStyle(
        name='CustomBulletPoint',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=3,
        leftIndent=10,
        firstLineIndent=-10
    )
    
    # Contenu du PDF
    story = []
    
    # Page de titre
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("VÉLIZY-VILLACOUBLAY", custom_styles['MainTitle']))
    story.append(Paragraph("Fiche d'information complète", custom_styles['SectionTitle']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Département des Yvelines - Région Île-de-France", custom_styles['SubSection']))
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph(f"Généré le {datetime.now().strftime('%d %B %Y')}", 
                          ParagraphStyle(name='DateStyle', fontSize=10, alignment=TA_CENTER)))
    
    story.append(PageBreak())
    
    # Introduction
    story.append(Paragraph("PRÉSENTATION", custom_styles['SectionTitle']))
    story.append(Paragraph("Vélizy-Villacoublay est une commune française située dans le département des Yvelines en région Île-de-France, à trois kilomètres à l'est de Versailles.", custom_styles['BodyJustified']))
    story.append(Paragraph("Ville industrielle, accueillant de nombreux sièges sociaux d'entreprise, elle constitue la partie nord du pôle scientifique et technologique Paris-Saclay.", custom_styles['BodyJustified']))
    story.append(Spacer(1, 0.25*inch))
    
    # Informations clés
    story.append(Paragraph("INFORMATIONS CLÉS", custom_styles['SectionTitle']))
    
    key_data = [
        ["Population (2023)", "23 011 habitants"],
        ["Superficie", "893 hectares (8,93 km²)"],
        ["Altitude", "102 à 179 mètres"],
        ["Gentilé", "Véliziens, Véliziennes"],
        ["Code postal", "78140"],
        ["Intercommunalité", "Versailles Grand Parc"],
        ["Maire", "Pascal Thévenot (depuis 2014)"]
    ]
    
    key_table = Table(key_data, colWidths=[6*cm, 9*cm])
    key_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0, 0), (0, -1), colors.aliceblue),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.whitesmoke])
    ]))
    story.append(key_table)
    story.append(Spacer(1, 0.25*inch))
    
    # Géographie
    story.append(Paragraph("GÉOGRAPHIE", custom_styles['SectionTitle']))
    story.append(Paragraph("Localisation", custom_styles['SubSection']))
    story.append(Paragraph("• Située à 9 km de la Porte de Saint-Cloud (Paris)", custom_styles['BulletPoint']))
    story.append(Paragraph("• À 3,5 km à l'est de Versailles", custom_styles['BulletPoint']))
    story.append(Paragraph("• Plateau dominant Paris avec altitude de 102-179 m", custom_styles['BulletPoint']))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Environnement", custom_styles['SubSection']))
    story.append(Paragraph("• 313 hectares de forêt domaniale de Meudon", custom_styles['BulletPoint']))
    story.append(Paragraph("• Plus de 65 hectares d'espaces verts aménagés", custom_styles['BulletPoint']))
    story.append(Paragraph("• Protection naturelle contre les inondations", custom_styles['BulletPoint']))
    
    story.append(PageBreak())
    
    # Urbanisme
    story.append(Paragraph("URBANISME", custom_styles['SectionTitle']))
    
    story.append(Paragraph("Occupation des sols (2018)", custom_styles['SubSection']))
    
    occupation = [
        ["Type", "%", "Surface"],
        ["Forêts", "34,1", "306 ha"],
        ["Zones ind./com.", "27,3", "245 ha"],
        ["Tissu urbain", "20,5", "184 ha"],
        ["Aéroports", "13,2", "118 ha"],
        ["Routes/rails", "3,7", "33 ha"],
        ["Sports/loisirs", "1,2", "11 ha"]
    ]
    
    occ_table = Table(occupation, colWidths=[6*cm, 3*cm, 4*cm])
    occ_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (2, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke])
    ]))
    story.append(occ_table)
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Quartiers", custom_styles['SubSection']))
    quartiers = ["Mozart", "Le Clos", "Le Mail", "Le Village", "Est", "Vélizy-Bas"]
    for q in quartiers:
        story.append(Paragraph(f"• {q}", custom_styles['BulletPoint']))
    
    # Transports
    story.append(Paragraph("TRANSPORTS", custom_styles['SectionTitle']))
    
    transports_data = [
        ["Route", "A86, RN118, RN12 - 15 min de Paris"],
        ["RER", "Ligne C - Gare Chaville-Vélizy"],
        ["Tramway", "T6 - 7 stations (depuis 2014)"],
        ["Bus", "RATP, Paris-Saclay, Vélizy Vallées"],
        ["Nuit", "Noctilien N66"]
    ]
    
    trans_table = Table(transports_data, colWidths=[4*cm, 11*cm])
    trans_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.whitesmoke])
    ]))
    story.append(trans_table)
    
    story.append(PageBreak())
    
    # Histoire
    story.append(Paragraph("HISTOIRE", custom_styles['SectionTitle']))
    
    dates_histoire = [
        ["1815", "Victoire du général Exelmans"],
        ["1937", "Fusion Vélizy-Villacoublay"],
        ["1936", "Base aérienne 107 Villacoublay"],
        ["1940-1944", "Occupation et bombardements"],
        ["1952", "Croix de guerre"],
        ["1962", "1ers grands ensembles"],
        ["1972", "Centre commercial Vélizy 2"],
        ["1991", "Création IUT"],
        ["2002", "Centre culturel 'l'Onde'"],
        ["2014", "Tramway T6"]
    ]
    
    hist_table = Table(dates_histoire, colWidths=[3*cm, 12*cm])
    hist_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.whitesmoke])
    ]))
    story.append(hist_table)
    story.append(Spacer(1, 0.25*inch))
    
    # Économie
    story.append(Paragraph("ÉCONOMIE", custom_styles['SectionTitle']))
    
    story.append(Paragraph("Inovel Parc", custom_styles['SubSection']))
    story.append(Paragraph("• 1 000 entreprises", custom_styles['BulletPoint']))
    story.append(Paragraph("• 45 000 salariés", custom_styles['BulletPoint']))
    story.append(Paragraph("• Partie du pôle Paris-Saclay", custom_styles['BulletPoint']))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Grandes entreprises", custom_styles['SubSection']))
    
    entreprises = [
        ["Thales", "Aéronautique, défense"],
        ["PSA Peugeot Citroën", "Automobile"],
        ["Dassault Systèmes", "Logiciel 3D"],
        ["Safran", "Aéronautique"],
        ["Oracle", "Informatique"],
        ["BMW/Mini", "Automobile"],
        ["Nokia", "Télécoms"],
        ["Kraft Foods", "Agroalimentaire"],
        ["Eiffage", "BTP"],
        ["Carmat", "Médical"]
    ]
    
    ent_table = Table(entreprises, colWidths=[6*cm, 9*cm])
    ent_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.whitesmoke])
    ]))
    story.append(ent_table)
    
    story.append(PageBreak())
    
    # Éducation et Culture
    story.append(Paragraph("ÉDUCATION & CULTURE", custom_styles['SectionTitle']))
    
    education = [
        ["IUT de Vélizy", "Institut universitaire de technologie (1991)"],
        ["ISTY", "Institut des sciences et techniques des Yvelines (2011)"]
    ]
    
    edu_table = Table(education, colWidths=[5*cm, 10*cm])
    edu_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    story.append(edu_table)
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Équipements culturels", custom_styles['SubSection']))
    story.append(Paragraph("• L'Onde - Centre culturel (2002)", custom_styles['BulletPoint']))
    story.append(Paragraph("• Église Saint-Denis (1674)", custom_styles['BulletPoint']))
    story.append(Paragraph("• Musée des CRS", custom_styles['BulletPoint']))
    story.append(Paragraph("• Westfield Vélizy 2", custom_styles['BulletPoint']))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Personnalités", custom_styles['SubSection']))
    story.append(Paragraph("• Aline Riera - Footballeuse", custom_styles['BulletPoint']))
    story.append(Paragraph("• Bastien Sohet - Rugbyman", custom_styles['BulletPoint']))
    story.append(Paragraph("• Olivier Megaton - Réalisateur", custom_styles['BulletPoint']))
    
    # Conclusion
    story.append(Paragraph("SYNTHÈSE", custom_styles['SectionTitle']))
    
    conclusions = [
        "✓ Ville économique majeure de l'Ouest parisien",
        "✓ Pôle d'emploi avec Inovel Parc (45 000 emplois)",
        "✓ Histoire marquée par l'aéronautique",
        "✓ Croissance démographique exceptionnelle",
        "✓ Excellente accessibilité routière et transports",
        "✓ Enseignement supérieur présent (IUT, ISTY)",
        "✓ Cadre de vie vert avec forêts et espaces verts",
        "✓ Centre commercial régional important",
        "✓ Intégration au pôle scientifique Paris-Saclay",
        "✓ Développement urbain moderne post-1960"
    ]
    
    for concl in conclusions:
        story.append(Paragraph(concl, custom_styles['BulletPoint']))
    
    story.append(Spacer(1, 0.5*inch))
    
    # Source
    story.append(Paragraph("Source: Wikipedia - Données actualisées", 
                          ParagraphStyle(name='Source', fontSize=8, alignment=TA_CENTER, textColor=colors.grey)))
    
    # Générer le PDF
    doc.build(story)
    return filename

def main():
    print("🚀 Génération du PDF final sur Vélizy-Villacoublay...")
    
    output_file = "Velizy_Villacoublay_Informations.pdf"
    
    try:
        result = create_final_pdf(output_file)
        file_size = os.path.getsize(output_file)
        
        print("\n" + "="*50)
        print("✅ PDF GÉNÉRÉ AVEC SUCCÈS !")
        print("="*50)
        print(f"📄 Fichier : {result}")
        print(f"📏 Taille : {file_size:,} octets")
        print(f"📍 Contenu : Informations complètes sur Vélizy-Villacoublay")
        print(f"📚 Source : Données Wikipedia structurées")
        print("="*50)
        print("\nLe fichier PDF contient toutes les informations demandées :")
        print("• Présentation générale de la commune")
        print("• Géographie et environnement")
        print("• Urbanisme et transports")
        print("• Histoire et développement")
        print("• Économie et entreprises")
        print("• Éducation et culture")
        print("• Synthèse des points clés")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    main()