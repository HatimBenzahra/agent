#!/usr/bin/env python3
"""
Analyze current PDF design and identify areas for improvement.
"""

import os
import re
import json
from typing import Dict, List, Tuple, Optional

def analyze_markdown_design(file_path: str) -> Dict:
    """Analyze the markdown structure and design elements."""
    
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {"error": f"Failed to read file: {e}"}
    
    analysis = {
        "file_name": file_path,
        "file_size_bytes": os.path.getsize(file_path),
        "total_lines": 0,
        "total_words": 0,
        "total_characters": 0,
        "heading_counts": {},
        "code_block_count": 0,
        "list_count": 0,
        "table_count": 0,
        "link_count": 0,
        "image_count": 0,
        "section_structure": [],
        "design_issues": [],
        "recommendations": []
    }
    
    lines = content.split('\n')
    analysis["total_lines"] = len(lines)
    analysis["total_words"] = len(content.split())
    analysis["total_characters"] = len(content)
    
    # Analyze headings
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Headings
        if line.startswith('# '):
            analysis["heading_counts"]["h1"] = analysis["heading_counts"].get("h1", 0) + 1
            analysis["section_structure"].append({"type": "h1", "content": line[2:], "line": i+1})
        elif line.startswith('## '):
            analysis["heading_counts"]["h2"] = analysis["heading_counts"].get("h2", 0) + 1
            analysis["section_structure"].append({"type": "h2", "content": line[3:], "line": i+1})
        elif line.startswith('### '):
            analysis["heading_counts"]["h3"] = analysis["heading_counts"].get("h3", 0) + 1
            analysis["section_structure"].append({"type": "h3", "content": line[4:], "line": i+1})
        elif line.startswith('#### '):
            analysis["heading_counts"]["h4"] = analysis["heading_counts"].get("h4", 0) + 1
            analysis["section_structure"].append({"type": "h4", "content": line[5:], "line": i+1})
        
        # Code blocks
        if line.startswith('```'):
            analysis["code_block_count"] += 1
        
        # Lists
        if line.strip().startswith(('- ', '* ', '+ ')) or re.match(r'^\d+\.\s', line):
            analysis["list_count"] += 1
        
        # Tables (simple detection)
        if '|' in line and ('---' in line or line.count('|') >= 2):
            analysis["table_count"] += 1
        
        # Links
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        matches = re.findall(link_pattern, line)
        analysis["link_count"] += len(matches)
        
        # Images
        img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        img_matches = re.findall(img_pattern, line)
        analysis["image_count"] += len(img_matches)
    
    # Identify design issues
    identify_design_issues(analysis, content)
    
    # Generate recommendations
    generate_recommendations(analysis)
    
    return analysis

def identify_design_issues(analysis: Dict, content: str) -> None:
    """Identify specific design issues in the content."""
    
    issues = []
    
    # Check heading hierarchy
    if analysis["heading_counts"].get("h1", 0) > 1:
        issues.append("Multiple H1 headings - should have only one main title")
    
    if analysis["heading_counts"].get("h2", 0) == 0 and analysis["heading_counts"].get("h1", 0) > 0:
        issues.append("No H2 headings found - poor structural hierarchy")
    
    # Check code blocks without context
    code_blocks = re.findall(r'```[\w]*\n(.*?)\n```', content, re.DOTALL)
    for i, block in enumerate(code_blocks[:3]):  # Check first 3
        lines_before = content.split(f'```')[0].split('\n')[-5:]  # Last 5 lines before code block
        explanatory_text = any(keyword in line.lower() for line in lines_before 
                              for keyword in ['example', 'code', 'implementation', 'how to'])
        if not explanatory_text and len(block.strip()) > 0:
            issues.append(f"Code block #{i+1} may lack explanatory context")
    
    # Check for long paragraphs
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    long_paragraphs = []
    for i, para in enumerate(paragraphs):
        if len(para.split()) > 200 and not para.startswith('#'):  # Very long paragraph
            long_paragraphs.append(f"Paragraph {i+1}: {len(para.split())} words (consider breaking down)")
    
    if long_paragraphs:
        issues.append(f"Long paragraphs detected: {', '.join(long_paragraphs[:3])}")
    
    # Check for inconsistent formatting
    # Look for variations in heading formatting
    heading_lines = [line for line in content.split('\n') if line.strip().startswith('#')]
    if heading_lines:
        # Check if some headings have trailing hashes or inconsistent spacing
        inconsistent = False
        for heading in heading_lines:
            if not re.match(r'^#{1,6}\s+.+$', heading):
                inconsistent = True
                break
        if inconsistent:
            issues.append("Inconsistent heading formatting detected")
    
    analysis["design_issues"] = issues

