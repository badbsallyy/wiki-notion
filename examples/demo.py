#!/usr/bin/env python3
"""
Example script demonstrating wiki-notion converter usage
This example works with local markdown content to demonstrate the tool's functionality
"""

from wiki_notion.converter import NotionConverter
from pathlib import Path

def main():
    print("🎯 wiki-notion Example Demo\n")
    print("=" * 60)
    
    # Sample markdown content (simulating a GitHub wiki/list)
    sample_content = """# Awesome Python Resources

A curated list of awesome Python frameworks, libraries, and resources.

## Web Frameworks

- **Django** - High-level Python web framework
  - [Documentation](https://docs.djangoproject.com/)
  - GitHub: [django/django](https://github.com/django/django)
  
- **Flask** - Lightweight WSGI web application framework
  - [Documentation](https://flask.palletsprojects.com/)
  - GitHub: [pallets/flask](https://github.com/pallets/flask)

## Data Science

- **NumPy** - Fundamental package for numerical computing
- **Pandas** - Data manipulation and analysis library
- **Matplotlib** - Comprehensive visualization library

## Machine Learning

1. **TensorFlow** - End-to-end open source platform for ML
2. **PyTorch** - Open source machine learning library
3. **Scikit-learn** - Simple and efficient tools for data mining

## Code Examples

```python
# Hello World in Python
print("Hello, World!")

def greet(name):
    return f"Hello, {name}!"
```

## Tables

| Library | Purpose | Stars |
|---------|---------|-------|
| Django  | Web     | 70k+  |
| Flask   | Web     | 60k+  |
| NumPy   | Math    | 25k+  |

## Contributing

Contributions are welcome! Please read the contributing guidelines first.
"""
    
    # Initialize converter
    converter = NotionConverter()
    
    # Create output directory
    output_dir = Path("examples/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n📝 Converting sample content...\n")
    
    # 1. Clean markdown for Notion
    print("1️⃣  Cleaning markdown for Notion...")
    cleaned_md = converter.clean_markdown_for_notion(sample_content)
    md_file = output_dir / "awesome_python.md"
    md_file.write_text(cleaned_md, encoding='utf-8')
    print(f"   ✅ Saved: {md_file}")
    
    # 2. Generate HTML
    print("\n2️⃣  Generating HTML...")
    html_content = converter.markdown_to_html(sample_content, "Awesome Python Resources")
    html_file = output_dir / "awesome_python.html"
    html_file.write_text(html_content, encoding='utf-8')
    print(f"   ✅ Saved: {html_file}")
    
    # 3. Generate with Table of Contents
    print("\n3️⃣  Generating with Table of Contents...")
    toc = converter.create_table_of_contents(sample_content)
    content_with_toc = toc + "\n" + sample_content
    toc_file = output_dir / "awesome_python_with_toc.md"
    toc_file.write_text(content_with_toc, encoding='utf-8')
    print(f"   ✅ Saved: {toc_file}")
    
    # 4. Extract links
    print("\n4️⃣  Extracting links...")
    links = converter.extract_links_from_markdown(sample_content)
    print(f"   Found {len(links)} links:")
    for link in links[:3]:  # Show first 3
        print(f"   - {link['text']}: {link['url']}")
    if len(links) > 3:
        print(f"   ... and {len(links) - 3} more")
    
    # 5. Combine multiple files demo
    print("\n5️⃣  Combining multiple files...")
    files = [
        {'name': 'README.md', 'content': sample_content},
        {'name': 'docs/guide.md', 'content': '## Installation\n\nRun `pip install awesome-python`'},
    ]
    combined = converter.combine_multiple_files(files)
    combined_file = output_dir / "combined.md"
    combined_file.write_text(combined, encoding='utf-8')
    print(f"   ✅ Saved: {combined_file}")
    
    print("\n" + "=" * 60)
    print("\n✨ Demo complete! Files generated in: examples/output/")
    print("\n💡 To use with GitHub repositories:")
    print("   python -m wiki_notion.cli convert https://github.com/owner/repo")
    print("\n📥 Import these files to Notion:")
    print("   1. Open Notion")
    print("   2. Click 'Import' in the sidebar")
    print("   3. Select 'Markdown & CSV' or 'HTML'")
    print("   4. Upload the generated files")
    print("\n🎉 Enjoy your wiki in Notion!")

if __name__ == "__main__":
    main()
