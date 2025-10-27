# Quick Reference

One-page reference for wiki-notion commands.

## Installation

```bash
git clone https://github.com/badbsallyy/wiki-notion.git
cd wiki-notion
pip install -r requirements.txt
```

## Commands

### Convert Repository

```bash
python -m wiki_notion.cli convert REPO_URL [OPTIONS]
```

**Options:**
- `-o, --output PATH` - Output directory (default: output)
- `-f, --format [html|markdown|both]` - Output format (default: both)
- `-t, --token TOKEN` - GitHub token (or set GITHUB_TOKEN env var)
- `-c, --combine` - Combine all markdown files into one
- `--toc` - Add table of contents

### Get Repository Info

```bash
python -m wiki_notion.cli info REPO_URL [OPTIONS]
```

## Quick Examples

```bash
# Basic conversion
python -m wiki_notion.cli convert https://github.com/owner/repo

# Combine all files with TOC
python -m wiki_notion.cli convert https://github.com/owner/repo --combine --toc

# HTML only
python -m wiki_notion.cli convert https://github.com/owner/repo --format html

# With GitHub token
python -m wiki_notion.cli convert https://github.com/owner/repo --token YOUR_TOKEN

# Custom output directory
python -m wiki_notion.cli convert https://github.com/owner/repo --output my_exports

# Check repo first
python -m wiki_notion.cli info https://github.com/owner/repo
```

## Common Use Cases

| Use Case | Command |
|----------|---------|
| Convert awesome list | `python -m wiki_notion.cli convert URL --combine --toc` |
| Single README only | `python -m wiki_notion.cli convert URL` |
| Documentation wiki | `python -m wiki_notion.cli convert URL --combine` |
| HTML for styling | `python -m wiki_notion.cli convert URL --format html` |
| Quick preview | `python -m wiki_notion.cli info URL` |

## Import to Notion

1. **In Notion:** Click "Import" in sidebar
2. **Choose:** "Markdown & CSV" or "HTML"
3. **Upload:** Your generated file
4. **Done!** New page created

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Rate limit exceeded | Use `--token YOUR_GITHUB_TOKEN` |
| Module not found | Run `pip install -r requirements.txt` |
| Repository not found | Check URL, use token for private repos |
| No markdown files | Repository might not have .md files |

## Environment Variables

```bash
# Set GitHub token to avoid rate limits
export GITHUB_TOKEN=your_token_here
```

## File Output

### Without --combine:
- `output/repo.md` - Cleaned markdown
- `output/repo.html` - Styled HTML

### With --combine:
- `output/repo_combined.md` - All files merged
- `output/repo_combined.html` - All files as HTML

## Testing

```bash
# Run tests
python tests/test_converter.py

# Run demo
python examples/demo.py
```

## More Information

- Full documentation: See [README.md](README.md)
- Usage guide: See [USAGE.md](USAGE.md)
- Examples: See [examples/](examples/)
