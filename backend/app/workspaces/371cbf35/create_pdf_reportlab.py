#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer un PDF professionnel sur Vélizy-Villacoublay
Utilisation de ReportLab pour une mise en forme avancée
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import os
from datetime import datetime

# Définir les données structurées pour le PDF
PDF_INFO = {
    'title': 'Vélizy-Villacoublay - Informations Complètes',
    'author': 'Système d\'Information',
    'subject': 'Informations sur la commune de Vélizy-Villacoublay',
    'keywords': 'Vélizy-Villacoublay, Yvelines, Île-de-France, France'
}

def create_pdf(filename='velizy_villacoublay_rapport.pdf'):
    """Créer un PDF professionnel sur Vélizy-Villacoublay"""
    
    # Créer le document PDF
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        title=PDF_INFO['title'],
        author=PDF_INFO['author']
    )
    
    # Récupérer les styles par défaut
    styles = getSampleStyleSheet()
    
    # Définir des styles personnalisés
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Title'],
        fontSize=18,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    ))
    
    styles.add(ParagraphStyle(
        name='CustomHeading1',
        parent=styles['Heading1'],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=10,
        textColor=colors.darkblue
    ))
    
    styles.add(ParagraphStyle(
        name='CustomHeading2',
        parent=styles['Heading2'],
        fontSize=12,
        spaceBefore=10,
        spaceAfter=5,
        textColor=colors.navy
    ))
    
    styles.add(ParagraphStyle(
        name='NormalJustified',
        parent=styles['Normal'],
        alignment=TA_JUSTIFY,
        fontSize=10,
        spaceAfter=5
    ))
    
    # Contenu du PDF
    story = []
    
    # Titre principal
    story.append(Paragraph("Vélizy-Villacoublay", styles['CustomTitle']))
    story.append(Paragraph("Commune française du département des Yvelines", styles['CustomHeading2']))
    story.append(Spacer(1, 0.25*inch))
    
    # Date de génération
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    story.append(Paragraph(f"Rapport généré le : {current_date}", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    
    # 1. Informations générales
    story.append(Paragraph("1. Informations Générales", styles['CustomHeading1']))
    
    info_generales = [
        ["Nom complet", "Vélizy-Villacoublay"],
        ["Département", "Yvelines"],
        ["Région", "Île-de-France"],
        ["Population (2023)", "23 011 habitants"],
        ["Gentilé", "Véliziens"],
        ["Superficie", "893 hectares"],
        ["Intercommunalité", "Versailles Grand Parc (depuis 2016)"],
        ["Code postal", "78140"]
    ]
    
    info_table = Table(info_generales, colWidths=[3*cm, 10*cm])
    info_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
        ('BACKGROUND', (0, 0), (0, -1), colors.aliceblue),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.whitesmoke])
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.25*inch))
    
    # 2. Géographie
    story.append(Paragraph("2. Géographie", styles['CustomHeading1']))
    story.append(Paragraph("Localisation", styles['CustomHeading2']))
    story.append(Paragraph("• Située à 9 km de la Porte de Saint-Cloud (Paris)", styles['NormalJustified']))
    story.append(Paragraph("• À 3,5 km à l'est de Versailles", styles['NormalJustified']))
    story.append(Paragraph("• Altitude: entre 102 et 179 mètres", styles['NormalJustified']))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Caractéristiques physiques", styles['CustomHeading2']))
    story.append(Paragraph("• 313 hectares de forêt domaniale (domaine forestier de Meudon)", styles['NormalJustified']))
    story.append(Paragraph("• Plus de 65 hectares d'espaces verts", styles['NormalJustified']))
    story.append(Paragraph("• Situation sur un plateau dominant Paris (protection contre les inondations)", styles['NormalJustified']))
    story.append(Spacer(1, 0.25*inch))
    
    # 3. Urbanisme
    story.append(Paragraph("3. Urbanisme", styles['CustomHeading1']))
    
    occupation_sols = [
        ["Type d'occupation", "Pourcentage", "Superficie (ha)"],
        ["Tissu urbain discontinu", "20,5%", "184"],
        ["Zones industrielles/commerciales", "27,3%", "245"],
        ["Aéroports", "13,2%", "118"],
        ["Forêts de feuillus", "34,1%", "306"],
        ["Équipements sportifs/loisirs", "1,2%", "11"],
        ["Réseaux routiers/ferroviaires", "3,7%", "33"]
    ]
    
    story.append(Paragraph("Occupation des sols (2018)", styles['CustomHeading2']))
    occupation_table = Table(occupation_sols, colWidths=[6*cm, 3*cm, 4*cm])
    occupation_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke])
    ]))
    story.append(occupation_table)
    story.append(Spacer(1, 0.25*inch))
    
    # 4. Transports
    story.append(Paragraph("4. Transports", styles['CustomHeading1']))
    story.append(Paragraph("Voies routières", styles['CustomHeading2']))
    story.append(Paragraph("• Accès par A86, RN 118, RN 12", styles['NormalJustified']))
    story.append(Paragraph("• 15 km de Paris intra-muros", styles['NormalJustified']))
    story.append(Paragraph("• 15 minutes en voiture via N118", styles['NormalJustified']))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Transports en commun", styles['CustomHeading2']))
    story.append(Paragraph("• RER C: Gare de Chaville - Vélizy (sur Viroflay)", styles['NormalJustified']))
    story.append(Paragraph("• Tramway T6: 7 stations sur la commune", styles['NormalJustified']))
    story.append(Paragraph("• Bus RATP: Lignes 179, 190, 291, 390", styles['NormalJustified']))
    story.append(Paragraph("• Noctilien: Ligne N66 (service de nuit)", styles['NormalJustified']))
    story.append(Spacer(1, 0.25*inch))
    
    # 5. Histoire
    story.append(Paragraph("5. Histoire", styles['CustomHeading1']))
    
    dates_importantes = [
        ["Année", "Événement"],
        ["1815", "Victoire du général Exelmans contre les Prussiens"],
        ["1936", "Base aérienne 107 Villacoublay"],
        ["1937", "Fusion Vélizy-Villacoublay"],
        ["1940-1944", "Occupation allemande et bombardements"],
        ["1952", "Citation à l'ordre de la Nation"],
        ["1962", "Construction premiers grands ensembles"],
        ["1972", "Ouverture centre commercial Vélizy 2"],
        ["1991", "Création IUT de Vélizy"],
        ["2002", "Ouverture centre culturel \"l'Onde\""],
        ["2014", "Mise en service tramway T6"]
    ]
    
    history_table = Table(dates_importantes, colWidths=[2.5*cm, 11.5*cm])
    history_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke])
    ]))
    story.append(history_table)
    story.append(Spacer(1, 0.25*inch))
    
    # 6. Économie
    story.append(Paragraph("6. Économie", styles['CustomHeading1']))
    story.append(Paragraph("Grandes entreprises présentes", styles['CustomHeading2']))
    
    entreprises = [
        ["Secteur", "Entreprises"],
        ["Aéronautique", "Thales, Safran Landing Systems"],
        ["Automobile", "PSA Peugeot Citroën, Renault Trucks, Porsche, BMW/Mini, Audi"],
        ["Télécommunications", "Thales, Nokia France, Bouygues Telecom, Ekinops"],
        ["Logiciel", "Dassault Systèmes, Oracle, Capgemini Engineering"],
        ["Agro-alimentaire", "Kraft Foods"],
        ["BTP", "Eiffage"],
        ["Technologie médicale", "Carmat"],
        ["Services", "Steria, LGM"],
        ["Logistique", "Jungheinrich"]
    ]
    
    entreprises_table = Table(entreprises, colWidths=[4*cm, 10*cm])
    entreprises_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke])
    ]))
    story.append(entreprises_table)
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Inovel Parc", styles['CustomHeading2']))
    story.append(Paragraph("• Environ 1 000 entreprises", styles['NormalJustified']))
    story.append(Paragraph("• Plus de 45 000 salariés", styles['NormalJustified']))
    story.append(Paragraph("• Une des plus fortes concentrations d'entreprises de l'Ouest parisien", styles['NormalJustified']))
    story.append(Paragraph("• Partie du pôle scientifique et technologique Paris-Saclay", styles['NormalJustified']))
    story.append(Spacer(1, 0.25*inch))
    
    # 7. Démographie
    story.append(Paragraph("7. Démographie", styles['CustomHeading1']))
    
    evolution_demo = [
        ["Année", "Population"],
        ["1793", "168"],
        ["1921", "1 487"],
        ["1936", "4 175"],
        ["1968", "15 471"],
        ["1975", "22 611"],
        ["1990", "20 725"],
        ["2000", "20 342"],
        ["2010", "20 711"],
        ["2020", "22 713"],
        ["2023", "23 011"]
    ]
    
    demo_table = Table(evolution_demo, colWidths=[3*cm, 3*cm])
    demo_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke])
    ]))
    story.append(demo_table)
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("Structure par âge (2018)", styles['CustomHeading2']))
    story.append(Paragraph("• Taux < 30 ans: 38,6% (vs 38% départemental)", styles['NormalJustified']))
    story.append(Paragraph("• Hommes: 11 330 (50,02%)", styles['NormalJustified']))
    story.append(Paragraph("• Femmes: 11 319 (49,98%)", styles['NormalJustified']))
    story.append(Spacer(1, 0.25*inch))
    
    # 8. Éducation et Culture
    story.append(Paragraph("8. Éducation et Culture", styles['CustomHeading1']))
    story.append(Paragraph("Enseignement supérieur", styles['CustomHeading2']))
    story.append(Paragraph("• Institut universitaire de technologie (IUT) de Vélizy (créé 1991)", styles['NormalJustified']))
    story.append(Paragraph("• Institut des sciences et techniques des Yvelines (ISTY) (implanté 2011)", styles['NormalJustified']))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Lieux culturels", styles['CustomHeading2']))
    story.append(Paragraph("• Centre culturel \"l'Onde\" (2002)", styles['NormalJustified']))
    story.append(Paragraph("• Église Saint-Denis (1674)", styles['NormalJustified']))
    story.append(Paragraph("• Église Saint-Jean-Baptiste (style moderne)", styles['NormalJustified']))
    story.append(Paragraph("• Musée des CRS", styles['NormalJustified']))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Personnalités liées à la commune", styles['CustomHeading2']))
    story.append(Paragraph("• Aline Riera (née 1972), footballeuse", styles['NormalJustified']))
    story.append(Paragraph("• Bastien Sohet (né 1986), rugbyman", styles['NormalJustified']))
    story.append(Paragraph("• Mayada Gargouri (née 1988), auteur BD", styles['NormalJustified']))
    story.append(Paragraph("• Olivier Megaton (né 1965), réalisateur", styles['NormalJustified']))
    story.append(Spacer(1, 0.25*inch))
    
    # 9. Conclusion
    story.append(Paragraph("9. Points Clés à Retenir", styles['CustomHeading1']))
    
    points_cles = [
        "1. Ville industrielle et tertiaire importante de l'Ouest parisien",
        "2. Pôle économique majeur avec Inovel Parc (45 000 emplois)",
        "3. Histoire aéronautique marquée par la base aérienne 107 Villacoublay",
        "4. Croissance démographique rapide depuis le XXe siècle",
        "5. Excellente desserte en transports (autoroutes, RER, tramway)",
        "6. Présence d'établissements d'enseignement supérieur (IUT, ISTY)",
        "7. Importantes surfaces forestières et espaces verts",
        "8. Centre commercial régional Westfield Vélizy 2",
        "9. Ville moderne développée principalement après 1960",
        "10. Intégration au pôle scientifique Paris-Saclay"
    ]
    
    for point in points_cles:
        story.append(Paragraph(f"• {point}", styles['NormalJustified']))
    
    story.append(Spacer(1, 0.5*inch))
    
    # Pied de page
    story.append(Paragraph("Sources: Wikipedia, INSEE, Données officielles", 
                          ParagraphStyle(name='Footer', fontSize=8, textColor=colors.grey, alignment=TA_CENTER)))
    
    # Générer le PDF
    doc.build(story)
    print(f"PDF généré avec succès : {filename}")
    print(f"Taille du fichier : {os.path.getsize(filename)} octets")
    
    return filename

def main():
    """Fonction principale"""
    try:
        # Installer reportlab si nécessaire
        try:
            import reportlab
        except ImportError:
            print("Installation de ReportLab...")
            import subprocess
            subprocess.check_call(['pip', 'install', 'reportlab'])
            print("ReportLab installé avec succès")
        
        # Nom du fichier PDF
        pdf_filename = "Vélizy-Villacoublay_Rapport.pdf"
        
        # Créer le PDF
        print("Génération du PDF en cours...")
        created_file = create_pdf(pdf_filename)
        
        print("\n" + "="*60)
        print("RAPPORT PDF GÉNÉRÉ AVEC SUCCÈS")
        print("="*60)
        print(f"Fichier : {created_file}")
        print(f"Contenu : Informations complètes sur Vélizy-Villacoublay")
        print(f"Sections : 9 sections détaillées")
        print("="*60)
        
    except Exception as e:
        print(f"Erreur lors de la génération du PDF : {e}")
        return None

if __name__ == "__main__":
    main()