#!/usr/bin/env python3
# Créer un PDF avec fpdf2

from fpdf import FPDF
from datetime import datetime
import os

class PDF(FPDF):
    def header(self):
        # Logo
        # self.image('logo.png', 10, 8, 33)
        # Police
        self.set_font('Helvetica', 'B', 16)
        # Titre
        title = "VÉLIZY-VILLACOUBLAY"
        self.cell(0, 10, title, 0, 1, 'C')
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 10, f"Informations Wikipedia - Généré le {datetime.now().strftime('%d/%m/%Y')}", 0, 1, 'C')
        # Saut de ligne
        self.ln(10)
    
    def footer(self):
        # Position à 1.5 cm du bas
        self.set_y(-15)
        # Police
        self.set_font('Helvetica', 'I', 8)
        # Numéro de page
        page_num = f'Page {self.page_no()}'
        self.cell(0, 10, page_num, 0, 0, 'C')
    
    def chapter_title(self, title):
        # Police
        self.set_font('Helvetica', 'B', 12)
        # Couleur de fond
        self.set_fill_color(200, 220, 255)
        # Titre
        self.cell(0, 6, title, 0, 1, 'L', 1)
        # Saut de ligne
        self.ln(4)
    
    def chapter_body(self, body):
        # Police
        self.set_font('Helvetica', '', 11)
        # Sortie du texte justifié
        self.multi_cell(0, 5, body)
        # Saut de ligne
        self.ln()

