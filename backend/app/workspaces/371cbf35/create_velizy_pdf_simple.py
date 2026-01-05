#!/usr/bin/env python3
# Script simple pour créer un PDF avec les informations sur Vélizy-Villacoublay

import os
from datetime import datetime

def create_simple_pdf():
    """Crée un PDF simple avec les informations sur Vélizy-Villacoublay"""
    
    # Contenu du PDF en format texte simple
    content = """VÉLIZY-VILLACOUBLAY - INFORMATIONS WIKIPEDIA

Généré le: {date}
Source: Wikipedia

================================================================================
INTRODUCTION
================================================================================

Vélizy-Villacoublay est une commune française située dans le département des Yvelines
en région Île-de-France, à trois kilomètres à l'est de Versailles.

Ville industrielle, accueillant de nombreux sièges sociaux d'entreprise, elle constitue
la partie nord du pôle scientifique et technologique Paris-Saclay, en cours d'aménagement
depuis 2010.

Depuis le 1er janvier 2016, elle fait partie de Versailles Grand Parc.
Ses habitants sont appelés les Véliziens.

================================================================================
GÉOGRAPHIE
================================================================================

LOCALISATION
------------
- Distance de Paris: 9 km de la Porte de Saint-Cloud
- Distance de Versailles: 3,5 km à l'est
- Superficie: 893 hectares
- Altitude: 102 à 179 mètres

ENVIRONNEMENT
-------------
- Forêt domaniale de Meudon: 313 hectares
- Espaces verts: plus de 65 hectares

CLIMAT
------
Climat océanique dégradé des plaines du Centre et du Nord.

================================================================================
TRANSPORTS
================================================================================

VOIES ROUTIÈRES
---------------
- A86
- RN 118
- RN 12

TRANSPORTS EN COMMUN
--------------------
- RER C: Gare de Chaville - Vélizy (à Viroflay)
- Tramway T6: 7 stations sur la commune
- Bus RATP: Lignes 179, 190, 291, 390
- Réseau Noctilien: Ligne N66 (nuit)

================================================================================
URBANISME
================================================================================

QUARTIERS D'HABITATION
----------------------
1. Mozart
2. Le Clos
3. Le Mail (avec Pointe Ouest)
4. Le Village
5. Est (avec Louvois et Europe)
6. Vélizy - Bas (avec l'Ursine et le Bocage)

OCCUPATION DES SOLS (2018)
--------------------------
- Tissu urbain discontinu: 20,5% (184 ha)
- Zones industrielles/commerciales: 27,3% (245 ha)
- Réseaux routiers/ferroviaires: 3,7% (33 ha)
- Aéroports: 13,2% (118 ha)
- Équipements sportifs: 1,2% (11 ha)
- Forêts de feuillus: 34,1% (306 ha)

================================================================================
HISTOIRE
================================================================================

DATES IMPORTANTES
-----------------
- 1er juillet 1815: Bataille de Vélizy (général Exelmans)
- 1936: Création de la base aérienne 107 Villacoublay
- 29 mai 1937: La commune devient Vélizy-Villacoublay
- Seconde Guerre mondiale: Base bombardée à plusieurs reprises
- 23 août 1944: Libération par les Alliés
- 1952: Citation à l'ordre de la Nation avec Croix de guerre
- 1972: Ouverture du centre commercial Vélizy 2
- 1991: Création de l'IUT de Vélizy
- 2002: Inauguration du centre culturel "l'Onde"
- 13 décembre 2014: Mise en service du tramway T6

================================================================================
POLITIQUE ET ADMINISTRATION
================================================================================

LISTE DES MAIRES DEPUIS 1953
-----------------------------
1953-1988: Robert Wagner (UNR/UDR/RPR)
1988-1990: Antoine Trani (RPR)
1990-2004: Raymond Loisel (RPR/UMP)
2004-2014: Joël Loison (UMP)
2014-en cours: Pascal Thévenot (LR/Soyons libres)

INTERCOMMUNALITÉ
----------------
- 2014: Rejoint Grand Paris Seine Ouest (GPSO)
- 2016: Intègre Versailles Grand Parc

================================================================================
DÉMOGRAPHIE
================================================================================

ÉVOLUTION DÉMOGRAPHIQUE
-----------------------
1793: 168 habitants
1921: 1 487 habitants
1936: 4 175 habitants
1975: 22 611 habitants (pic)
2023: 23 011 habitants

DONNÉES RÉCENTES
----------------
1999: 20 342
2006: 20 030
2011: 20 711
2016: 21 517
2021: 22 713
2023: 23 011

STRUCTURE PAR ÂGE (2018)
------------------------
- Taux < 30 ans: 38,6% (département: 38%)
- Population: 11 330 hommes / 11 319 femmes
- Taux d'hommes: 50,02% (département: 48,68%)

================================================================================
ÉCONOMIE
================================================================================

REVENUS
-------
- 2010: Revenu fiscal médian/ménage = 39 599 €
- 2021: Revenu médian disponible/UC = 28 610 €

EMPLOI (2009)
-------------
- Population active (15-64 ans): 17 056 personnes
- Taux d'activité: 78,4%
- Taux d'emploi: 73,9%
- Taux de chômage: 4,6%

ENTREPRISES (Décembre 2010)
---------------------------
Total établissements: 1 898
- Agriculture: 3
- Industrie: 88
- Construction: 141
- Commerce/transports/services: 1 459
- Secteur administratif: 207

PRINCIPALES ENTREPRISES
-----------------------
- Aéronautique: Thales, Safran Landing Systems
- Transport: Thales, Schindler
- Automobile: PSA Peugeot Citroën, Renault Trucks, Porsche, BMW, Audi
- BTP: Eiffage
- Logiciels: Dassault Systèmes, Oracle, Capgemini
- Télécommunications: Ekinops, Thales, Nokia France, Bouygues Telecom
- Logistique: Jungheinrich

INOVEL PARC
-----------
- Environ 1 000 entreprises
- Plus de 45 000 salariés
- Pôle majeur du pôle scientifique et technologique Paris-Saclay

================================================================================
CULTURE ET PATRIMOINE
================================================================================

LIEUX ET MONUMENTS
------------------
- Église Saint-Denis (transférée d'Ursine en 1674)
- Église Saint-Jean-Baptiste (style moderne)
- Caserne de CRS
- Musée des CRS
- Centre culturel "l'Onde" (conçu par Claude Vasconi)

PERSONNALITÉS LIÉES À LA COMMUNE
----------------------------------
- Aline Riera (née en 1972): ancienne footballeuse française
- Bastien Sohet (né en 1986): rugbyman français
- Mayada Gargouri (née en 1988): auteur de bande dessinée française
- Olivier Megaton (né en 1965): grapheur, graphiste, réalisateur

HÉRALDIQUE
----------
Blason défini en 1943 par la commission héraldique de la préfecture de Seine-et-Oise.

Description: D'azur à deux vols d'argent en forme de V posés l'un au-dessus de l'autre,
accompagnés en chef d'une étoile et en pointe de deux quintefeuilles et entre chacun
des vols, de deux épis de blé tigés et feuillés posés l'un en bande, l'autre en barre,
le tout d'or.

================================================================================
CONCLUSION
================================================================================

Vélizy-Villacoublay est une commune dynamique de la banlieue parisienne,
alliant développement économique avec Inovel Parc et qualité de vie avec
ses espaces verts. Sa position stratégique dans le pôle Paris-Saclay et
sa bonne desserte en transports en font une ville attractive pour les
entreprises et les habitants.

================================================================================

Source principale: Wikipedia
Dernière mise à jour: 2024

"""

    # Ajouter la date
    content = content.format(date=datetime.now().strftime('%d/%m/%Y à %H:%M'))
    
    # Créer le fichier PDF en utilisant une conversion simple via HTML
    output_file = "Vélizy-Villacoublay_Informations.pdf"
    
    # Créer un fichier texte d'abord
    txt_file = "velizy_info.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Essayer de créer un PDF simple avec une méthode alternative
    try:
        # Méthode 1: Utiliser pandoc si disponible
        import subprocess
        result = subprocess.run(['which', 'pandoc'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Pandoc trouvé, conversion en PDF...")
            subprocess.run(['pandoc', txt_file, '-o', output_file])
        else:
            print("Pandoc non trouvé, création d'un fichier texte formaté...")
            # Créer un fichier texte bien formaté comme alternative
            output_file = "Vélizy-Villacoublay_Informations.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
    except:
        # Si tout échoue, créer juste un fichier texte
        output_file = "Vélizy-Villacoublay_Informations.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"Document créé avec succès : {output_file}")
    print(f"Taille du document : {len(content)} caractères")
    
    return output_file

if __name__ == "__main__":
    create_simple_pdf()