def generate_recommendations(analysis: Dict) -> None:
    """Generate design improvement recommendations."""
    
    recommendations = []
    
    # Typography recommendations
    recommendations.append("Implement consistent typographic hierarchy: H1 (24pt), H2 (18pt), H3 (14pt), body (11pt)")
    recommendations.append("Use modern sans-serif font like Inter or Open Sans for better readability")
    recommendations.append("Implement monospace font (JetBrains Mono, Fira Code) for code blocks")
    
    # Color recommendations
    recommendations.append("Define and apply a consistent color palette throughout")
    recommendations.append("Use Notion-inspired blue (#1D4ED8) for headings and links")
    recommendations.append("Apply semantic colors: green for success, yellow for warnings, red for errors")
    recommendations.append("Use light gray background (#F9FAFB) for code blocks with 1px border (#E5E7EB)")
    
    # Layout recommendations
    recommendations.append("Increase whitespace: 2cm margins, 12pt between paragraphs, 24pt between sections")
    recommendations.append("Implement grid system for consistent alignment")
    recommendations.append("Consider two-column layout for desktop viewing")
    
    # Code block recommendations
    if analysis["code_block_count"] > 0:
        recommendations.append("Add syntax highlighting for code blocks")
        recommendations.append("Include line numbers for code references")
        recommendations.append("Add explanatory context before each code example")
        recommendations.append("Ensure code blocks have proper padding and background")
    
    # Navigation recommendations
    recommendations.append("Add clickable table of contents with internal links")
    recommendations.append("Include PDF bookmarks for easy navigation")
    recommendations.append("Add header with section title and footer with page numbers")
    
    # Accessibility recommendations
    recommendations.append("Ensure WCAG AA compliance: minimum 4.5:1 text contrast")
    recommendations.append("Use semantic HTML structure when converting to PDF")
    recommendations.append("Add alt text for any images")
    
    # Content structure recommendations
    if analysis["table_count"] > 0:
        recommendations.append("Optimize tables for PDF: limit width, add descriptions")
    
    if analysis["list_count"] > 10:
        recommendations.append("Consider grouping related list items under subheadings")
    
    analysis["recommendations"] = recommendations

def analyze_pdf_visual(file_path: str) -> Dict:
    """Analyze visual aspects of PDF (placeholder for PDF analysis)."""
    
    if not os.path.exists(file_path):
        return {"error": f"PDF file not found: {file_path}"}
    
    try:
        file_size = os.path.getsize(file_path)
    except Exception as e:
        return {"error": f"Failed to analyze PDF: {e}"}
    
    return {
        "file_name": file_path,
        "file_size_bytes": file_size,
        "file_size_kb": file_size / 1024,
        "note": "Full PDF visual analysis requires PDF parsing libraries. Recommendations based on standard technical documentation issues."
    }

def main():
    """Main analysis function."""
    
    print("=" * 60)
    print("Analyse du Design du PDF Actuel")
    print("=" * 60)
    
    # Files to analyze
    markdown_file = "documentation-complete-compiled.md"
    pdf_file = "documentation-api-notion.pdf"
    
    print(f"\n1. Analyse du fichier Markdown: {markdown_file}")
    print("-" * 40)
    
    md_analysis = analyze_markdown_design(markdown_file)
    
    if "error" in md_analysis:
        print(f"Erreur: {md_analysis['error']}")
    else:
        print(f"Taille du fichier: {md_analysis['file_size_bytes']:,} octets")
        print(f"Nombre de lignes: {md_analysis['total_lines']}")
        print(f"Nombre de mots: {md_analysis['total_words']:,}")
        print(f"Nombre de caractères: {md_analysis['total_characters']:,}")
        
        print(f"\nStructure des titres:")
        for level, count in md_analysis["heading_counts"].items():
            print(f"  {level.upper()}: {count}")
        
        print(f"\nÉléments de contenu:")
        print(f"  Blocs de code: {md_analysis['code_block_count']}")
        print(f"  Listes: {md_analysis['list_count']}")
        print(f"  Tables: {md_analysis['table_count']}")
        print(f"  Liens: {md_analysis['link_count']}")
        print(f"  Images: {md_analysis['image_count']}")
        
        print(f"\nProblèmes de design identifiés ({len(md_analysis['design_issues'])}):")
        for i, issue in enumerate(md_analysis['design_issues'], 1):
            print(f"  {i}. {issue}")
    
    print(f"\n2. Analyse du fichier PDF: {pdf_file}")
    print("-" * 40)
    
    pdf_analysis = analyze_pdf_visual(pdf_file)
    
    if "error" in pdf_analysis:
        print(f"Erreur: {pdf_analysis['error']}")
    else:
        print(f"Taille du fichier: {pdf_analysis['file_size_kb']:.1f} KB")
        print(f"Note: {pdf_analysis['note']}")
    
    print(f"\n3. Recommandations de design ({len(md_analysis.get('recommendations', []))}):")
    print("-" * 40)
    
    if "recommendations" in md_analysis:
        for i, rec in enumerate(md_analysis["recommendations"], 1):
            print(f"  {i}. {rec}")
    
    print(f"\n4. Résumé de l'analyse:")
    print("-" * 40)
    
    summary = {
        "issues_count": len(md_analysis.get("design_issues", [])),
        "recommendations_count": len(md_analysis.get("recommendations", [])),
        "key_areas": [
            "Hiérarchie typographique",
            "Cohérence des couleurs",
            "Espace blanc et mise en page",
            "Lisibilité du code",
            "Navigation dans le PDF",
            "Accessibilité"
        ],
        "priority_focus": "Typographie et mise en page (fondamentaux du design)"
    }
    
    print(f"Nombre de problèmes identifiés: {summary['issues_count']}")
    print(f"Nombre de recommandations: {summary['recommendations_count']}")
    print(f"Domaines clés à améliorer: {', '.join(summary['key_areas'])}")
    print(f"Priorité: {summary['priority_focus']}")
    
    # Save analysis to file
    output_file = "pdf_design_analysis.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "markdown_analysis": md_analysis,
            "pdf_analysis": pdf_analysis,
            "summary": summary
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Analyse sauvegardée dans: {output_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()