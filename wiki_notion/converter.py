"""
Converter module to transform markdown/HTML to Notion-friendly formats
"""

import markdown
import re
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import html2text


class NotionConverter:
    """Convert content to Notion-friendly formats"""
    
    def __init__(self):
        """Initialize the converter"""
        self.html2text_converter = html2text.HTML2Text()
        self.html2text_converter.body_width = 0  # Don't wrap text
        self.html2text_converter.ignore_links = False
        self.html2text_converter.ignore_images = False
        
    def markdown_to_html(self, md_content: str, title: Optional[str] = None) -> str:
        """
        Convert Markdown to clean HTML suitable for Notion
        
        Args:
            md_content: Markdown content
            title: Optional title for the document
            
        Returns:
            HTML string
        """
        # Convert markdown to HTML
        html_content = markdown.markdown(
            md_content,
            extensions=[
                'extra',
                'codehilite',
                'tables',
                'toc',
                'fenced_code',
            ]
        )
        
        # Wrap in basic HTML structure
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title or 'Converted Document'}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Courier New', monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f4f4f4;
            font-weight: bold;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            margin: 0;
            padding-left: 20px;
            color: #666;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
        }}
        ul, ol {{
            padding-left: 30px;
        }}
        li {{
            margin: 4px 0;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
        
        return html_template
    
    def clean_markdown_for_notion(self, md_content: str) -> str:
        """
        Clean and optimize Markdown for Notion import
        
        Notion has specific requirements for Markdown import:
        - Remove complex HTML tags
        - Simplify formatting
        - Ensure proper list formatting
        
        Args:
            md_content: Raw markdown content
            
        Returns:
            Cleaned markdown string
        """
        # Remove HTML comments
        md_content = re.sub(r'<!--.*?-->', '', md_content, flags=re.DOTALL)
        
        # Convert HTML tags to markdown equivalents where possible
        # Remove complex HTML that Notion might not support
        md_content = re.sub(r'<details>.*?</details>', '', md_content, flags=re.DOTALL)
        md_content = re.sub(r'<summary>.*?</summary>', '', md_content, flags=re.DOTALL)
        
        # Ensure proper spacing around headers
        md_content = re.sub(r'\n(#{1,6}\s)', r'\n\n\1', md_content)
        md_content = re.sub(r'(#{1,6}\s.*?)\n', r'\1\n\n', md_content)
        
        # Clean up multiple consecutive blank lines
        md_content = re.sub(r'\n{3,}', '\n\n', md_content)
        
        return md_content.strip()
    
    def extract_links_from_markdown(self, md_content: str) -> List[Dict[str, str]]:
        """
        Extract all links from markdown content
        
        Args:
            md_content: Markdown content
            
        Returns:
            List of dictionaries with 'text' and 'url' keys
        """
        # Match markdown links: [text](url)
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        links = []
        
        for match in re.finditer(link_pattern, md_content):
            links.append({
                'text': match.group(1),
                'url': match.group(2)
            })
        
        return links
    
    def create_table_of_contents(self, md_content: str) -> str:
        """
        Generate a table of contents from markdown headers
        
        Args:
            md_content: Markdown content
            
        Returns:
            Markdown table of contents
        """
        headers = []
        
        # Match headers (# Header)
        header_pattern = r'^(#{1,6})\s+(.+?)$'
        
        for line in md_content.split('\n'):
            match = re.match(header_pattern, line)
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                # Create anchor (simplified)
                anchor = re.sub(r'[^\w\s-]', '', text.lower())
                anchor = re.sub(r'[\s]+', '-', anchor)
                
                headers.append({
                    'level': level,
                    'text': text,
                    'anchor': anchor
                })
        
        if not headers:
            return ""
        
        toc = "## Table of Contents\n\n"
        for header in headers:
            indent = "  " * (header['level'] - 1)
            toc += f"{indent}- [{header['text']}](#{header['anchor']})\n"
        
        return toc + "\n"
    
    def html_to_markdown(self, html_content: str) -> str:
        """
        Convert HTML back to Markdown
        
        Args:
            html_content: HTML content
            
        Returns:
            Markdown string
        """
        return self.html2text_converter.handle(html_content)
    
    def combine_multiple_files(self, files_content: List[Dict[str, str]]) -> str:
        """
        Combine multiple markdown files into one document
        
        Args:
            files_content: List of dicts with 'name' and 'content' keys
            
        Returns:
            Combined markdown content
        """
        combined = ""
        
        for file_info in files_content:
            name = file_info.get('name', 'Unknown')
            content = file_info.get('content', '')
            
            # Add file name as header
            combined += f"\n\n---\n\n# {name}\n\n{content}\n"
        
        return combined.strip()
