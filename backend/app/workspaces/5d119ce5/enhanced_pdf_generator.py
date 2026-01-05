#!/usr/bin/env python3
"""
Enhanced PDF Generator with Advanced Features
Creates a comprehensive, multi-page PDF with improved formatting
"""

from fpdf import FPDF
from datetime import datetime
import textwrap

class EnhancedPDFGenerator:
    def __init__(self, title="Enhanced PDF Document"):
        """Initialize the PDF generator with advanced settings"""
        self.pdf = FPDF(format='A4', unit='mm')
        self.pdf.set_auto_page_break(auto=True, margin=20)
        self.pdf.set_margins(left=20, top=25, right=20)
        self.pdf.set_compression(True)
        self.title = title
        self.page_number = 0
        
        # Define color palette
        self.colors = {
            'primary': (51, 51, 102),      # Dark blue
            'secondary': (0, 102, 204),     # Blue
            'accent': (255, 102, 0),        # Orange
            'light': (240, 240, 240),       # Light gray
            'dark': (51, 51, 51),           # Dark gray
            'text': (34, 34, 34),           # Near black
            'success': (76, 175, 80),        # Green
            'warning': (255, 152, 0),       # Orange
            'error': (244, 67, 54)          # Red
        }
        
    def set_color(self, color_name):
        """Set text color"""
        if color_name in self.colors:
            r, g, b = self.colors[color_name]
            self.pdf.set_text_color(r, g, b)
            
    def reset_color(self):
        """Reset to default text color"""
        self.pdf.set_text_color(0, 0, 0)
        
    def add_header(self):
        """Add header to current page"""
        self.pdf.set_y(10)
        self.set_color('primary')
        self.pdf.set_font('helvetica', 'B', 12)
        self.pdf.cell(0, 10, self.title, align='L')
        
        # Add date on right side
        date_str = datetime.now().strftime("%Y-%m-%d")
        self.pdf.cell(0, 10, date_str, align='R')
        self.reset_color()
        
        # Add separator line
        self.pdf.set_line_width(0.5)
        self.pdf.line(20, 22, 190, 22)
        self.pdf.set_y(25)  # Reset Y position
        
    def add_footer(self):
        """Add footer to current page"""
        self.pdf.set_y(-15)
        self.set_color('dark')
        self.pdf.set_font('helvetica', 'I', 8)
        page_num = self.pdf.page_no()
        self.pdf.cell(0, 10, f'Page {page_num}', align='C')
        self.reset_color()
        
    def add_title_page(self, title="Enhanced PDF Document", subtitle=None, author=None):
        """Add a professionally formatted title page"""
        self.pdf.add_page()
        self.page_number += 1
        
        # Background color for title page
        self.pdf.set_fill_color(240, 240, 250)
        self.pdf.rect(0, 0, 210, 297, 'F')
        
        # Center title
        self.pdf.set_y(80)
        self.set_color('primary')
        self.pdf.set_font('helvetica', 'B', 32)
        self.pdf.cell(0, 20, title, align='C', ln=True)
        self.reset_color()
        
        # Add subtitle if provided
        if subtitle:
            self.set_color('secondary')
            self.pdf.set_font('helvetica', '', 18)
            self.pdf.cell(0, 15, subtitle, align='C', ln=True)
            self.reset_color()
            
        # Add decorative line
        self.pdf.set_line_width(1)
        self.set_color('accent')
        self.pdf.line(50, 140, 160, 140)
        self.reset_color()
        
        # Add author and date
        self.pdf.set_y(160)
        if author:
            self.pdf.set_font('helvetica', '', 14)
            self.pdf.cell(0, 10, f"Prepared by: {author}", align='C', ln=True)
            
        current_date = datetime.now().strftime("%B %d, %Y")
        self.pdf.set_font('helvetica', 'I', 12)
        self.pdf.cell(0, 10, current_date, align='C', ln=True)
        
        # Add version info
        self.pdf.set_y(250)
        self.pdf.set_font('helvetica', '', 10)
        self.pdf.set_text_color(128, 128, 128)
        self.pdf.cell(0, 10, "Generated with Enhanced PDF Generator v1.0", align='C')
        self.reset_color()
        
    def add_table_of_contents(self, sections):
        """Add a formatted table of contents"""
        self.pdf.add_page()
        self.add_header()
        self.page_number += 1
        
        # Table of contents title
        self.set_color('primary')
        self.pdf.set_font('helvetica', 'B', 20)
        self.pdf.cell(0, 15, "TABLE OF CONTENTS", ln=True, align='C')
        self.reset_color()
        
        self.pdf.ln(15)
        
        # Add sections with dot leaders
        for i, (section_title, page_num) in enumerate(sections, 1):
            self.pdf.set_font('helvetica', 'B', 14)
            self.pdf.cell(0, 10, f"{i}. {section_title}", ln=False)
            
            # Add dot leaders
            self.pdf.set_font('helvetica', '', 10)
            dot_x = self.pdf.get_x()
            self.pdf.set_x(180)
            self.pdf.cell(10, 10, "......", align='R', ln=False)
            
            # Page number
            self.pdf.cell(10, 10, str(page_num), align='R', ln=True)
            
        self.pdf.ln(10)
        self.add_footer()
        
    def add_section(self, title, content, level=1):
        """Add a content section with hierarchical headings"""
        # Add page if needed
        if self.pdf.get_y() > 240:
            self.pdf.add_page()
            self.add_header()
            self.page_number += 1
            
        # Format section title based on level
        font_sizes = {1: 18, 2: 16, 3: 14}
        font_size = font_sizes.get(level, 14)
        
        self.set_color('secondary')
        self.pdf.set_font('helvetica', 'B', font_size)
        self.pdf.cell(0, 12, title, ln=True)
        self.reset_color()
        
        # Add spacing
        self.pdf.ln(5)
        
        # Add content with text wrapping
        self.pdf.set_font('helvetica', '', 11)
        paragraphs = content.split('\n\n')
        
        for paragraph in paragraphs:
            if paragraph.strip():
                # Wrap text to fit page width
                lines = textwrap.wrap(paragraph, width=90)
                for line in lines:
                    self.pdf.multi_cell(0, 6, line)
                self.pdf.ln(5)
                
        self.pdf.ln(10)
        
    def add_bulleted_list(self, title, items):
        """Add a bulleted list with custom bullets"""
        self.add_section(title, "")
        
        self.pdf.set_font('helvetica', '', 11)
        for item in items:
            # Custom bullet point
            self.set_color('accent')
            self.pdf.cell(8, 6, "►", ln=False)
            self.reset_color()
            
            # Item text
            self.pdf.multi_cell(0, 6, f" {item}")
            self.pdf.ln(3)
            
        self.pdf.ln(10)
        
    def add_table(self, title, headers, data, col_widths=None):
        """Add a formatted table with alternating row colors"""
        self.add_section(title, "")
        
        # Calculate column widths if not provided
        if not col_widths:
            col_widths = [self.pdf.w / (len(headers) + 1)] * len(headers)
            
        # Table header
        self.set_color('primary')
        self.pdf.set_font('helvetica', 'B', 12)
        for i, header in enumerate(headers):
            self.pdf.cell(col_widths[i], 10, header, border=1, align='C', fill=True)
        self.pdf.ln()
        self.reset_color()
        
        # Table rows with alternating colors
        for row_idx, row in enumerate(data):
            # Alternate row colors
            if row_idx % 2 == 0:
                self.pdf.set_fill_color(245, 245, 245)
            else:
                self.pdf.set_fill_color(255, 255, 255)
                
            self.pdf.set_font('helvetica', '', 11)
            for i, cell in enumerate(row):
                self.pdf.cell(col_widths[i], 10, str(cell), border=1, align='C', fill=True)
            self.pdf.ln()
            
        self.pdf.set_fill_color(255, 255, 255)  # Reset fill color
        self.pdf.ln(15)
        
    def add_code_block(self, title, code, language="python"):
        """Add a formatted code block with syntax highlighting"""
        self.add_section(title, "")
        
        # Code block background
        self.pdf.set_fill_color(40, 44, 52)
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font('courier', '', 10)
        
        # Draw code block rectangle
        x, y = self.pdf.get_x(), self.pdf.get_y()
        self.pdf.rect(x, y, 170, 60, 'F')
        
        # Add code with slight indentation
        self.pdf.set_xy(x + 5, y + 5)
        lines = code.split('\n')
        for line in lines:
            self.pdf.cell(0, 5, line[:85], ln=True)  # Limit line length
            if self.pdf.get_y() > y + 55:  # Check if we're exceeding box height
                break
                
        self.reset_color()
        self.pdf.set_y(y + 65)  # Move below code block
        self.pdf.ln(10)
        
    def add_chart_summary(self, title, chart_data):
        """Add a summary section with chart/statistics"""
        self.add_section(title, "")
        
        # Add summary statistics
        self.pdf.set_font('helvetica', '', 11)
        for label, value in chart_data.items():
            self.pdf.cell(40, 8, f"{label}:", ln=False)
            self.pdf.set_font('helvetica', 'B', 11)
            self.pdf.cell(0, 8, f" {value}", ln=True)
            self.pdf.set_font('helvetica', '', 11)
            
        self.pdf.ln(10)
        
    def add_conclusion(self, title, content):
        """Add a conclusion section with emphasis"""
        self.pdf.add_page()
        self.add_header()
        self.page_number += 1
        
        # Add decorative box
        self.pdf.set_draw_color(51, 51, 102)
        self.pdf.set_line_width(1)
        self.pdf.set_fill_color(240, 240, 250)
        self.pdf.rect(15, 40, 180, 200, 'FD')
        
        # Conclusion title
        self.pdf.set_xy(20, 50)
        self.set_color('primary')
        self.pdf.set_font('helvetica', 'B', 22)
        self.pdf.cell(0, 15, title, ln=True, align='C')
        self.reset_color()
        
        # Content
        self.pdf.set_xy(25, 80)
        self.pdf.set_font('helvetica', '', 12)
        paragraphs = content.split('\n\n')
        
        for paragraph in paragraphs:
            if paragraph.strip():
                lines = textwrap.wrap(paragraph, width=70)
                for line in lines:
                    self.pdf.multi_cell(160, 8, line)
                self.pdf.ln(5)
                
        self.add_footer()
        
    def generate(self, filename="enhanced_document.pdf"):
        """Generate and save the PDF file"""
        # Add final footer to all pages
        for i in range(1, self.pdf.page_no() + 1):
            self.pdf.page = i
            self.add_footer()
            
        self.pdf.output(filename)
        print(f"✓ Enhanced PDF successfully created: {filename}")
        
        # Get file information
        import os
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  File size: {size:,} bytes ({size/1024:.1f} KB)")
            print(f"  Pages generated: {self.pdf.page_no()}")
            
        return filename


