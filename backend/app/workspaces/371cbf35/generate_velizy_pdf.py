#!/usr/bin/env python3
# Script pour générer un PDF avec les informations Wikipedia sur Vélizy-Villacoublay

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from datetime import datetime
import textwrap

def create_pdf():
    """Crée un PDF avec les informations sur Vélizy-Villacoublay"""
    
    # Nom du fichier de sortie
    output_filename = "Vélizy-Villacoublay_Wikipedia.pdf"
    
    # Création du document
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Liste pour contenir les éléments du document
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Style pour le titre principal
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Style pour les sous-titres
    heading1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1E40AF'),
        spaceBefore=20,
        spaceAfter=10
    )
    
    heading2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#3B82F6'),
        spaceBefore=15,
        spaceAfter=8
    )
    
    # Style pour le texte normal
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=TA_JUSTIFY
    )
    
    # Style pour les dates
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.gray,
        alignment=TA_CENTER
    )
    
    # Titre principal
    story.append(Paragraph("Vélizy-Villacoublay", title_style))
    story.append(Paragraph(f"Informations Wikipedia - Généré le {datetime.now().strftime('%d/%m/%Y')}", date_style))
    story.append(Spacer(1, 20))
    
    # Introduction
    intro_text = """
    Vélizy-Villacoublay est une commune française située dans le département des Yvelines 
    en région Île-de-France, à trois kilomètres à l'est de Versailles. Ville industrielle, 
    accueillant de nombreux sièges sociaux d'entreprise, elle constitue la partie nord 
    du pôle scientifique et technologique Paris-Saclay, en cours d'aménagement depuis 2010.
    
    Depuis le 1er janvier 2016, elle fait partie de Versailles Grand Parc. 
    Ses habitants sont appelés les Véliziens.
    """
    story.append(Paragraph("Introduction", heading1_style))
    story.append(Paragraph(intro_text, normal_style))
    
    # Page break pour la structure
    story.append(PageBreak())
    
    # Géographie
    story.append(Paragraph("Géographie", heading1_style))
    
    # Localisation
    localisation_text = """
    La commune est située à 9 kilomètres de la Porte de Saint-Cloud du boulevard 
    périphérique parisien, et à 3,5 kilomètres à l'est de Versailles.
    
    La superficie de la commune est de 893 hectares ; l'altitude varie entre 102 et 179 mètres.
    La commune est située sur un plateau dominant Paris et bénéficie donc d'une altitude 
    privilégiée, ce qui lui permet de ne pas ou peu souffrir des possibles inondations 
    lors des fortes pluies.
    """
    story.append(Paragraph("Localisation", heading2_style))
    story.append(Paragraph(localisation_text, normal_style))
    
    # Environnement
    environnement_text = """
    Environ 313 hectares de forêt domaniale (domaine forestier de Meudon) couvrent 
    une partie du territoire de la commune et offrent aux Véliziens de grands espaces 
    de verdure naturels. De plus Vélizy possède plus de 65 hectares d'espaces verts.
    """
    story.append(Paragraph("Environnement", heading2_style))
    story.append(Paragraph(environnement_text, normal_style))
    
    # Climat
    climat_text = """
    En 2010, le climat de la commune était ainsi de type climat océanique dégradé 
    des plaines du Centre et du Nord, selon une étude du CNRS s'appuyant sur une 
    méthode combinant données climatiques et facteurs de milieu (topographie, 
    occupation des sols, etc.) et des données couvrant la période 1971-2000.
    """
    story.append(Paragraph("Climat", heading2_style))
    story.append(Paragraph(climat_text, normal_style))
    
    # Page break pour continuer
    story.append(PageBreak())
    
    # Transports
    story.append(Paragraph("Voies de communications et transports", heading1_style))
    
    transports_text = """
    Vélizy se situe à une quinzaine de kilomètres de Paris intra-muros et à une 
    quinzaine de minutes de trajet en voiture en passant par la N118. 
    La commune est desservie par l'A86, par la RN 118 et la RN 12.
    
    **Transports en commun :**
    - Le RER C à la gare de Chaville - Vélizy
    - Le Tramway T6 (7 stations sur la commune)
    - Plusieurs lignes de bus RATP
    - Ligne N66 (Noctilien) pour les déplacements nocturnes
    """
    story.append(Paragraph(transports_text, normal_style))
    
    # Urbanisme
    story.append(Paragraph("Urbanisme", heading1_style))
    
    urbanisme_text = """
    Au 1er janvier 2024, Vélizy-Villacoublay est catégorisée grand centre urbain.
    Elle appartient à l'unité urbaine de Paris, une agglomération inter-départementale 
    regroupant 407 communes, dont elle est une commune de la banlieue.
    """
    story.append(Paragraph(urbanisme_text, normal_style))
    
    # Quartiers
    quartiers_text = """
    **Quartiers d'habitation :**
    1. Mozart
    2. Le Clos
    3. Le Mail (avec Pointe Ouest)
    4. Le Village
    5. Est (avec Louvois et Europe)
    6. Vélizy - Bas (avec l'Ursine et le Bocage)
    """
    story.append(Paragraph("Quartiers", heading2_style))
    story.append(Paragraph(quartiers_text, normal_style))
    
    # Page break
    story.append(PageBreak())
    
    # Histoire
    story.append(Paragraph("Histoire", heading1_style))
    
    # Dates importantes
    dates_historiques = [
        ["Période", "Événement"],
        ["Ancien Régime", "Vélizy n'était qu'un simple hameau du village d'Ursine"],
        ["1er juillet 1815", "Le général Exelmans défait les Prussiens à Vélizy"],
        ["1936", "L'aérodrome devient base aérienne 107 Villacoublay"],
        ["29 mai 1937", "La commune prend le nom de Vélizy-Villacoublay"],
        ["Seconde Guerre mondiale", "Base bombardée plusieurs fois"],
        ["23 août 1944", "Libération de Vélizy par les Alliés"],
        ["1952", "Citation à l'ordre de la Nation et Croix de guerre"],
        ["1972", "Ouverture du centre commercial Vélizy 2"],
        ["1991", "Création de l'IUT de Vélizy"],
        ["2002", "Inauguration du centre culturel 'l'Onde'"],
        ["13 décembre 2014", "Mise en service du tramway T6"]
    ]
    
    # Création de la table historique
    history_table = Table(dates_historiques, colWidths=[2.5*cm, 12*cm])
    history_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F3F4F6')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D1D5DB')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(history_table)
    story.append(Spacer(1, 20))
    
    # Politique et administration
    story.append(Paragraph("Politique et administration", heading1_style))
    
    maires_data = [
        ["Période", "Maire", "Parti"],
        ["1953-1988", "Robert Wagner", "UNR/UDR/RPR"],
        ["1988-1990", "Antoine Trani", "RPR"],
        ["1990-2004", "Raymond Loisel", "RPR/UMP"],
        ["2004-2014", "Joël Loison", "UMP"],
        ["2014-en cours", "Pascal Thévenot", "LR/Soyons libres"]
    ]
    
    maires_table = Table(maires_data, colWidths=[3*cm, 5*cm, 4*cm])
    maires_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E40AF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#EFF6FF')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#93C5FD')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(Paragraph("Liste des maires", heading2_style))
    story.append(maires_table)
    story.append(Spacer(1, 20))
    
    # Page break
    story.append(PageBreak())
    
    # Démographie
    story.append(Paragraph("Démographie", heading1_style))
    
    demographie_text = """
    En 2023, la commune comptait 23 011 habitants.
    
    **Évolution démographique marquante :**
    - 1793 : 168 habitants
    - 1921 : 1 487 habitants
    - 1936 : 4 175 habitants
    - 1975 : 22 611 habitants (pic démographique)
    - 2023 : 23 011 habitants
    """
    story.append(Paragraph(demographie_text, normal_style))
    
    # Données démographiques récentes
    donnees_demo = [
        ["Année", "Population"],
        ["1999", "20 342"],
        ["2006", "20 030"],
        ["2011", "20 711"],
        ["2016", "21 517"],
        ["2021", "22 713"],
        ["2023", "23 011"]
    ]
    
    demo_table = Table(donnees_demo, colWidths=[3*cm, 4*cm])
    demo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10B981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#D1FAE5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#34D399')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(demo_table)
    story.append(Spacer(1, 20))
    
    # Structure par âge
    structure_age = """
    **Structure par âge (2018) :**
    - Taux de personnes < 30 ans : 38,6% (au-dessus de la moyenne départementale de 38%)
    - Population : 11 330 hommes / 11 319 femmes
    - Taux d'hommes : 50,02% (légèrement supérieur au département : 48,68%)
    """
    story.append(Paragraph(structure_age, normal_style))
    
    # Économie
    story.append(Paragraph("Économie", heading1_style))
    
    # Revenus
    revenus_text = """
    **Revenus :**
    - 2010 : Revenu fiscal médian par ménage = 39 599 €
    - 2021 : Revenu médian disponible par UC = 28 610 €
    
    **Emploi (2009) :**
    - Population active (15-64 ans) : 17 056 personnes
    - Taux d'activité : 78,4%
    - Taux d'emploi : 73,9%
    - Taux de chômage : 4,6%
    """
    story.append(Paragraph(revenus_text, normal_style))
    
    # Entreprises
    entreprises_text = """
    **Entreprises (décembre 2010) :**
    - Total établissements : 1 898
    - Agriculture : 3
    - Industrie : 88
    - Construction : 141
    - Commerce/transports/services : 1 459
    - Secteur administratif : 207
    """
    story.append(Paragraph(entreprises_text, normal_style))
    
    # Principales entreprises
    entreprises_principales = [
        ["Secteur", "Entreprises"],
        ["Aéronautique", "Thales, Safran Landing Systems"],
        ["Transport", "Thales, Schindler"],
        ["Automobile", "PSA, Renault Trucks, Porsche, BMW, Audi"],
        ["BTP", "Eiffage"],
        ["Logiciels", "Dassault Systèmes, Oracle, Capgemini"],
        ["Télécoms", "Ekinops, Thales, Nokia, Bouygues Telecom"],
        ["Logistique", "Jungheinrich"]
    ]
    
    ent_table = Table(entreprises_principales, colWidths=[4*cm, 10*cm])
    ent_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F59E0B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FEF3C7')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#FBBF24')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(Paragraph("Principales entreprises", heading2_style))
    story.append(ent_table)
    
    # Page break
    story.append(PageBreak())
    
    # Inovel Parc
    inovel_text = """
    **Inovel Parc :**
    En parallèle à l'aménagement des quartiers d'habitation, la ville accueille 
    le pôle d'affaires d'envergure Inovel Parc. Il représente une des plus fortes 
    concentrations d'entreprises de l'Ouest parisien.
    
    **Chiffres clés :**
    - Environ 1 000 entreprises
    - Plus de 45 000 salariés
    - Pôle majeur du pôle scientifique et technologique Paris-Saclay
    """
    story.append(Paragraph("Inovel Parc - Pôle économique", heading2_style))
    story.append(Paragraph(inovel_text, normal_style))
    
    # Culture et patrimoine
    story.append(Paragraph("Culture locale et patrimoine", heading1_style))
    
    culture_text = """
    **Lieux et monuments :**
    - Église Saint-Denis (transférée d'Ursine en 1674)
    - Église Saint-Jean-Baptiste (style moderne)
    - Caserne de CRS
    - Musée des CRS
    - Centre culturel "l'Onde" (conçu par Claude Vasconi)
    """
    story.append(Paragraph(culture_text, normal_style))
    
    # Personnalités
    personnalites_text = """
    **Personnalités liées à la commune :**
    - Aline Riera (née en 1972) : ancienne footballeuse française
    - Bastien Sohet (né en 1986) : rugbyman français
    - Mayada Gargouri (née en 1988) : auteur de bande dessinée française
    - Olivier Megaton (né en 1965) : grapheur, graphiste, réalisateur
    """
    story.append(Paragraph("Personnalités", heading2_style))
    story.append(Paragraph(personnalites_text, normal_style))
    
    # Héraldique
    heraldique_text = """
    **Héraldique :**
    Blason défini en 1943 par la commission héraldique de la préfecture de Seine-et-Oise.
    
    **Description :**
    D'azur à deux vols d'argent en forme de V posés l'un au-dessus de l'autre, 
    accompagnés en chef d'une étoile et en pointe de deux quintefeuilles et entre 
    chacun des vols, de deux épis de blé tigés et feuillés posés l'un en bande, 
    l'autre en barre, le tout d'or.
    """
    story.append(Paragraph("Héraldique", heading2_style))
    story.append(Paragraph(heraldique_text, normal_style))
    
    # Conclusion
    story.append(Spacer(1, 30))
    conclusion_text = """
    **Conclusion :**
    Vélizy-Villacoublay est une commune dynamique de la banlieue parisienne, 
    alliant développement économique avec Inovel Parc et qualité de vie avec 
    ses espaces verts. Sa position stratégique dans le pôle Paris-Saclay et 
    sa bonne desserte en transports en font une ville attractive pour les 
    entreprises et les habitants.
    """
    story.append(Paragraph(conclusion_text, normal_style))
    
    # Pied de page
    story.append(Spacer(1, 40))
    footer_text = f"""
    Source : Wikipedia - Données mises à jour en 2024
    Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}
    """
    story.append(Paragraph(footer_text, date_style))
    
    # Génération du PDF
    doc.build(story)
    print(f"PDF généré avec succès : {output_filename}")
    return output_filename

if __name__ == "__main__":
    try:
        pdf_file = create_pdf()
        print("Le fichier PDF a été créé avec succès !")
        print(f"Nom du fichier : {pdf_file}")
    except Exception as e:
        print(f"Erreur lors de la génération du PDF : {e}")
        import traceback
        traceback.print_exc()