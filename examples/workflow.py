#!/usr/bin/env python3
"""
Complete workflow example for wiki-notion

This example demonstrates a typical workflow:
1. Check repository information
2. Convert to multiple formats
3. Show what files were created
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wiki_notion.converter import NotionConverter
from pathlib import Path


def workflow_demo():
    """Demonstrate a complete workflow"""
    
    print("=" * 70)
    print("   WIKI-NOTION WORKFLOW DEMONSTRATION")
    print("=" * 70)
    
    # Sample content representing a GitHub wiki or awesome list
    sample_wiki_content = """# Developer Resources Wiki

Welcome to our curated collection of developer resources!

## Programming Languages

### Python
- **Django** - The web framework for perfectionists with deadlines
  - [Official Site](https://www.djangoproject.com/)
  - Best for: Complex web applications
  
- **Flask** - Lightweight and flexible web framework
  - [Official Site](https://flask.palletsprojects.com/)
  - Best for: Small to medium applications

### JavaScript
- **React** - A JavaScript library for building user interfaces
- **Vue.js** - The progressive JavaScript framework
- **Node.js** - JavaScript runtime built on Chrome's V8

## Development Tools

### Version Control
1. **Git** - Distributed version control system
2. **GitHub** - Web-based hosting for Git repositories
3. **GitLab** - DevOps platform with Git repository management

### Code Editors
| Editor | Language | License |
|--------|----------|---------|
| VS Code | TypeScript | MIT |
| Sublime | C++/Python | Proprietary |
| Vim | C | Open Source |

## Learning Resources

> "The best way to learn is by doing" - Anonymous

### Online Courses
- Coursera - University-level courses
- Udemy - Practical skill-based learning
- edX - Free online courses from top universities

### Books
```
📚 Recommended Reading List:
- Clean Code by Robert Martin
- The Pragmatic Programmer
- Design Patterns (Gang of Four)
```

## Contributing

Want to add more resources? Check our [contributing guidelines](CONTRIBUTING.md).

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Add your resources
4. Submit a pull request

## License

MIT License - feel free to use these resources!
"""

    additional_content = """# Getting Started Guide

## Installation

Follow these steps to get started:

1. Clone the repository
2. Install dependencies
3. Run the application

## Configuration

Create a config file with your settings:

```yaml
app:
  name: MyApp
  version: 1.0
  debug: false
```

## Usage

Run the application:

```bash
python app.py --config config.yaml
```
"""

    # Initialize converter
    converter = NotionConverter()
    output_dir = Path("examples/workflow_output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n📋 STEP 1: Analyzing Content")
    print("-" * 70)
    
    # Extract information
    links = converter.extract_links_from_markdown(sample_wiki_content)
    print(f"   Found {len(links)} links in the content")
    print(f"   Content length: {len(sample_wiki_content)} characters")
    
    # Show a few links
    print("\n   Sample links:")
    for link in links[:3]:
        print(f"   - {link['text']}: {link['url']}")
    
    print("\n📝 STEP 2: Generating Markdown Files")
    print("-" * 70)
    
    # Clean and save markdown
    cleaned = converter.clean_markdown_for_notion(sample_wiki_content)
    md_file = output_dir / "developer_resources.md"
    md_file.write_text(cleaned, encoding='utf-8')
    print(f"   ✅ Created: {md_file.name}")
    
    # Create markdown with TOC
    toc = converter.create_table_of_contents(sample_wiki_content)
    with_toc = toc + "\n" + sample_wiki_content
    toc_file = output_dir / "developer_resources_toc.md"
    toc_file.write_text(with_toc, encoding='utf-8')
    print(f"   ✅ Created: {toc_file.name}")
    
    print("\n🎨 STEP 3: Generating HTML Files")
    print("-" * 70)
    
    # Generate HTML
    html = converter.markdown_to_html(sample_wiki_content, "Developer Resources Wiki")
    html_file = output_dir / "developer_resources.html"
    html_file.write_text(html, encoding='utf-8')
    print(f"   ✅ Created: {html_file.name}")
    
    # Generate HTML with TOC
    html_toc = converter.markdown_to_html(with_toc, "Developer Resources Wiki (with TOC)")
    html_toc_file = output_dir / "developer_resources_toc.html"
    html_toc_file.write_text(html_toc, encoding='utf-8')
    print(f"   ✅ Created: {html_toc_file.name}")
    
    print("\n📦 STEP 4: Combining Multiple Documents")
    print("-" * 70)
    
    # Combine multiple files
    files = [
        {'name': 'README.md', 'content': sample_wiki_content},
        {'name': 'GETTING_STARTED.md', 'content': additional_content},
    ]
    combined = converter.combine_multiple_files(files)
    combined_file = output_dir / "complete_wiki.md"
    combined_file.write_text(combined, encoding='utf-8')
    print(f"   ✅ Created: {combined_file.name}")
    
    # Combined HTML
    combined_html = converter.markdown_to_html(combined, "Complete Wiki")
    combined_html_file = output_dir / "complete_wiki.html"
    combined_html_file.write_text(combined_html, encoding='utf-8')
    print(f"   ✅ Created: {combined_html_file.name}")
    
    print("\n📊 STEP 5: Summary")
    print("-" * 70)
    print(f"   Output directory: {output_dir.absolute()}")
    print(f"   Files created: 6")
    print("\n   Markdown files:")
    for f in output_dir.glob("*.md"):
        size = f.stat().st_size
        print(f"      - {f.name} ({size:,} bytes)")
    print("\n   HTML files:")
    for f in output_dir.glob("*.html"):
        size = f.stat().st_size
        print(f"      - {f.name} ({size:,} bytes)")
    
    print("\n" + "=" * 70)
    print("   WORKFLOW COMPLETE!")
    print("=" * 70)
    print("\n💡 Next Steps:")
    print("   1. Open the HTML files in a browser to preview")
    print("   2. Import the Markdown or HTML files to Notion")
    print("   3. Try with a real GitHub repository:")
    print("      python -m wiki_notion.cli convert https://github.com/owner/repo")
    print("\n📥 To import to Notion:")
    print("   • In Notion, click 'Import' → 'Markdown & CSV' or 'HTML'")
    print("   • Select any of the generated files")
    print("   • Notion will create a new page with your content!")
    print("\n✨ Enjoy your wiki in Notion!")
    print()


if __name__ == "__main__":
    try:
        workflow_demo()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
