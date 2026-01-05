#!/usr/bin/env python3
# Créer un PDF avec fpdf2 - version corrigée

from fpdf import FPDF
from datetime import datetime

class UnicodePDF(FPDF):
    def header(self):
        # Titre
        self.set_font('Helvetica', 'B', 16)
        title = "VELIZY-VILLACOUBLAY"
        self.cell(0, 10, title, 0, 1, 'C')
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 10, f"Informations Wikipedia - Genere le {datetime.now().strftime('%d/%m/%Y')}", 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        page_num = f'Page {self.page_no()}'
        self.cell(0, 10, page_num, 0, 0, 'C')
    
    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(4)
    
    def chapter_body(self, body):
        self.set_font('Helvetica', '', 11)
        # Utiliser une fonction pour remplacer les caractères spéciaux
        safe_body = body.replace('€', 'EUR')
        self.multi_cell(0, 5, safe_body)
        self.ln()

def create_pdf():
    pdf = UnicodePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Introduction
    pdf.chapter_title("INTRODUCTION")
    intro = """Velizy-Villacoublay est une commune francaise situee dans le departement des Yvelines en region Ile-de-France, a trois kilometres a l'est de Versailles.

Ville industrielle, accueillant de nombreux sieges sociaux d'entreprise, elle constitue la partie nord du pole scientifique et technologique Paris-Saclay, en cours d'amenagement depuis 2010.

Depuis le 1er janvier 2016, elle fait partie de Versailles Grand Parc. Ses habitants sont appeles les Veliziens."""
    pdf.chapter_body(intro)
    
    # Geographie
    pdf.add_page()
    pdf.chapter_title("GEOGRAPHIE")
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Localisation", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- Distance de Paris: 9 km de la Porte de Saint-Cloud
- Distance de Versailles: 3,5 km a l'est
- Superficie: 893 hectares
- Altitude: 102 a 179 metres""")
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Environnement", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- Foret domaniale de Meudon: 313 hectares
- Espaces verts: plus de 65 hectares""")
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Climat", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, "Climat oceanique degrade des plaines du Centre et du Nord.")
    
    # Transports
    pdf.add_page()
    pdf.chapter_title("TRANSPORTS")
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Voies routieres", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, "- A86\n- RN 118\n- RN 12")
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Transports en commun", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- RER C: Gare de Chaville - Velizy (a Viroflay)
- Tramway T6: 7 stations sur la commune
- Bus RATP: Lignes 179, 190, 291, 390
- Reseau Noctilien: Ligne N66 (nuit)""")
    
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
6. Velizy - Bas (avec l'Ursine et le Bocage)""")
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Occupation des sols (2018)", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- Tissu urbain discontinu: 20,5% (184 ha)
- Zones industrielles/commerciales: 27,3% (245 ha)
- Reseaux routiers/ferroviaires: 3,7% (33 ha)
- Aeroports: 13,2% (118 ha)
- Equipements sportifs: 1,2% (11 ha)
- Forets de feuillus: 34,1% (306 ha)""")
    
    # Histoire
    pdf.add_page()
    pdf.chapter_title("HISTOIRE - DATES IMPORTANTES")
    
    dates = [
        ["1er juillet 1815", "Bataille de Velizy (general Exelmans)"],
        ["1936", "Creation de la base aerienne 107 Villacoublay"],
        ["29 mai 1937", "La commune devient Velizy-Villacoublay"],
        ["Seconde Guerre mondiale", "Base bombardee a plusieurs reprises"],
        ["23 aout 1944", "Liberation par les Allies"],
        ["1952", "Citation a l'ordre de la Nation avec Croix de guerre"],
        ["1972", "Ouverture du centre commercial Velizy 2"],
        ["1991", "Creation de l'IUT de Velizy"],
        ["2002", "Inauguration du centre culturel 'l'Onde'"],
        ["13 decembre 2014", "Mise en service du tramway T6"]
    ]
    
    # Tableau des dates
    col_widths = [40, 140]
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(col_widths[0], 8, "Date", border=1)
    pdf.cell(col_widths[1], 8, "Evenement", border=1)
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
        ["2004-2014", "Joel Loison", "UMP"],
        ["2014-en cours", "Pascal Thevenot", "LR/Soyons libres"]
    ]
    
    col_widths2 = [30, 70, 50]
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(col_widths2[0], 8, "Periode", border=1)
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
    pdf.cell(0, 6, "Intercommunalite", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- 2014: Rejoint Grand Paris Seine Ouest (GPSO)
- 2016: Integre Versailles Grand Parc""")
    
    # Demographie
    pdf.add_page()
    pdf.chapter_title("DEMOGRAPHIE")
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Evolution demographique", 0, 1)
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
    pdf.cell(0, 6, "Donnees recentes", 0, 1)
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
    
    # Economie
    pdf.add_page()
    pdf.chapter_title("ECONOMIE")
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Revenus", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- 2010: Revenu fiscal median/menage = 39 599 EUR
- 2021: Revenu median disponible/UC = 28 610 EUR""")
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Emploi (2009)", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- Population active (15-64 ans): 17 056 personnes
- Taux d'activite: 78,4%
- Taux d'emploi: 73,9%
- Taux de chomage: 4,6%""")
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Principales entreprises", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- Aeronautique: Thales, Safran Landing Systems
- Transport: Thales, Schindler
- Automobile: PSA Peugeot Citroen, Renault Trucks, Porsche, BMW, Audi
- BTP: Eiffage
- Logiciels: Dassault Systemes, Oracle, Capgemini
- Telecommunications: Ekinops, Thales, Nokia France, Bouygues Telecom
- Logistique: Jungheinrich""")
    
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Inovel Parc", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- Environ 1 000 entreprises
- Plus de 45 000 salaries
- Pole majeur du pole scientifique et technologique Paris-Saclay""")
    
    # Culture et patrimoine
    pdf.add_page()
    pdf.chapter_title("CULTURE ET PATRIMOINE")
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Lieux et monuments", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- Eglise Saint-Denis (transferee d'Ursine en 1674)
- Eglise Saint-Jean-Baptiste (style moderne)
- Caserne de CRS
- Musee des CRS
- Centre culturel "l'Onde" (concu par Claude Vasconi)""")
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Personnalites liees a la commune", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """- Aline Riera (nee en 1972): ancienne footballeuse francaise
- Bastien Sohet (ne en 1986): rugbyman francais
- Mayada Gargouri (nee en 1988): auteur de bande dessinee francaise
- Olivier Megaton (ne en 1965): grapheur, graphiste, realisateur""")
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, "Heraldique", 0, 1)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 5, """Blason defini en 1943 par la commission heraldique de la prefecture de Seine-et-Oise.

Description: D'azur a deux vols d'argent en forme de V poses l'un au-dessus de l'autre, accompagnes en chef d'une etoile et en pointe de deux quintefeuilles et entre chacun des vols, de deux epis de ble tiges et feuilles poses l'un en bande, l'autre en barre, le tout d'or.""")
    
    # Conclusion
    pdf.add_page()
    pdf.chapter_title("CONCLUSION")
    
    conclusion = """Velizy-Villacoublay est une commune dynamique de la banlieue parisienne,
alliant developpement economique avec Inovel Parc et qualite de vie avec
ses espaces verts. Sa position strategique dans le pole Paris-Saclay et
sa bonne desserte en transports en font une ville attractive pour les
entreprises et les habitants.

Source principale: Wikipedia
Derniere mise a jour: 2024"""
    
    pdf.chapter_body(conclusion)
    
    # Sauvegarde du PDF
    output_file = "Velizy-Villacoublay_Rapport_Wikipedia.pdf"
    pdf.output(output_file)
    
    print(f"PDF cree avec succes: {output_file}")
    print(f"Taille: {os.path.getsize(output_file) if os.path.exists(output_file) else 0} bytes")
    return output_file

if __name__ == "__main__":
    create_pdf()