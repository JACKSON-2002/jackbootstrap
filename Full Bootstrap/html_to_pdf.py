"""
Bootstrap Website HTML to PDF Converter
Creates a comprehensive PDF from all HTML files in the Bootstrap project
"""

import os
import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime

def install_package(package_name):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def create_combined_html():
    """Create a single HTML file combining all Bootstrap pages"""
    folder_path = Path(__file__).parent
    output_html = folder_path / "combined_bootstrap.html"
    
    # HTML files to include
    html_files = [
        'index.html',
        'layout.html', 
        'components.html',
        'content.html',
        'forms.html',
        'helpers.html'
    ]
    
    # Start building the combined HTML
    combined_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bootstrap 5.3 Complete Learning Guide</title>
    
    <!-- Bootstrap 5.3 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Bootstrap Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
    
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; }
        .pdf-page-break { page-break-before: always; }
        .pdf-title { font-size: 2.5em; color: #0d6efd; text-align: center; margin: 2em 0; }
        .pdf-subtitle { font-size: 1.8em; color: #6f42c1; margin: 1.5em 0; }
        .pdf-section { margin: 2em 0; padding: 1em; border-left: 4px solid #0d6efd; }
        .code-block { background: #f8f9fa; border: 1px solid #dee2e6; padding: 1em; border-radius: 0.375rem; font-family: monospace; }
        .toc { background: #f8f9fa; padding: 2em; border-radius: 0.5rem; margin: 2em 0; }
        .toc ul { list-style-type: none; padding-left: 1em; }
        .toc a { text-decoration: none; color: #0d6efd; }
        .navbar, .sidebar, script { display: none !important; }
        @media print {
            .navbar, .sidebar, script { display: none !important; }
            .pdf-page-break { page-break-before: always; }
        }
    </style>
</head>
<body>

<div class="container-fluid p-4">
    <!-- Cover Page -->
    <div class="text-center">
        <h1 class="pdf-title">Bootstrap 5.3 Complete Learning Guide</h1>
        <h2 class="pdf-subtitle">Comprehensive Examples and Documentation</h2>
        <p class="lead">This document contains a complete collection of Bootstrap 5.3 components, utilities, and examples.</p>
        <p><strong>Generated on:</strong> """ + datetime.now().strftime("%B %d, %Y") + """</p>
        <p><strong>Bootstrap Version:</strong> 5.3.2</p>
    </div>

    <!-- Table of Contents -->
    <div class="toc pdf-page-break">
        <h2>Table of Contents</h2>
        <ul>
            <li><a href="#main-examples">1. Main Examples & Overview</a></li>
            <li><a href="#layout-system">2. Layout System & Grid</a></li>
            <li><a href="#components">3. Components Collection</a></li>
            <li><a href="#content-typography">4. Content & Typography</a></li>
            <li><a href="#forms-controls">5. Forms & Input Controls</a></li>
            <li><a href="#helpers-utilities">6. Helpers & Utility Classes</a></li>
        </ul>
    </div>
"""
    
    # Process each HTML file
    for i, filename in enumerate(html_files, 1):
        file_path = folder_path / filename
        if file_path.exists():
            print(f"Processing {filename}...")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract title
                title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
                page_title = title_match.group(1) if title_match else filename.replace('.html', '').title()
                
                # Extract main content (between main tags or body content)
                main_content = ""
                
                # Try to extract main content
                main_match = re.search(r'<main[^>]*>(.*?)</main>', content, re.DOTALL | re.IGNORECASE)
                if main_match:
                    main_content = main_match.group(1)
                else:
                    # Fallback: extract body content and clean it
                    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
                    if body_match:
                        body_content = body_match.group(1)
                        # Remove navigation and script elements
                        body_content = re.sub(r'<nav[^>]*>.*?</nav>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
                        body_content = re.sub(r'<script[^>]*>.*?</script>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
                        main_content = body_content
                
                # Clean up the content
                main_content = re.sub(r'<!--.*?-->', '', main_content, flags=re.DOTALL)
                main_content = re.sub(r'data-bs-[^=]*="[^"]*"', '', main_content)
                
                # Add to combined content
                section_id = filename.replace('.html', '').replace('_', '-')
                combined_content += f"""
    <div class="pdf-page-break">
        <div id="{section_id}" class="pdf-section">
            <h1 class="pdf-title">{page_title}</h1>
            <p><em>Source: {filename}</em></p>
            {main_content}
        </div>
    </div>
"""
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                combined_content += f"""
    <div class="pdf-page-break">
        <div class="pdf-section">
            <h1 class="pdf-title">Error Processing {filename}</h1>
            <p>Could not process this file: {e}</p>
        </div>
    </div>
"""
    
    # Add CSS content
    css_file = folder_path / "styles.css"
    if css_file.exists():
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            combined_content += f"""
    <div class="pdf-page-break">
        <div class="pdf-section">
            <h1 class="pdf-title">Custom CSS Styles</h1>
            <p><em>Source: styles.css</em></p>
            <div class="code-block">
                <pre>{css_content[:5000]}{'...' if len(css_content) > 5000 else ''}</pre>
            </div>
        </div>
    </div>
"""
        except Exception as e:
            print(f"Error processing CSS file: {e}")
    
    # Close HTML
    combined_content += """
</div>

<!-- Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""
    
    # Write combined HTML file
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(combined_content)
    
    print(f"Combined HTML created: {output_html}")
    return output_html

def html_to_pdf_simple(html_file, pdf_file):
    """Convert HTML to PDF using simple method"""
    try:
        # Try using wkhtmltopdf if available
        cmd = [
            'wkhtmltopdf',
            '--page-size', 'A4',
            '--margin-top', '0.75in',
            '--margin-right', '0.75in', 
            '--margin-bottom', '0.75in',
            '--margin-left', '0.75in',
            '--enable-local-file-access',
            str(html_file),
            str(pdf_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            print(f"wkhtmltopdf error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("wkhtmltopdf not found. Trying alternative method...")
        return False

def html_to_pdf_weasyprint(html_file, pdf_file):
    """Convert HTML to PDF using weasyprint"""
    try:
        # Install weasyprint if not available
        try:
            import weasyprint
        except ImportError:
            print("Installing weasyprint...")
            if not install_package("weasyprint"):
                return False
            import weasyprint
        
        # Convert HTML to PDF
        weasyprint.HTML(filename=str(html_file)).write_pdf(str(pdf_file))
        return True
        
    except Exception as e:
        print(f"Weasyprint error: {e}")
        return False

def html_to_pdf_playwright(html_file, pdf_file):
    """Convert HTML to PDF using playwright"""
    try:
        # Install playwright if not available
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("Installing playwright...")
            if not install_package("playwright"):
                return False
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
            from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{html_file.absolute()}")
            page.pdf(path=str(pdf_file), format="A4", margin={"top": "1in", "bottom": "1in", "left": "0.75in", "right": "0.75in"})
            browser.close()
        
        return True
        
    except Exception as e:
        print(f"Playwright error: {e}")
        return False

def main():
    """Main function to generate the PDF"""
    print("Bootstrap Website PDF Generator")
    print("=" * 40)
    
    # Create combined HTML
    html_file = create_combined_html()
    pdf_file = Path(__file__).parent / "learnBoot.pdf"
    
    print(f"Converting to PDF: {pdf_file}")
    
    # Try different PDF conversion methods
    methods = [
        ("wkhtmltopdf", html_to_pdf_simple),
        ("weasyprint", html_to_pdf_weasyprint),
        ("playwright", html_to_pdf_playwright)
    ]
    
    success = False
    for method_name, method_func in methods:
        print(f"Trying {method_name}...")
        if method_func(html_file, pdf_file):
            print(f"✅ PDF generated successfully using {method_name}: {pdf_file}")
            success = True
            break
        else:
            print(f"❌ {method_name} failed")
    
    if not success:
        print("\n❌ All PDF conversion methods failed.")
        print(f"📄 However, you can open {html_file} in a browser and use 'Print to PDF'")
        print("   Make sure to:")
        print("   - Select 'More settings'")
        print("   - Choose 'Paper size: A4'")
        print("   - Set margins to 'Minimum' or 'Custom'")
        print("   - Check 'Background graphics'")
        print("   - Save as 'learnBoot.pdf'")
    
    # Clean up temporary HTML file
    try:
        os.remove(html_file)
    except:
        pass

if __name__ == "__main__":
    main()
