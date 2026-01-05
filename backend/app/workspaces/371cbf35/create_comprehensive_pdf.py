#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer un PDF complet et professionnel sur Vélizy-Villacoublay
avec des informations détaillées issues de Wikipedia
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
import os
from datetime import datetime
import textwrap

def create_comprehensive_pdf(filename='Velizy_Villacoublay_Complete.pdf'):
    """Créer un PDF complet sur Vélizy-Villacoublay"""
    
    # Créer le document PDF
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        title='Vélizy-Villacoublay - Fiche Complète',
        author='Informations Wikipedia',
        subject='Dossier complet sur la commune de Vélizy-Villacoublay'
    )
    
    # Récupérer les styles par défaut
    styles = getSampleStyleSheet()
    
    # Définir des styles personnalisés
    styles.add(ParagraphStyle(
        name='MainTitle',
        parent=styles['Title'],
        fontSize=22,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='SectionTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=12,
        textColor=colors.navy,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='SubSection',
        parent=styles['Heading2'],
        fontSize=12,
        spaceBefore=10,
        spaceAfter=6,
        textColor=colors.darkblue,
        fontName='Helvetica'
    ))
    
    styles.add(ParagraphStyle(
        name='BodyText',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    ))
    
    styles.add(ParagraphStyle(
        name='BulletText',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=3,
        leftIndent=10,
        firstLineIndent=-10,
        alignment=TA_LEFT,
        fontName='Helvetica'
    ))
    
    styles.add(ParagraphStyle(
        name='TableHeader',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        textColor=colors.white
    ))
    
    # Contenu du PDF
    story = []
    
    # Page de titre
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("VÉLIZY-VILLACOUBLAY", styles['MainTitle']))
    story.append(Paragraph("Commune du département des Yvelines", styles['SectionTitle']))
    story.append(Paragraph("Région Île-de-France", styles['SubSection']))
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("Fiche d'information complète", styles['BodyText']))
    story.append(Paragraph("basée sur les données Wikipedia", styles['BodyText']))
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y')}", 
                          ParagraphStyle(name='Date', fontSize=10, alignment=TA_CENTER)))
    
    story.append(PageBreak())
    
    # Table des matières
    story.append(Paragraph("TABLE DES MATIÈRES", styles['SectionTitle']))
    story.append(Spacer(1, 0.5*inch))
    
    toc_items = [
        "1. Présentation générale",
        "2. Géographie et environnement",
        "3. Urbanisme et logement",
        "4. Transports et déplacements",
        "5. Histoire de la commune",
        "6. Politique et administration",
        "7. Démographie",
        "8. Économie et entreprises",
        "9. Éducation et culture",
        "10. Patrimoine et infrastructures",
        "11. Points clés"
    ]
    
    for item in toc_items:
        story.append(Paragraph(f"• {item}", styles['BulletText']))
    
    story.append(PageBreak())
    
    # 1. Présentation générale
    story.append(Paragraph("1. PRÉSENTATION GÉNÉRALE", styles['SectionTitle']))
    
    general_info = [
        ["Nom complet", "Vélizy-Villacoublay"],
        ["Département", "Yvelines (78)"],
        ["Région", "Île-de-France"],
        ["Code postal", "78140"],
        ["Gentilé", "Véliziens (Véliziennes)"],
        ["Population (2023)", "23 011 habitants"],
        ["Superficie", "893 hectares (8,93 km²)"],
        ["Altitude", "102 à 179 mètres"],
        ["Intercommunalité", "Versailles Grand Parc (depuis 2016)"],
        ["Maire actuel", "Pascal Thévenot (depuis 2014)"]
    ]
    
    gen_table = Table(general_info, colWidths=[5*cm, 10*cm])
    gen_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0, 0), (0, -1), colors.aliceblue),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.whitesmoke])
    ]))
    story.append(gen_table)
    story.append(Spacer(1, 0.25*inch))
    
    story.append(Paragraph("Localisation", styles['SubSection']))
    story.append(Paragraph("Vélizy-Villacoublay est une commune française située à trois kilomètres à l'est de Versailles. Ville industrielle, elle accueille de nombreux sièges sociaux d'entreprise et constitue la partie nord du pôle scientifique et technologique Paris-Saclay.", styles['BodyText']))
    story.append(Paragraph("La commune est située à 9 kilomètres de la Porte de Saint-Cloud du boulevard périphérique parisien, et à 3,5 kilomètres à l'est de Versailles.", styles['BodyText']))
    story.append(Spacer(1, 0.25*inch))
    
    # 2. Géographie et environnement
    story.append(Paragraph("2. GÉOGRAPHIE ET ENVIRONNEMENT", styles['SectionTitle']))
    
    story.append(Paragraph("Géologie et relief", styles['SubSection']))
    story.append(Paragraph("La commune est située sur un plateau dominant Paris et bénéficie d'une altitude privilégiée (102-179 m), ce qui lui permet de ne pas ou peu souffrir des inondations lors des fortes pluies.", styles['BodyText']))
    
    env_data = [
        ["Surface forestière", "313 hectares (forêt domaniale de Meudon)"],
        ["Espaces verts aménagés", "Plus de 65 hectares"],
        ["Climat", "Océanique dégradé des plaines du Centre et du Nord"],
        ["Étude climatique", "CNRS - période 1971-2000"]
    ]
    
    env_table = Table(env_data, colWidths=[6*cm, 9*cm])
    env_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0, 0), (0, -1), colors.aliceblue),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6)
    ]))
    story.append(env_table)
    story.append(Spacer(1, 0.25*inch))
    
    # 3. Urbanisme et logement
    story.append(Paragraph("3. URBANISME ET LOGEMENT", styles['SectionTitle']))
    
    story.append(Paragraph("Typologie urbaine (Insee 2022)", styles['SubSection']))
    story.append(Paragraph("• Grand centre urbain", styles['BulletText']))
    story.append(Paragraph("• Appartient à l'unité urbaine de Paris", styles['BulletText']))
    story.append(Paragraph("• Fait partie de l'aire d'attraction de Paris (pôle principal)", styles['BulletText']))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Occupation des sols (2018)", styles['SubSection']))
    
    occupation = [
        ["Type d'occupation", "Pourcentage", "Surface"],
        ["Forêts de feuillus", "34,1%", "306 ha"],
        ["Zones industrielles/commerciales", "27,3%", "245 ha"],
        ["Tissu urbain discontinu", "20,5%", "184 ha"],
        ["Aéroports", "13,2%", "118 ha"],
        ["Réseaux routiers/ferroviaires", "3,7%", "33 ha"],
        ["Équipements sportifs/loisirs", "1,2%", "11 ha"]
    ]
    
    occ_table = Table(occupation, colWidths=[7*cm, 3*cm, 4*cm])
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
    story.append(Paragraph("Quartiers résidentiels", styles['SubSection']))
    quartiers = ["Mozart", "Le Clos", "Le Mail (avec Pointe Ouest)", "Le Village", 
                 "Est (avec Louvois et Europe)", "Vélizy-Bas (avec l'Ursine et le Bocage)"]
    for q in quartiers:
        story.append(Paragraph(f"• {q}", styles['BulletText']))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Logement (2009)", styles['SubSection']))
    story.append(Paragraph("• Total logements : 8 856", styles['BulletText']))
    story.append(Paragraph("• Résidences principales : 94,5%", styles['BulletText']))
    story.append(Paragraph("• Maisons individuelles : 17,9%", styles['BulletText']))
    story.append(Paragraph("• Appartements : 81,2%", styles['BulletText']))
    
    story.append(PageBreak())
    
    # 4. Transports et déplacements
    story.append(Paragraph("4. TRANSPORTS ET DÉPLACEMENTS", styles['SectionTitle']))
    
    story.append(Paragraph("Voies routières", styles['SubSection']))
    story.append(Paragraph("• A86, RN 118, RN 12", styles['BulletText']))
    story.append(Paragraph("• 15 km de Paris intra-muros", styles['BulletText']))
    story.append(Paragraph("• 15 minutes en voiture via N118", styles['BulletText']))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Transports en commun", styles['SubSection']))
    
    transports = [
        ["Type", "Détails"],
        ["RER", "C - Gare de Chaville-Vélizy (sur Viroflay)"],
        ["Tramway", "T6 - 7 stations sur la commune (depuis 2014)"],
        ["Bus RATP", "Lignes 179, 190, 291, 390"],
        ["Bus Paris-Saclay", "4615, 9108, 9160"],
        ["Bus Vélizy Vallées", "16 lignes différentes"],
        ["Noctilien", "N66 - Service nocturne"]
    ]
    
    trans_table = Table(transports, colWidths=[4*cm, 11*cm])
    trans_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke])
    ]))
    story.append(trans_table)
    story.append(Spacer(1, 0.25*inch))
    
    # 5. Histoire de la commune
    story.append(Paragraph("5. HISTOIRE DE LA COMMUNE", styles['SectionTitle']))
    
    histoire = [
        ["Période", "Événement"],
        ["XIe siècle", "Trois seigneuries : Vélizy, Villacoublay, Ursine"],
        ["1er juillet 1815", "Victoire du général Exelmans contre les Prussiens"],
        ["1934", "Création de l'armée de l'air française"],
        ["1936", "Base aérienne 107 Villacoublay"],
        ["29 mai 1937", "Fusion Vélizy-Villacoublay"],
        ["3 juin 1940", "Bombardement allemand de la base"],
        ["14 juin 1940", "Occupation allemande"],
        ["24 août 1943", "Bombardement américain neutralise la piste"],
        ["23 août 1944", "Libération par les forces alliées"],
        ["1952", "Citation à l'ordre de la Nation - Croix de guerre"],
        ["1962", "Construction premiers grands ensembles (2 000 logements)"],
        ["1972", "Ouverture centre commercial Vélizy 2"],
        ["1991", "Création IUT de Vélizy"],
        ["2002", "Ouverture centre culturel \"l'Onde\""],
        ["2014", "Mise en service tramway T6"]
    ]
    
    hist_table = Table(histoire, colWidths=[3.5*cm, 11.5*cm])
    hist_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke])
    ]))
    story.append(hist_table)
    
    story.append(PageBreak())
    
    # 6. Politique et administration
    story.append(Paragraph("6. POLITIQUE ET ADMINISTRATION", styles['SectionTitle']))
    
    story.append(Paragraph("Maires successifs (depuis 1953)", styles['SubSection']))
    
    maires = [
        ["Période", "Maire", "Parti"],
        ["1953-1988", "Robert Wagner", "UNR/UDR/RPR"],
        ["1988-1990", "Antoine Trani", "RPR"],
        ["1990-2004", "Raymond Loisel", "RPR/UMP"],
        ["2004-2014", "Joël Loison", "UMP"],
        ["2014-", "Pascal Thévenot", "UMP/LR/Soyons libres"]
    ]
    
    maires_table = Table(maires, colWidths=[4*cm, 5*cm, 6*cm])
    maires_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke])
    ]))
    story.append(maires_table)
    story.append(Spacer(1, 0.25*inch))
    
    story.append(Paragraph("Intercommunalité", styles['SubSection']))
    story.append(Paragraph("• Depuis le 1er janvier 2016 : Versailles Grand Parc", styles['BulletText']))
    story.append(Paragraph("• 2014-2015 : Grand Paris Seine Ouest (GPSO)", styles['BulletText']))
    story.append(Paragraph("• Avant 2014 : Communauté d'agglomération Versailles Grand Parc", styles['BulletText']))
    
    story.append(Spacer(1, 0.25*inch))
    
    # 7. Démographie
    story.append(Paragraph("7. DÉMOGRAPHIE", styles['SectionTitle']))
    
    story.append(Paragraph("Évolution démographique", styles['SubSection']))
    
    demographie = [
        ["Année", "Population"],
        ["1793", "168"],
        ["1921", "1 487"],
        ["1936", "4 175"],
        ["1962", "6 402"],
        ["1968", "15 471"],
        ["1975", "22 611 (pic)"],
        ["1990", "20 725"],
        ["2000", "20 342"],
        ["2010", "20 711"],
        ["2020", "22 713"],
        ["2023", "23 011"]
    ]
    
    demo_table = Table(demographie, colWidths=[3*cm, 3*cm])
    demo_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke])
    ]))
    story.append(demo_table)
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Structure par âge (2018)", styles['SubSection']))
    story.append(Paragraph("• Taux < 30 ans : 38,6% (moyenne départementale : 38%)", styles['BulletText']))
    story.append(Paragraph("• Hommes : 11 330 (50,02%)", styles['BulletText']))
    story.append(Paragraph("• Femmes : 11 319 (49,98%)", styles['BulletText']))
    story.append(Paragraph("• Répartition équilibrée hommes/femmes", styles['BulletText']))
    
    story.append(PageBreak())
    
    # 8. Économie et entreprises
    story.append(Paragraph("8. ÉCONOMIE ET ENTREPRISES", styles['SectionTitle']))
    
    story.append(Paragraph("Indicateurs économiques", styles['SubSection']))
    story.append(Paragraph("• Revenu fiscal médian 2010 : 39 599 €", styles['BulletText']))
    story.append(Paragraph("• Revenu médian disponible 2021 : 28 610 €/UC", styles['BulletText']))
    story.append(Paragraph("• Taux d'activité 2009 : 78,4%", styles['BulletText']))
    story.append(Paragraph("• Taux d'emploi : 73,9%", styles['BulletText']))
    story.append(Paragraph("• Taux de chômage : 4,6%", styles['BulletText']))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Grandes entreprises présentes", styles['SubSection']))
    
    entreprises = [
        ["Secteur", "Principales entreprises"],
        ["Aéronautique", "Thales, Safran Landing Systems"],
        ["Automobile", "PSA Peugeot Citroën, Renault Trucks, Porsche, BMW, Audi"],
        ["Télécoms", "Thales, Nokia, Bouygues Telecom, Ekinops"],
        ["Logiciel", "Dassault Systèmes, Oracle, Capgemini Engineering"],
        ["Agroalimentaire", "Kraft Foods"],
        ["BTP", "Eiffage"],
        ["Technologie", "Carmat (cœurs artificiels)"],
        ["Services", "Steria, LGM"],
        ["Logistique", "Jungheinrich"]
    ]
    
    ent_table = Table(entreprises, colWidths=[4*cm, 11*cm])
    ent_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke])
    ]))
    story.append(ent_table)
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Inovel Parc", styles['SubSection']))
    story.append(Paragraph("Pôle d'affaires majeur de l'Ouest parisien :", styles['BodyText']))
    story.append(Paragraph("• 1 000 entreprises", styles['BulletText']))
    story.append(Paragraph("• 45 000 salariés", styles['BulletText']))
    story.append(Paragraph("• Partie du pôle Paris-Saclay", styles['BulletText']))
    story.append(Paragraph("• Forte concentration d'entreprises high-tech", styles['BulletText']))
    
    story.append(Spacer(1, 0.25*inch))
    
    # 9. Éducation et culture
    story.append(Paragraph("9. ÉDUCATION ET CULTURE", styles['SectionTitle']))
    
    story.append(Paragraph("Enseignement supérieur", styles['SubSection']))
    story.append(Paragraph("• Institut universitaire de technologie (IUT) de Vélizy (créé 1991)", styles['BulletText']))
    story.append(Paragraph("• Institut des sciences et techniques des Yvelines (ISTY) (implanté 2011)", styles['BulletText']))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Équipements culturels", styles['SubSection']))
    story.append(Paragraph("• Centre culturel \"l'Onde\" (arch. Claude Vasconi, 2002)", styles['BulletText']))
    story.append(Paragraph("• Église Saint-Denis (transférée d'Ursine en 1674)", styles['BulletText']))
    story.append(Paragraph("• Église Saint-Jean-Baptiste (style moderne)", styles['BulletText']))
    story.append(Paragraph("• Musée des CRS", styles['BulletText']))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Personnalités liées", styles['SubSection']))
    story.append(Paragraph("• Aline Riera (footballeuse, née 1972)", styles['BulletText']))
    story.append(Paragraph("• Bastien Sohet (rugbyman, né 1986)", styles['BulletText']))
    story.append(Paragraph("• Mayada Gargouri (auteur BD, née 1988)", styles['BulletText']))
    story.append(Paragraph("• Olivier Megaton (réalisateur, né 1965)", styles['BulletText']))
    
    story.append(PageBreak())
    
    # 10. Patrimoine et infrastructures
    story.append(Paragraph("10. PATRIMOINE ET INFRASTRUCTURES", styles['SectionTitle']))
    
    story.append(Paragraph("Base aérienne 107 Villacoublay", styles['SubSection']))
    story.append(Paragraph("• Rôle historique important pendant la Seconde Guerre mondiale", styles['BulletText']))
    story.append(Paragraph("• Cible de plusieurs bombardements (1940-1944)", styles['BulletText']))
    story.append(Paragraph("• Aujourd'hui intégrée au tissu économique local", styles['BulletText']))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Centres commerciaux", styles['SubSection']))
    story.append(Paragraph("• Westfield Vélizy 2 (ouvert 1972, rénové)", styles['BulletText']))
    story.append(Paragraph("• L'Usine mode et maison", styles['BulletText']))
    story.append(Paragraph("• Art de vivre", styles['BulletText']))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Autres infrastructures", styles['SubSection']))
    story.append(Paragraph("• Caserne des CRS (1965)", styles['BulletText']))
    story.append(Paragraph("• Nombreux équipements sportifs", styles['BulletText']))
    story.append(Paragraph("• Espaces verts et forestiers importants", styles['BulletText']))
    
    story.append(Spacer(1, 0.25*inch))
    
    # 11. Points clés à retenir
    story.append(Paragraph("11. POINTS CLÉS À RETENIR", styles['SectionTitle']))
    
    key_points = [
        "1. Ville industrielle et tertiaire majeure de l'Ouest parisien",
        "2. Pôle économique Inovel Parc avec 45 000 emplois",
        "3. Histoire aéronautique marquée par la base 107 Villacoublay",
        "4. Croissance démographique spectaculaire (x137 depuis 1793)",
        "5. Excellente desserte transports (autoroutes, RER, tramway, bus)",
        "6. Présence d'établissements d'enseignement supérieur",
        "7. Cadre de vie vert avec 313 ha de forêt",
        "8. Centre commercial régional Westfield Vélizy 2",
        "9. Intégration au pôle scientifique Paris-Saclay",
        "10. Développement urbain principalement post-1960"
    ]
    
    for i, point in enumerate(key_points):
        story.append(Paragraph(point, styles['BulletText']))
    
    story.append(Spacer(1, 0.5*inch))
    
    # Pied de page final
    footer_text = "Source : Wikipedia - Données actualisées - Généré automatiquement"
    story.append(Paragraph(footer_text, 
                          ParagraphStyle(name='Footer', fontSize=8, textColor=colors.grey, alignment=TA_CENTER)))
    
    # Générer le PDF
    try:
        doc.build(story)
        print(f"✅ PDF généré avec succès : {filename}")
        print(f"📄 Taille : {os.path.getsize(filename):,} octets")
        print(f"📊 Pages : Estimation 6-8 pages")
        return filename
    except Exception as e:
        print(f"❌ Erreur lors de la génération : {e}")
        return None

def main():
    """Fonction principale"""
    print("=" * 60)
    print("GÉNÉRATION DU PDF SUR VÉLIZY-VILLACOUBLAY")
    print("=" * 60)
    
    pdf_file = "Velizy_Villacoublay_Fiche_Complete.pdf"
    
    print("📋 Collecte des informations...")
    print("📊 Structuration des données...")
    print("🖨️  Génération du PDF...")
    
    result = create_comprehensive_pdf(pdf_file)
    
    if result:
        print("=" * 60)
        print("✅ MISSION ACCOMPLIE !")
        print("=" * 60)
        print(f"Le fichier PDF '{result}' a été généré avec succès.")
        print("Il contient toutes les informations structurées sur Vélizy-Villacoublay.")
        print("=" * 60)
    else:
        print("❌ Échec de la génération du PDF.")

if __name__ == "__main__":
    main()