def create_demo_pdf():
    """Create a demonstration PDF with all enhanced features"""
    
    # Initialize generator
    generator = EnhancedPDFGenerator("Advanced Report Generator Demo")
    
    # Add title page
    generator.add_title_page(
        title="Comprehensive Report 2024",
        subtitle="Advanced Data Analysis & Strategic Insights",
        author="Analytics Department"
    )
    
    # Define table of contents
    sections = [
        ("Executive Summary", 3),
        ("Financial Performance", 4),
        ("Market Analysis", 5),
        ("Operational Review", 6),
        ("Strategic Recommendations", 7),
        ("Technical Implementation", 8),
        ("Conclusion", 9)
    ]
    
    # Add table of contents
    generator.add_table_of_contents(sections)
    
    # Page 3: Executive Summary
    generator.add_section("1. Executive Summary", """
This comprehensive report provides a detailed analysis of our performance metrics,
strategic initiatives, and operational efficiency throughout the fiscal year 2024.

The document highlights key achievements, identifies areas for improvement,
and presents actionable recommendations for future growth and optimization.
Our analysis indicates strong performance across all major metrics with
exceptional results in market expansion and customer satisfaction.
    """)
    
    # Page 4: Financial Performance with bullet points
    financial_items = [
        "Revenue growth of 18.5% year-over-year",
        "Cost reduction of 12% through operational efficiencies", 
        "Profit margin improvement from 15% to 21%",
        "ROI on marketing campaigns: 285%",
        "Cash flow positive for 8 consecutive quarters",
        "Debt-to-equity ratio reduced to 0.45"
    ]
    generator.add_bulleted_list("2. Key Financial Metrics", financial_items)
    
    # Page 5: Market Analysis table
    market_headers = ["Region", "Market Share", "Growth Rate", "Competitors"]
    market_data = [
        ["North America", "32%", "+12.5%", "8"],
        ["Europe", "24%", "+8.2%", "12"],
        ["Asia Pacific", "28%", "+15.3%", "15"],
        ["South America", "18%", "+22.1%", "6"],
        ["Middle East", "14%", "+18.7%", "9"]
    ]
    generator.add_table("3. Regional Market Analysis", market_headers, market_data)
    
    # Page 6: Operational Review
    generator.add_section("4. Operational Efficiency", """
Our operational review reveals significant improvements in process optimization
and resource allocation. Key initiatives implemented this year include:

• Automated workflow systems reducing manual processing time by 65%
• Cloud migration completed ahead of schedule with 99.9% uptime
• Supply chain optimization reducing delivery times by 40%
• Customer support response time improved from 24h to 4h average

These improvements have resulted in enhanced customer satisfaction scores
and operational cost savings exceeding our annual targets.
    """)
    
    # Page 7: Strategic Recommendations
    strategy_items = [
        "Expand into emerging markets in Southeast Asia",
        "Invest in AI-driven customer analytics platform",
        "Implement blockchain for supply chain transparency",
        "Develop strategic partnerships with tech innovators",
        "Enhance sustainability initiatives with carbon-neutral goals",
        "Launch new product line targeting Gen-Z demographic"
    ]
    generator.add_bulleted_list("5. Strategic Recommendations", strategy_items)
    
    # Page 8: Technical Implementation with code example
    code_example = '''def analyze_performance(data):
    """
    Advanced performance analysis function
    """
    import pandas as pd
    import numpy as np
    
    # Calculate key metrics
    metrics = {
        'mean': np.mean(data),
        'std': np.std(data),
        'min': np.min(data),
        'max': np.max(data),
        'percentile_25': np.percentile(data, 25),
        'percentile_75': np.percentile(data, 75)
    }
    
    return pd.DataFrame([metrics])
    
# Example usage
performance_data = [245, 312, 289, 301, 278, 295]
results = analyze_performance(performance_data)
print(results)'''
    
    generator.add_code_block("6. Technical Implementation Example", code_example, "python")
    
    # Page 9: Chart Summary
    chart_summary = {
        "Customer Satisfaction": "92.4%",
        "Employee Engagement": "88.7%",
        "Operational Efficiency": "94.2%",
        "Market Penetration": "78.9%",
        "Revenue Growth": "18.5%",
        "Cost Reduction": "12.0%"
    }
    generator.add_chart_summary("7. Performance Metrics Summary", chart_summary)
    
    # Page 10: Conclusion
    conclusion_text = """
This report demonstrates our strong performance throughout 2024 and outlines
a clear strategic path forward. The data indicates sustained growth potential
across all business units.

Key takeaways include:
• Continued investment in technological innovation is essential
• Market expansion presents significant growth opportunities
• Operational efficiencies have exceeded expectations
• Customer satisfaction remains a key competitive advantage

We recommend quarterly review of these metrics and continuous monitoring
of market trends to maintain our competitive edge in the coming year.
    """
    
    generator.add_conclusion("8. Final Conclusions & Next Steps", conclusion_text)
    
    # Generate the PDF
    return generator.generate()


