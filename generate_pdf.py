from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import io
import datetime

# Créer le document PDF
buffer = io.BytesIO()
doc = SimpleDocTemplate("agents_ia_2025.pdf", pagesize=letter, 
                       rightMargin=72, leftMargin=72,
                       topMargin=72, bottomMargin=72)

# Styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#2E86AB'),
    alignment=TA_CENTER,
    spaceAfter=30
)

subtitle_style = ParagraphStyle(
    'CustomSubtitle',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#A23B72'),
    alignment=TA_CENTER,
    spaceAfter=20
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=16,
    textColor=colors.HexColor('#2E86AB'),
    spaceBefore=20,
    spaceAfter=10
)

normal_style = ParagraphStyle(
    'CustomNormal',
    parent=styles['Normal'],
    fontSize=12,
    leading=14,
    spaceAfter=12
)

highlight_style = ParagraphStyle(
    'CustomHighlight',
    parent=styles['Normal'],
    fontSize=12,
    leading=14,
    backColor=colors.HexColor('#F0F7FF'),
    borderPadding=10,
    spaceAfter=12
)

quote_style = ParagraphStyle(
    'CustomQuote',
    parent=styles['Italic'],
    fontSize=11,
    leading=13,
    leftIndent=20,
    textColor=colors.HexColor('#555555'),
    borderLeft=3,
    borderLeftColor=colors.HexColor('#2E86AB'),
    borderPadding=10,
    spaceAfter=15
)

footer_style = ParagraphStyle(
    'CustomFooter',
    parent=styles['Normal'],
    fontSize=10,
    textColor=colors.gray,
    alignment=TA_CENTER
)

# Contenu de l'article
content = []

# Titre principal
content.append(Paragraph("L'Ère des Agents IA en 2025 : Révolution et Perspectives", title_style))
content.append(Paragraph("Analyse des Nouvelles Capacités et Applications Stratégiques", subtitle_style))
content.append(Spacer(1, 20))

# Date et auteur
date_info = f"Article généré le {datetime.datetime.now().strftime('%d/%m/%Y')}"
content.append(Paragraph(date_info, footer_style))
content.append(Spacer(1, 30))

# Introduction
intro_text = """
L'année 2025 marque un tournant décisif dans l'évolution des agents d'intelligence artificielle. 
Ces entités numériques autonomes ne se contentent plus d'exécuter des tâches prédéfinies ; 
elles démontrent désormais une capacité d'initiative, d'adaptation et de collaboration 
qui redéfinit notre interaction avec la technologie.
"""
content.append(Paragraph("Introduction", heading_style))
content.append(Paragraph(intro_text, normal_style))
content.append(Spacer(1, 15))

# Section 1
section1_title = "1. Les Nouveautés Majeures des Agents IA en 2025"
content.append(Paragraph(section1_title, heading_style))

section1_content = [
    ("<b>Autonomie Contextuelle Accrue</b>", 
     "Les agents IA développent une compréhension contextuelle sophistiquée, leur permettant d'anticiper les besoins sans intervention humaine explicite."),
    
    ("<b>Multimodalité Native</b>", 
     "Intégration transparente de la vision, de l'audio, du texte et des données sensoriques pour une perception holistique de l'environnement."),
    
    ("<b>Apprentissage Continu en Temps Réel</b>", 
     "Capacité d'adaptation dynamique aux nouvelles informations sans nécessiter de réentraînement complet."),
    
    ("<b>Collaboration Inter-Agents</b>", 
     "Formation de réseaux d'agents spécialisés travaillant en synergie pour résoudre des problèmes complexes."),
    
    ("<b>Raisonnement Éthique Intégré</b>", 
     "Cadres décisionnels incorporant des principes éthiques et réglementaires dès la conception.")
]

for title, desc in section1_content:
    content.append(Paragraph(title, ParagraphStyle('BulletTitle', parent=normal_style, leftIndent=20)))
    content.append(Paragraph(desc, ParagraphStyle('BulletDesc', parent=normal_style, leftIndent=40, spaceAfter=10)))

content.append(Spacer(1, 20))

# Section 2
section2_title = "2. Intérêts et Applications Stratégiques"
content.append(Paragraph(section2_title, heading_style))

