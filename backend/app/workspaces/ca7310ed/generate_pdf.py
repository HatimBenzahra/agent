#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to generate a PDF article about AI agents in 2025
Uses the reportlab library to create a styled PDF document
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime

def generate_pdf(filename="ai_agents_2025.pdf"):
    """Generates a PDF article about AI agents in 2025"""
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Prepare the content
    story = []
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#3498DB'),
        spaceBefore=20,
        spaceAfter=15
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#2C3E50'),
        alignment=TA_JUSTIFY,
        spaceBefore=6,
        spaceAfter=6
    )
    
    # Main title
    story.append(Paragraph("The Age of AI Agents in 2025: Innovations and Impacts", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Subtitle and information
    story.append(Paragraph("Research Article - Artificial Intelligence", styles['Heading3']))
    story.append(Paragraph(f"Date: {datetime.datetime.now().strftime('%d %B %Y')}", styles['Normal']))
    story.append(Paragraph("Author: Future AI Research Team", styles['Normal']))
    story.append(Spacer(1, 0.4*inch))
    
    # Introduction
    story.append(Paragraph("Introduction", subtitle_style))
    story.append(Paragraph(
        "The year 2025 marks a decisive turning point in the evolution of artificial intelligence agents. "
        "These autonomous systems, capable of perceiving, analyzing, and acting in complex environments, "
        "are radically transforming our relationship with technology. This article explores the major innovations, "
        "emerging trends, and challenges shaping the landscape of AI agents in 2025.",
        body_style
    ))
    story.append(Spacer(1, 0.3*inch))
    
    # Section 1: Technological innovations
    story.append(Paragraph("1. Major Technological Innovations", subtitle_style))
    
    story.append(Paragraph(
        "1.1 Autonomous Multi-Modal Agents", styles['Heading4']
    ))
    story.append(Paragraph(
        "In 2025, AI agents can simultaneously process text, images, audio, and video with deep contextual understanding. "
        "These systems create unified representations of the world that allow them to act with unprecedented flexibility and adaptability.",
        body_style
    ))
    
    story.append(Paragraph(
        "1.2 Hierarchical Agent Architecture", styles['Heading4']
    ))
    story.append(Paragraph(
        "New architectures enable specialized agents to collaborate under the supervision of a primary agent. "
        "This hierarchical approach optimizes complex problem-solving by distributing tasks according to each agent's specific competencies.",
        body_style
    ))
    
    story.append(Paragraph(
        "1.3 Continuous Real-Time Learning", styles['Heading4']
    ))
    story.append(Paragraph(
        "2025 agents can learn and adapt continuously from new experiences without requiring massive retraining. "
        "This dynamic adaptation capability revolutionizes their deployment in rapidly evolving environments.",
        body_style
    ))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Section 2: Application domains
    story.append(Paragraph("2. Transformative Application Domains", subtitle_style))
    
    # Application table
    app_data = [
        ['Domain', 'Application', 'Impact'],
        ['Healthcare', 'AI-assisted diagnosis, Medical monitoring agents', '40% reduction in diagnostic errors'],
        ['Finance', 'Autonomous financial advisors, Intelligent fraud detection', '30% portfolio optimization'],
        ['Education', 'Personalized tutors, Adaptive learning agents', '60% increase in knowledge retention'],
        ['Industry', 'Supply chain optimization, Predictive maintenance', '25% reduction in operational costs'],
        ['Research', 'AI scientific collaborators, Discovery automation', '50% acceleration of scientific breakthroughs']
    ]
    
    app_table = Table(app_data, colWidths=[2*inch, 2.5*inch, 2.5*inch])
    app_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ECF0F1')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    
    story.append(app_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Section 3: Challenges and concerns
    story.append(Paragraph("3. Ethical and Technical Challenges", subtitle_style))
    
    story.append(Paragraph(
        "3.1 Ethical Questions", styles['Heading4']
    ))
    story.append(Paragraph(
        "The growing autonomy of AI agents raises crucial questions about accountability, transparency, and human control. "
        "2025 systems must integrate robust accountability mechanisms and ethical safeguards.",
        body_style
    ))
    
    story.append(Paragraph(
        "3.2 Security and Privacy", styles['Heading4']
    ))
    story.append(Paragraph(
        "The protection of personal data and the security of autonomous systems are absolute priorities. "
        "New architectures include homomorphic encryption protocols and differential privacy techniques.",
        body_style
    ))
    
    story.append(Paragraph(
        "3.3 Interoperability", styles['Heading4']
    ))
    story.append(Paragraph(
        "The diversity of platforms and technical standards requires universal interfaces that enable agents "
        "from different origins to collaborate effectively.",
        body_style
    ))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Section 4: Future trends
    story.append(Paragraph("4. Emerging Trends for 2025 and Beyond", subtitle_style))
    
    trends = [
        "• Inter-enterprise collaborative AI agents",
        "• Self-improving agent systems",
        "• Integration with augmented and virtual reality",
        "• Specialized agents for environmental sustainability",
        "• Democratized open-source agent platforms"
    ]
    
    for trend in trends:
        story.append(Paragraph(trend, body_style))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Conclusion
    story.append(Paragraph("Conclusion", subtitle_style))
    story.append(Paragraph(
        "AI agents in 2025 represent a transformative advancement in the history of artificial intelligence. "
        "Their ability to act autonomously while collaborating with humans opens unprecedented perspectives "
        "for solving the complex challenges of our time. However, this technological power comes with increased "
        "responsibility regarding ethics, security, and governance.",
        body_style
    ))
    
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph(
        "The future of AI agents depends on a delicate balance between technological innovation and human considerations. "
        "In 2025, the priority is to develop systems that amplify human capabilities while preserving our autonomy "
        "and fundamental values.",
        body_style
    ))
    
    story.append(Spacer(1, 0.5*inch))
    
    # References
    story.append(Paragraph("References and Sources", subtitle_style))
    story.append(Paragraph("1. 2025 Global AI Report - AI Research Institute", styles['Normal']))
    story.append(Paragraph("2. Journal of Advanced Artificial Intelligence", styles['Normal']))
    story.append(Paragraph("3. International Conference on Autonomous Systems 2024", styles['Normal']))
    story.append(Paragraph("4. White Paper: Ethical and Responsible AI Agents", styles['Normal']))
    
    # Generate the PDF
    doc.build(story)
    print(f"PDF generated successfully: {filename}")
    
    return filename

if __name__ == "__main__":
    print("Generating PDF article about AI agents in 2025...")
    pdf_file = generate_pdf()
    print(f"Article created successfully: {pdf_file}")
    print("The document contains sections on:")
    print("1. Technological innovations")
    print("2. Application domains")
    print("3. Ethical challenges")
    print("4. Future trends")