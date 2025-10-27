# Usage Guide

Complete guide to using wiki-notion to convert GitHub repositories to Notion-friendly formats.

## Installation

### Quick Install

```bash
git clone https://github.com/badbsallyy/wiki-notion.git
cd wiki-notion
pip install -r requirements.txt
```

### Development Install

```bash
pip install -e .
```

## Basic Usage

### Method 1: Using the CLI Module

Since the tool may not be in your PATH, you can run it directly:

```bash
python -m wiki_notion.cli convert https://github.com/owner/repo
```

### Method 2: After Installing the Package

If you've installed with `pip install -e .`, and the scripts directory is in your PATH:

```bash
wiki-notion convert https://github.com/owner/repo
```

## Command Examples

### 1. Convert Repository README

The simplest use case - convert just the README:

```bash
python -m wiki_notion.cli convert https://github.com/owner/repo
```

This creates:
- `output/repo.md` - Cleaned markdown
- `output/repo.html` - Styled HTML

### 2. Combine All Markdown Files

For repositories with multiple markdown files (like wikis or documentation):

```bash
python -m wiki_notion.cli convert https://github.com/owner/repo --combine
```

This fetches all `.md` files and combines them into one document.

### 3. Add Table of Contents

Great for long documents:

```bash
python -m wiki_notion.cli convert https://github.com/owner/repo --toc
```

Automatically generates a clickable table of contents from headers.

### 4. Choose Output Format

```bash
# HTML only
python -m wiki_notion.cli convert https://github.com/owner/repo --format html

# Markdown only
python -m wiki_notion.cli convert https://github.com/owner/repo --format markdown

# Both (default)
python -m wiki_notion.cli convert https://github.com/owner/repo --format both
```

### 5. Custom Output Directory

```bash
python -m wiki_notion.cli convert https://github.com/owner/repo --output my_wikis
```

### 6. Use with Private Repositories

For private repos or to increase API rate limits:

```bash
# Set environment variable
export GITHUB_TOKEN=ghp_your_token_here
python -m wiki_notion.cli convert https://github.com/owner/private-repo

# Or pass directly
python -m wiki_notion.cli convert https://github.com/owner/private-repo --token ghp_your_token_here
```

### 7. Check Repository Info First

Before converting, see what's in the repo:

```bash
python -m wiki_notion.cli info https://github.com/owner/repo
```

This shows:
- Repository name and description
- Stars and forks
- List of all markdown files
- Topics/tags

## Real-World Examples

### Example 1: Convert an Awesome List

Awesome lists are perfect for this tool:

```bash
python -m wiki_notion.cli convert https://github.com/sindresorhus/awesome --combine --toc --output awesome-lists
```

### Example 2: Convert Project Documentation

```bash
python -m wiki_notion.cli convert https://github.com/python/cpython --combine --format markdown
```

### Example 3: Wiki Repository

```bash
python -m wiki_notion.cli convert https://github.com/owner/project-wiki --combine --toc
```

## Importing to Notion

After generating your files, import them to Notion:

### Import Markdown Files

1. Open Notion
2. Click **"Import"** in the left sidebar
3. Select **"Markdown & CSV"**
4. Choose your `.md` file
5. Notion creates a new page with your content!

### Import HTML Files

1. Open Notion
2. Click **"Import"** in the left sidebar
3. Select **"HTML"**
4. Choose your `.html` file
5. Notion creates a styled page!

## Tips and Best Practices

### 1. Start with Info

Always run `info` first to see what you're working with:

```bash
python -m wiki_notion.cli info https://github.com/owner/repo
```

### 2. Use Combine for Multi-File Repos

If a repo has many markdown files, use `--combine`:

```bash
python -m wiki_notion.cli convert https://github.com/owner/repo --combine
```

### 3. Add TOC for Long Documents

For repositories with lots of headers, add a table of contents:

```bash
python -m wiki_notion.cli convert https://github.com/owner/repo --toc
```

### 4. Choose the Right Format

- **HTML**: Better styling, preserves formatting
- **Markdown**: Lighter, easier to edit in Notion
- **Both**: Get both options and decide later

### 5. Handle Rate Limits

If you hit GitHub API rate limits, use a personal access token:

```bash
export GITHUB_TOKEN=your_token
```

### 6. Organize Your Exports

Use custom output directories for different projects:

```bash
python -m wiki_notion.cli convert https://github.com/owner/repo1 --output exports/project1
python -m wiki_notion.cli convert https://github.com/owner/repo2 --output exports/project2
```

## Troubleshooting

### Problem: "Module not found" error

**Solution**: Make sure you're in the wiki-notion directory and have installed dependencies:

```bash
cd wiki-notion
pip install -r requirements.txt
python -m wiki_notion.cli --help
```

### Problem: GitHub API rate limit exceeded

**Solution**: Use a GitHub personal access token:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token (only needs `public_repo` scope for public repos)
3. Use it:
   ```bash
   export GITHUB_TOKEN=your_token
   ```

### Problem: Repository not found

**Solution**: 
- Check the URL is correct
- For private repos, provide a token with appropriate permissions
- Ensure the repository actually exists

### Problem: No markdown files found

**Solution**: The repository might not have any markdown files. Try:

```bash
python -m wiki_notion.cli info https://github.com/owner/repo
```

to see what files are available.

### Problem: Conversion fails for large repos

**Solution**: The GitHub API has rate limits. Either:
- Use a personal access token (increases limits)
- Wait a bit and try again
- Convert just the README (don't use `--combine`)

## Advanced Usage

### Programmatic Usage

You can also use wiki-notion as a Python library:

```python
from wiki_notion.fetcher import GitHubRepoFetcher
from wiki_notion.converter import NotionConverter

# Fetch content
fetcher = GitHubRepoFetcher('https://github.com/owner/repo')
readme = fetcher.fetch_readme()

# Convert
converter = NotionConverter()
html = converter.markdown_to_html(readme, 'My Document')
cleaned_md = converter.clean_markdown_for_notion(readme)

# Save
with open('output.html', 'w') as f:
    f.write(html)
```

### Batch Processing

Process multiple repositories:

```bash
#!/bin/bash
repos=(
    "https://github.com/owner/repo1"
    "https://github.com/owner/repo2"
    "https://github.com/owner/repo3"
)

for repo in "${repos[@]}"; do
    python -m wiki_notion.cli convert "$repo" --combine --toc
done
```

## Use Cases

### 1. Personal Knowledge Management

Convert awesome lists and curated resources to your Notion workspace:

```bash
python -m wiki_notion.cli convert https://github.com/sindresorhus/awesome --combine
```

### 2. Documentation Backup

Save project documentation locally:

```bash
python -m wiki_notion.cli convert https://github.com/project/docs --combine --format both
```

### 3. Learning Resources

Collect learning resources from GitHub wikis:

```bash
python -m wiki_notion.cli convert https://github.com/educational/wiki --combine --toc
```

### 4. Research

Compile research resources and papers:

```bash
python -m wiki_notion.cli convert https://github.com/research/papers --combine
```

## Next Steps

- Try the demo: `python examples/demo.py`
- Check out example outputs in `examples/output/`
- Read the main README for more information
- Start converting your favorite GitHub repos!

## Questions or Issues?

If you run into problems or have questions, please open an issue on GitHub!