highlight_text = """
Les agents IA deviennent des partenaires stratégiques dans divers domaines, 
offrant non seulement de l'efficacité opérationnelle mais aussi des avantages compétitifs décisifs.
"""
content.append(Paragraph(highlight_text, highlight_style))

# Tableau des applications
app_data = [
    ['Domaine', 'Applications Concrètes', 'Impact Potentiel'],
    ['Santé', 'Diagnostic assisté, Recherche médicamenteuse, Surveillance patients', 'Réduction de 40% des erreurs médicales'],
    ['Finance', 'Gestion de portefeuille automatisée, Détection de fraude en temps réel', 'Optimisation de 25% des rendements'],
    ['Éducation', 'Tutorat personnalisé, Création de curricula adaptatifs', 'Amélioration de 35% des apprentissages'],
    ['Industrie', 'Maintenance prédictive, Optimisation des chaînes logistiques', 'Réduction de 30% des coûts opérationnels'],
    ['Recherche', 'Simulation d\'hypothèses, Analyse de données complexes', 'Accélération de 50% des découvertes']
]

table = Table(app_data, colWidths=[1.5*inch, 2.5*inch, 2*inch])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F9FF')),
    ('GRID', (0, 0), (-1, -1), 1, colors.gray),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))

content.append(table)
content.append(Spacer(1, 20))

# Section 3
section3_title = "3. Défis et Considérations Éthiques"
content.append(Paragraph(section3_title, heading_style))

quote_text = """
"La véritable mesure de l'intelligence artificielle ne réside pas dans sa capacité technique, 
mais dans son alignement avec les valeurs humaines et son impact sociétal positif."
"""
content.append(Paragraph(quote_text, quote_style))

challenges = [
    "Transparence des décisions algorithmiques",
    "Protection des données privées et confidentialité",
    "Responsabilité légale en cas d'erreurs",
    "Équité et prévention des biais discriminatoires",
    "Impact sur l'emploi et requalification professionnelle"
]

for challenge in challenges:
    content.append(Paragraph(f"• {challenge}", normal_style))

content.append(Spacer(1, 20))

# Section 4
section4_title = "4. Perspectives d'Avenir (2026 et au-delà)"
content.append(Paragraph(section4_title, heading_style))

future_text = """
L'évolution des agents IA s'oriente vers une intégration encore plus profonde dans notre quotidien. 
Nous anticipons l'émergence d'agents capables de :
"""
content.append(Paragraph(future_text, normal_style))

future_points = [
    "Comprendre et générer des émotions complexes",
    "Collaborer avec des humains sur des projets créatifs",
    "Opérer dans des environnements physiques non structurés",
    "Développer une forme d'intuition computationnelle",
    "Contribuer à la résolution de crises mondiales (climat, santé, ressources)"
]

for point in future_points:
    content.append(Paragraph(f"› {point}", ParagraphStyle('FuturePoint', parent=normal_style, leftIndent=20)))

content.append(Spacer(1, 25))

# Conclusion
conclusion_title = "Conclusion"
content.append(Paragraph(conclusion_title, heading_style))

conclusion_text = """
Les agents IA de 2025 représentent bien plus qu'une amélioration technologique incrémentale. 
Ils incarnent un changement de paradigme fondamental dans notre relation avec la machine. 
Leur capacité croissante à comprendre, anticiper et collaborer ouvre des perspectives 
inédites pour l'innovation, tout en imposant une réflexion approfondie sur l'éthique, 
la gouvernance et l'impact sociétal.

L'enjeu n'est plus seulement technique, mais civilisationnel : comment façonner ces 
technologies pour qu'elles servent l'humanité dans son ensemble, préservant notre 
autonomie tout en amplifiant notre potentiel collectif.
"""
content.append(Paragraph(conclusion_text, normal_style))
content.append(Spacer(1, 30))

# Pied de page
footer_text = "Article généré par Hatim AI • Tous droits réservés © 2025 • Les informations présentées sont à titre informatif"
content.append(Paragraph(footer_text, footer_style))

# Générer le PDF (directement dans le fichier)
doc.build(content)

print("PDF généré avec succès: agents_ia_2025.pdf")
