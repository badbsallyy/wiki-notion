# wiki-notion

Convert GitHub repositories (lists, wikis, libraries, databases) into Notion-friendly HTML and Markdown files.

## 🎯 Purpose

This tool helps you transform GitHub repositories that are structured like:
- 📚 Awesome lists (e.g., awesome-python, awesome-react)
- 📖 Wiki repositories
- 🗂️ Knowledge bases and documentation
- 📊 Curated resource collections

...into clean HTML or Markdown files that can be easily imported into Notion for personal knowledge management.

## ✨ Features

- 🔄 Convert GitHub repos to HTML or Markdown
- 📦 Fetch README and all markdown files from a repository
- 🔗 Preserve links, images, and formatting
- 📑 Optionally combine multiple files into one document
- 📋 Generate table of contents automatically
- 🎨 Clean, Notion-friendly output
- 🔐 Support for private repositories with GitHub token

## 🚀 Installation

### Option 1: Install from source

```bash
git clone https://github.com/badbsallyy/wiki-notion.git
cd wiki-notion
pip install -e .
```

### Option 2: Install dependencies directly

```bash
pip install -r requirements.txt
```

## 📖 Usage

### Basic Usage

Convert a GitHub repository to both HTML and Markdown:

```bash
wiki-notion convert https://github.com/owner/repo
```

This will create an `output` directory with the converted files.

### Convert to Specific Format

```bash
# HTML only
wiki-notion convert https://github.com/owner/repo --format html

# Markdown only
wiki-notion convert https://github.com/owner/repo --format markdown
```

### Combine Multiple Files

If the repository has multiple markdown files, combine them into one document:

```bash
wiki-notion convert https://github.com/owner/repo --combine
```

### Add Table of Contents

Generate a table of contents from the headers:

```bash
wiki-notion convert https://github.com/owner/repo --toc
```

### Custom Output Directory

```bash
wiki-notion convert https://github.com/owner/repo --output my_exports
```

### Use with Private Repositories

For private repositories or to avoid rate limits, use a GitHub personal access token:

```bash
# Set as environment variable
export GITHUB_TOKEN=your_token_here
wiki-notion convert https://github.com/owner/private-repo

# Or pass directly
wiki-notion convert https://github.com/owner/private-repo --token your_token_here
```

### View Repository Information

Before converting, you can view repository details:

```bash
wiki-notion info https://github.com/owner/repo
```

## 📚 Examples

### Example 1: Convert an Awesome List

```bash
wiki-notion convert https://github.com/vinta/awesome-python --combine --toc
```

This will fetch all markdown files from the awesome-python repository, combine them, add a table of contents, and save as both HTML and Markdown.

### Example 2: Convert a Wiki Repository

```bash
wiki-notion convert https://github.com/github/docs --format markdown --combine
```

### Example 3: Quick README Export

```bash
wiki-notion convert https://github.com/torvalds/linux --format html
```

## 📥 Importing to Notion

After converting your repository:

1. Open Notion
2. Click **"Import"** in the sidebar
3. Select **"Markdown & CSV"** (for .md files) or **"HTML"** (for .html files)
4. Upload your generated file(s)
5. Notion will create a new page with your content! 🎉

## 🛠️ Command Reference

### `convert` command

```
wiki-notion convert [OPTIONS] REPO_URL

Options:
  -o, --output TEXT       Output directory (default: output)
  -f, --format [html|markdown|both]  
                         Output format (default: both)
  -t, --token TEXT       GitHub personal access token
  -c, --combine          Combine all markdown files into one
  --toc                  Add table of contents
  --help                 Show this message and exit
```

### `info` command

```
wiki-notion info [OPTIONS] REPO_URL

Options:
  -t, --token TEXT       GitHub personal access token
  --help                 Show this message and exit
```

## 🔧 Requirements

- Python 3.7+
- requests
- requests
- markdown
- beautifulsoup4
- html2text
- click

## 📝 License

MIT License - feel free to use this tool for your personal knowledge management!

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 💡 Tips

- For large repositories, use `--combine` to get all content in one file
- Use `--toc` to make navigation easier in Notion
- Set `GITHUB_TOKEN` environment variable to avoid rate limiting
- The HTML output includes nice styling that works well with Notion

## 🐛 Troubleshooting

**Issue: Rate limit exceeded**
- Solution: Use a GitHub personal access token with `--token` option

**Issue: Repository not found**
- Solution: Make sure the URL is correct and the repository is public (or use a token for private repos)

**Issue: No markdown files found**
- Solution: The repository might not have any markdown files. Try a different repository or check the repo structure with `wiki-notion info`

## ⭐ Star this repo if you find it useful!