def create_pdf():
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Introduction
    pdf.chapter_title("INTRODUCTION")
    intro = """Vélizy-Villacoublay est une commune française située dans le département des Yvelines en région Île-de-France, à trois kilomètres à l'est de Versailles.

Ville industrielle, accueillant de nombreux sièges sociaux d'entreprise, elle constitue la partie nord du pôle scientifique et technologique Paris-Saclay, en cours d'aménagement depuis 2010.

Depuis le 1er janvier 2016, elle fait partie de Versailles Grand Parc. Ses habitants sont appelés les Véliziens."""
    pdf.chapter_body(intro)
    
    # Géographie
    pdf.add_page()
    pdf.chapter_title("GÉOGRAPHIE")
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Localisation", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- Distance de Paris: 9 km de la Porte de Saint-Cloud
- Distance de Versailles: 3,5 km à l'est
- Superficie: 893 hectares
- Altitude: 102 à 179 mètres""")
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Environnement", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- Forêt domaniale de Meudon: 313 hectares
- Espaces verts: plus de 65 hectares""")
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Climat", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, "Climat océanique dégradé des plaines du Centre et du Nord.")
    
    # Transports
    pdf.add_page()
    pdf.chapter_title("TRANSPORTS")
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Voies routières", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, "- A86\n- RN 118\n- RN 12")
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Transports en commun", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- RER C: Gare de Chaville - Vélizy (à Viroflay)
- Tramway T6: 7 stations sur la commune
- Bus RATP: Lignes 179, 190, 291, 390
- Réseau Noctilien: Ligne N66 (nuit)""")
    
    # Urbanisme
    pdf.add_page()
    pdf.chapter_title("URBANISME")
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Quartiers d'habitation", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """1. Mozart
2. Le Clos
3. Le Mail (avec Pointe Ouest)
4. Le Village
5. Est (avec Louvois et Europe)
6. Vélizy - Bas (avec l'Ursine et le Bocage)""")
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Occupation des sols (2018)", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- Tissu urbain discontinu: 20,5% (184 ha)
- Zones industrielles/commerciales: 27,3% (245 ha)
- Réseaux routiers/ferroviaires: 3,7% (33 ha)
- Aéroports: 13,2% (118 ha)
- Équipements sportifs: 1,2% (11 ha)
- Forêts de feuillus: 34,1% (306 ha)""")
    
    # Histoire
    pdf.add_page()
    pdf.chapter_title("HISTOIRE - DATES IMPORTANTES")
    
    dates = [
        ["1er juillet 1815", "Bataille de Vélizy (général Exelmans)"],
        ["1936", "Création de la base aérienne 107 Villacoublay"],
        ["29 mai 1937", "La commune devient Vélizy-Villacoublay"],
        ["Seconde Guerre mondiale", "Base bombardée à plusieurs reprises"],
        ["23 août 1944", "Libération par les Alliés"],
        ["1952", "Citation à l'ordre de la Nation avec Croix de guerre"],
        ["1972", "Ouverture du centre commercial Vélizy 2"],
        ["1991", "Création de l'IUT de Vélizy"],
        ["2002", "Inauguration du centre culturel 'l'Onde'"],
        ["13 décembre 2014", "Mise en service du tramway T6"]
    ]
    
    # Tableau des dates
    col_widths = [40, 140]
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(col_widths[0], 8, "Date", border=1)
    pdf.cell(col_widths[1], 8, "Événement", border=1)
    pdf.ln()
    
    pdf.set_font('Helvetica', '', 10)
    for date, event in dates:
        pdf.cell(col_widths[0], 8, date, border=1)
        pdf.cell(col_widths[1], 8, event, border=1)
        pdf.ln()
    
    # Politique
    pdf.add_page()
    pdf.chapter_title("POLITIQUE ET ADMINISTRATION")
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Liste des maires depuis 1953", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    
    maires = [
        ["1953-1988", "Robert Wagner", "UNR/UDR/RPR"],
        ["1988-1990", "Antoine Trani", "RPR"],
        ["1990-2004", "Raymond Loisel", "RPR/UMP"],
        ["2004-2014", "Joël Loison", "UMP"],
        ["2014-en cours", "Pascal Thévenot", "LR/Soyons libres"]
    ]
    
    col_widths2 = [30, 70, 50]
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(col_widths2[0], 8, "Période", border=1)
    pdf.cell(col_widths2[1], 8, "Maire", border=1)
    pdf.cell(col_widths2[2], 8, "Parti", border=1)
    pdf.ln()
    
    pdf.set_font('Helvetica', '', 10)
    for periode, maire, parti in maires:
        pdf.cell(col_widths2[0], 8, periode, border=1)
        pdf.cell(col_widths2[1], 8, maire, border=1)
        pdf.cell(col_widths2[2], 8, parti, border=1)
        pdf.ln()
    
    pdf.ln(10)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Intercommunalité", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- 2014: Rejoint Grand Paris Seine Ouest (GPSO)
- 2016: Intègre Versailles Grand Parc""")
    
    # Démographie
    pdf.add_page()
    pdf.chapter_title("DÉMOGRAPHIE")
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Évolution démographique", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    
    demo_data = [
        ["1793", "168 habitants"],
        ["1921", "1 487 habitants"],
        ["1936", "4 175 habitants"],
        ["1975", "22 611 habitants (pic)"],
        ["2023", "23 011 habitants"]
    ]
    
    col_widths3 = [30, 70]
    for annee, pop in demo_data:
        pdf.cell(col_widths3[0], 8, annee, border=1)
        pdf.cell(col_widths3[1], 8, pop, border=1)
        pdf.ln()
    
    pdf.ln(10)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Données récentes", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    
    recent_data = [
        ["1999", "20 342"],
        ["2006", "20 030"],
        ["2011", "20 711"],
        ["2016", "21 517"],
        ["2021", "22 713"],
        ["2023", "23 011"]
    ]
    
    for annee, pop in recent_data:
        pdf.cell(col_widths3[0], 8, annee, border=1)
        pdf.cell(col_widths3[1], 8, pop, border=1)
        pdf.ln()
    
    # Économie
    pdf.add_page()
    pdf.chapter_title("ÉCONOMIE")
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Revenus", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- 2010: Revenu fiscal médian/ménage = 39 599 €
- 2021: Revenu médian disponible/UC = 28 610 €""")
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Emploi (2009)", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- Population active (15-64 ans): 17 056 personnes
- Taux d'activité: 78,4%
- Taux d'emploi: 73,9%
- Taux de chômage: 4,6%""")
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Principales entreprises", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- Aéronautique: Thales, Safran Landing Systems
- Transport: Thales, Schindler
- Automobile: PSA Peugeot Citroën, Renault Trucks, Porsche, BMW, Audi
- BTP: Eiffage
- Logiciels: Dassault Systèmes, Oracle, Capgemini
- Télécommunications: Ekinops, Thales, Nokia France, Bouygues Telecom
- Logistique: Jungheinrich""")
    
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Inovel Parc", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- Environ 1 000 entreprises
- Plus de 45 000 salariés
- Pôle majeur du pôle scientifique et technologique Paris-Saclay""")
    
    # Culture et patrimoine
    pdf.add_page()
    pdf.chapter_title("CULTURE ET PATRIMOINE")
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Lieux et monuments", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- Église Saint-Denis (transférée d'Ursine en 1674)
- Église Saint-Jean-Baptiste (style moderne)
- Caserne de CRS
- Musée des CRS
- Centre culturel "l'Onde" (conçu par Claude Vasconi)""")
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Personnalités liées à la commune", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- Aline Riera (née en 1972): ancienne footballeuse française
- Bastien Sohet (né en 1986): rugbyman français
- Mayada Gargouri (née en 1988): auteur de bande dessinée française
- Olivier Megaton (né en 1965): grapheur, graphiste, réalisateur""")
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Héraldique", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """Blason défini en 1943 par la commission héraldique de la préfecture de Seine-et-Oise.

Description: D'azur à deux vols d'argent en forme de V posés l'un au-dessus de l'autre, accompagnés en chef d'une étoile et en pointe de deux quintefeuilles et entre chacun des vols, de deux épis de blé tigés et feuillés posés l'un en bande, l'autre en barre, le tout d'or.""")
    
    # Conclusion
    pdf.add_page()
    pdf.chapter_title("CONCLUSION")
    
    conclusion = """Vélizy-Villacoublay est une commune dynamique de la banlieue parisienne,
alliant développement économique avec Inovel Parc et qualité de vie avec
ses espaces verts. Sa position stratégique dans le pôle Paris-Saclay et
sa bonne desserte en transports en font une ville attractive pour les
entreprises et les habitants.

Source principale: Wikipedia
Dernière mise à jour: 2024"""
    
    pdf.chapter_body(conclusion)
    
    # Sauvegarde du PDF
    output_file = "Vélizy-Villacoublay_Rapport_Complet.pdf"
    pdf.output(output_file)
    
    print(f"PDF créé avec succès: {output_file}")
    return output_file

if __name__ == "__main__":
    create_pdf()