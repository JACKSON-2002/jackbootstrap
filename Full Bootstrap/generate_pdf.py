#!/usr/bin/env python3
"""
Bootstrap Website PDF Generator
Generates a comprehensive PDF document from all HTML files in the Bootstrap project
"""

import os
import sys
import subprocess
from pathlib import Path
import re
from datetime import datetime

# Install reportlab if not available
try:
    import reportlab
except ImportError:
    print("Installing required dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black, blue, red, green, orange, purple, brown
from reportlab.lib import colors

class BootstrapPDFGenerator:
    def __init__(self, folder_path):
        self.folder_path = Path(folder_path)
        self.pdf_path = self.folder_path / "learnBoot.pdf"
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        self.story = []
        
    def setup_custom_styles(self):
        """Setup custom paragraph styles for the PDF"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1  # Center alignment
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=20,
            textColor=colors.blue,
            alignment=1
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=15,
            spaceBefore=15,
            textColor=colors.darkblue,
            leftIndent=0
        ))
        
        # Subsection style
        self.styles.add(ParagraphStyle(
            name='SubsectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=12,
            textColor=colors.blue,
            leftIndent=10
        ))
        
        # Code style
        self.styles.add(ParagraphStyle(
            name='Code',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Courier',
            leftIndent=20,
            rightIndent=20,
            spaceAfter=10,
            spaceBefore=5,
            textColor=colors.darkred,
            backColor=colors.lightgrey
        ))
        
        # CSS Classes style
        self.styles.add(ParagraphStyle(
            name='CSSClasses',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Courier',
            leftIndent=30,
            spaceAfter=8,
            textColor=colors.darkgreen
        ))

    def clean_html_content(self, html_content):
        """Extract meaningful content from HTML and clean it up"""
        # Remove HTML comments
        html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
        
        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
        title = title_match.group(1) if title_match else "Bootstrap Page"
        
        # Extract main content sections
        sections = []
        
        # Find all sections with IDs
        section_pattern = r'<section[^>]*id=["\']([^"\']+)["\'][^>]*>(.*?)</section>'
        section_matches = re.findall(section_pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        for section_id, section_content in section_matches:
            section_title = section_id.replace('-', ' ').title()
            
            # Extract h2, h3 headings
            headings = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', section_content, re.IGNORECASE)
            
            # Extract code examples
            code_blocks = re.findall(r'<code[^>]*class=["\']css-code["\'][^>]*>(.*?)</code>', section_content, re.DOTALL | re.IGNORECASE)
            
            # Extract meaningful text content
            text_content = re.sub(r'<[^>]+>', ' ', section_content)
            text_content = ' '.join(text_content.split())
            
            sections.append({
                'id': section_id,
                'title': section_title,
                'headings': headings,
                'code_blocks': code_blocks,
                'content': text_content[:500] + '...' if len(text_content) > 500 else text_content
            })
        
        return title, sections

    def add_cover_page(self):
        """Add a cover page to the PDF"""
        self.story.append(Spacer(1, 2*inch))
        
        # Main title
        self.story.append(Paragraph("Bootstrap 5.3 Complete Learning Guide", self.styles['CustomTitle']))
        self.story.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        self.story.append(Paragraph("Comprehensive Examples and Documentation", self.styles['CustomSubtitle']))
        self.story.append(Spacer(1, 0.3*inch))
        
        # Description
        description = """
        This document contains a complete collection of Bootstrap 5.3 components, utilities, 
        and examples. It covers everything from basic layout systems to advanced components 
        like modals, carousels, and form controls. Each section includes practical examples 
        and the corresponding CSS classes used.
        """
        self.story.append(Paragraph(description, self.styles['Normal']))
        self.story.append(Spacer(1, 1*inch))
        
        # Table of contents placeholder
        self.story.append(Paragraph("Contents Include:", self.styles['SectionHeader']))
        
        contents_list = [
            "• Layout System & Grid",
            "• Typography & Text Utilities", 
            "• Buttons & Button Groups",
            "• Navigation Components",
            "• Cards & Content Containers",
            "• Forms & Input Controls",
            "• Modals & Overlays",
            "• Alerts & Notifications",
            "• Tables & Data Display",
            "• Helper Utilities",
            "• Advanced Components",
            "• Code Examples & CSS Classes"
        ]
        
        for item in contents_list:
            self.story.append(Paragraph(item, self.styles['Normal']))
        
        self.story.append(Spacer(1, 1*inch))
        
        # Generation info
        generation_date = datetime.now().strftime("%B %d, %Y")
        self.story.append(Paragraph(f"Generated on: {generation_date}", self.styles['Normal']))
        self.story.append(Paragraph("Bootstrap Version: 5.3.2", self.styles['Normal']))
        
        self.story.append(PageBreak())

    def process_html_file(self, file_path):
        """Process a single HTML file and add its content to the PDF"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            title, sections = self.clean_html_content(html_content)
            
            # Add page title
            self.story.append(Paragraph(title, self.styles['CustomTitle']))
            self.story.append(Spacer(1, 0.3*inch))
            
            # Add file info
            self.story.append(Paragraph(f"Source File: {file_path.name}", self.styles['Normal']))
            self.story.append(Spacer(1, 0.2*inch))
            
            # Process each section
            for section in sections:
                # Section title
                self.story.append(Paragraph(section['title'], self.styles['SectionHeader']))
                
                # Section content
                if section['content'].strip():
                    # Split long content into smaller paragraphs
                    content_parts = section['content'].split('. ')
                    for part in content_parts[:3]:  # Limit to first 3 sentences
                        if part.strip():
                            self.story.append(Paragraph(part.strip() + '.', self.styles['Normal']))
                
                # Add headings found in the section
                for heading in section['headings'][:3]:  # Limit to first 3 headings
                    clean_heading = re.sub(r'<[^>]+>', '', heading).strip()
                    if clean_heading:
                        self.story.append(Paragraph(clean_heading, self.styles['SubsectionHeader']))
                
                # Add code blocks
                for code_block in section['code_blocks'][:2]:  # Limit to first 2 code blocks
                    clean_code = re.sub(r'<[^>]+>', '\n', code_block)
                    clean_code = '\n'.join(line.strip() for line in clean_code.split('\n') if line.strip())
                    if clean_code:
                        self.story.append(Paragraph("CSS Classes:", self.styles['SubsectionHeader']))
                        self.story.append(Paragraph(clean_code, self.styles['CSSClasses']))
                
                self.story.append(Spacer(1, 0.2*inch))
            
            self.story.append(PageBreak())
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    def add_css_summary(self):
        """Add a summary of the CSS file"""
        css_file = self.folder_path / "styles.css"
        if css_file.exists():
            try:
                with open(css_file, 'r', encoding='utf-8') as f:
                    css_content = f.read()
                
                self.story.append(Paragraph("Custom CSS Styles", self.styles['CustomTitle']))
                self.story.append(Spacer(1, 0.3*inch))
                
                # Extract CSS rules
                css_rules = re.findall(r'([.#][^{]+)\s*{([^}]+)}', css_content)
                
                for selector, rules in css_rules[:20]:  # Limit to first 20 rules
                    clean_selector = selector.strip()
                    clean_rules = rules.strip().replace('\n', ' ')
                    
                    self.story.append(Paragraph(f"Selector: {clean_selector}", self.styles['SubsectionHeader']))
                    self.story.append(Paragraph(clean_rules, self.styles['Code']))
                    self.story.append(Spacer(1, 0.1*inch))
                
            except Exception as e:
                print(f"Error processing CSS file: {e}")

    def generate_pdf(self):
        """Generate the complete PDF document"""
        print("Generating Bootstrap Learning PDF...")
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            str(self.pdf_path),
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Add cover page
        self.add_cover_page()
        
        # Process all HTML files
        html_files = [
            'index.html',
            'layout.html', 
            'components.html',
            'content.html',
            'forms.html',
            'helpers.html'
        ]
        
        for filename in html_files:
            file_path = self.folder_path / filename
            if file_path.exists():
                print(f"Processing {filename}...")
                self.process_html_file(file_path)
            else:
                print(f"Warning: {filename} not found")
        
        # Add CSS summary
        self.add_css_summary()
        
        # Build the PDF
        print("Building PDF document...")
        doc.build(self.story)
        print(f"PDF generated successfully: {self.pdf_path}")

def main():
    folder_path = Path(__file__).parent
    generator = BootstrapPDFGenerator(folder_path)
    generator.generate_pdf()

if __name__ == "__main__":
    main()
