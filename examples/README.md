# Examples

This directory contains examples demonstrating how to use wiki-notion.

## Running the Demo

To see wiki-notion in action with sample content:

```bash
cd /home/runner/work/wiki-notion/wiki-notion
python -c "
import sys
sys.path.insert(0, '.')
exec(open('examples/demo.py').read())
"
```

Or if you have installed wiki-notion:

```bash
python examples/demo.py
```

## What the Demo Does

The demo script demonstrates all key features:

1. **Markdown Cleaning** - Cleans markdown content for optimal Notion import
2. **HTML Generation** - Converts markdown to styled HTML
3. **Table of Contents** - Automatically generates navigation from headers
4. **Link Extraction** - Identifies all links in the document
5. **File Combination** - Merges multiple markdown files into one document

## Output Files

After running the demo, you'll find several files in `examples/output/`:

- `awesome_python.md` - Cleaned markdown file
- `awesome_python.html` - Styled HTML file
- `awesome_python_with_toc.md` - Markdown with table of contents
- `combined.md` - Example of multiple files combined

## Using with Real GitHub Repositories

Once you're ready to use with actual GitHub repos:

```bash
# Convert a repository
python -m wiki_notion.cli convert https://github.com/owner/repo

# Get repository info first
python -m wiki_notion.cli info https://github.com/owner/repo

# Convert with options
python -m wiki_notion.cli convert https://github.com/owner/repo --combine --toc --format html
```

## Importing to Notion

1. Open the generated HTML or Markdown files
2. In Notion, click "Import" from the sidebar
3. Choose "Markdown & CSV" or "HTML"
4. Select your generated file
5. Notion will create a new page with your content!

The HTML files have clean, professional styling that works great in Notion.