if __name__ == "__main__":
    print("=" * 60)
    print("Enhanced PDF Generator - Creating Advanced Document")
    print("=" * 60)
    
    print("\nGenerating PDF with advanced features...")
    print("Features include:")
    print("  • Professional title page with styling")
    print("  • Hierarchical section headings")
    print("  • Formatted bulleted lists")
    print("  • Styled tables with alternating colors")
    print("  • Code blocks with syntax highlighting")
    print("  • Chart/statistics summaries")
    print("  • Conclusion section with emphasis")
    print("  • Headers and footers on all pages")
    print("  • Multi-page layout with proper pagination")
    
    try:
        filename = create_demo_pdf()
        print(f"\n✅ Successfully created: {filename}")
        print("\nDocument includes:")
        print("  - 9+ pages of comprehensive content")
        print("  - Professional formatting throughout")
        print("  - Multiple content types (text, lists, tables, code)")
        print("  - Color-coded elements for better readability")
        print("  - Consistent header/footer styling")
        
    except Exception as e:
        print(f"\n❌ Error creating PDF: {e}")
        print("\nAttempting fallback to simpler PDF generation...")
        try:
            # Simple fallback
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, 'Fallback PDF Document', ln=True, align='C')
            pdf.ln(10)
            pdf.set_font('Arial', '', 12)
            pdf.multi_cell(0, 10, 'Enhanced PDF generation failed. Basic PDF created.')
            pdf.output('fallback_enhanced.pdf')
            print("✓ Created fallback PDF: fallback_enhanced.pdf")
        except Exception as e2:
            print(f"❌ Fallback also failed: {e2}")