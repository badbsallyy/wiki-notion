"""
Command-line interface for wiki-notion
"""

import click
import os
import sys
from pathlib import Path
from .fetcher import GitHubRepoFetcher
from .converter import NotionConverter


@click.group()
@click.version_option(version="0.1.0")
def main():
    """
    wiki-notion: Convert GitHub repositories to Notion-friendly formats
    
    Transform GitHub repos (lists, wikis, libraries) into HTML or Markdown
    files that can be easily imported into Notion.
    """
    pass


@main.command()
@click.argument('repo_url')
@click.option('--output', '-o', default='output', help='Output directory for generated files')
@click.option('--format', '-f', type=click.Choice(['html', 'markdown', 'both']), default='both',
              help='Output format (html, markdown, or both)')
@click.option('--token', '-t', envvar='GITHUB_TOKEN', help='GitHub personal access token')
@click.option('--combine', '-c', is_flag=True, help='Combine all markdown files into one')
@click.option('--toc', is_flag=True, help='Add table of contents')
def convert(repo_url, output, format, token, combine, toc):
    """
    Convert a GitHub repository to Notion-friendly format.
    
    REPO_URL: GitHub repository URL (e.g., https://github.com/owner/repo)
    
    Examples:
    
        \b
        # Convert to both HTML and Markdown
        wiki-notion convert https://github.com/owner/repo
        
        \b
        # Convert to HTML only
        wiki-notion convert https://github.com/owner/repo --format html
        
        \b
        # Use GitHub token for private repos or higher rate limits
        wiki-notion convert https://github.com/owner/repo --token YOUR_TOKEN
        
        \b
        # Combine all files into one document
        wiki-notion convert https://github.com/owner/repo --combine
    """
    click.echo(f"🔍 Fetching repository: {repo_url}")
    
    try:
        # Initialize fetcher
        fetcher = GitHubRepoFetcher(repo_url, github_token=token)
        converter = NotionConverter()
        
        # Create output directory
        output_dir = Path(output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Fetch repository info
        repo_info = fetcher.fetch_repo_info()
        if repo_info:
            click.echo(f"📦 Repository: {repo_info['full_name']}")
            if repo_info['description']:
                click.echo(f"📝 Description: {repo_info['description']}")
        
        # Fetch README
        readme_content = fetcher.fetch_readme()
        
        if combine:
            # Fetch all markdown files and combine them
            click.echo("📄 Fetching all markdown files...")
            md_files = fetcher.list_markdown_files()
            
            if not md_files and not readme_content:
                click.echo("❌ No markdown files found in the repository", err=True)
                sys.exit(1)
            
            files_content = []
            
            # Add README first if available
            if readme_content:
                files_content.append({
                    'name': 'README',
                    'content': readme_content
                })
            
            # Fetch other markdown files
            for md_file in md_files:
                if md_file['name'].upper() != 'README.MD':
                    click.echo(f"  📄 {md_file['path']}")
                    content = fetcher.fetch_file_content(md_file['path'])
                    if content:
                        files_content.append({
                            'name': md_file['path'],
                            'content': content
                        })
            
            # Combine all files
            combined_content = converter.combine_multiple_files(files_content)
            
            # Add table of contents if requested
            if toc:
                toc_content = converter.create_table_of_contents(combined_content)
                combined_content = toc_content + combined_content
            
            # Clean for Notion
            combined_content = converter.clean_markdown_for_notion(combined_content)
            
            # Save combined output
            repo_name = repo_info['name'] if repo_info else 'combined'
            
            if format in ['markdown', 'both']:
                md_file = output_dir / f"{repo_name}_combined.md"
                md_file.write_text(combined_content, encoding='utf-8')
                click.echo(f"✅ Markdown saved: {md_file}")
            
            if format in ['html', 'both']:
                html_content = converter.markdown_to_html(
                    combined_content,
                    title=f"{repo_info['full_name']}" if repo_info else repo_name
                )
                html_file = output_dir / f"{repo_name}_combined.html"
                html_file.write_text(html_content, encoding='utf-8')
                click.echo(f"✅ HTML saved: {html_file}")
        
        else:
            # Process README only
            if not readme_content:
                click.echo("❌ No README found in the repository", err=True)
                sys.exit(1)
            
            click.echo("📄 Processing README...")
            
            # Add table of contents if requested
            if toc:
                toc_content = converter.create_table_of_contents(readme_content)
                readme_content = toc_content + readme_content
            
            # Clean for Notion
            cleaned_content = converter.clean_markdown_for_notion(readme_content)
            
            repo_name = repo_info['name'] if repo_info else 'output'
            
            if format in ['markdown', 'both']:
                md_file = output_dir / f"{repo_name}.md"
                md_file.write_text(cleaned_content, encoding='utf-8')
                click.echo(f"✅ Markdown saved: {md_file}")
            
            if format in ['html', 'both']:
                html_content = converter.markdown_to_html(
                    cleaned_content,
                    title=f"{repo_info['full_name']}" if repo_info else repo_name
                )
                html_file = output_dir / f"{repo_name}.html"
                html_file.write_text(html_content, encoding='utf-8')
                click.echo(f"✅ HTML saved: {html_file}")
        
        click.echo(f"\n✨ Done! Files saved to: {output_dir.absolute()}")
        click.echo("\n💡 Tip: You can now import these files into Notion:")
        click.echo("   1. In Notion, click 'Import' in the sidebar")
        click.echo("   2. Select 'Markdown & CSV' or 'HTML'")
        click.echo("   3. Upload the generated file(s)")
        
    except ValueError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ An error occurred: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument('repo_url')
@click.option('--token', '-t', envvar='GITHUB_TOKEN', help='GitHub personal access token')
def info(repo_url, token):
    """
    Display information about a GitHub repository.
    
    REPO_URL: GitHub repository URL
    """
    try:
        fetcher = GitHubRepoFetcher(repo_url, github_token=token)
        repo_info = fetcher.fetch_repo_info()
        
        if repo_info:
            click.echo("\n📦 Repository Information:")
            click.echo(f"   Name: {repo_info['name']}")
            click.echo(f"   Full Name: {repo_info['full_name']}")
            click.echo(f"   Description: {repo_info['description'] or 'N/A'}")
            click.echo(f"   Stars: ⭐ {repo_info['stars']}")
            click.echo(f"   Forks: 🍴 {repo_info['forks']}")
            click.echo(f"   URL: {repo_info['url']}")
            if repo_info['topics']:
                click.echo(f"   Topics: {', '.join(repo_info['topics'])}")
            
            # List markdown files
            click.echo("\n📄 Markdown Files:")
            md_files = fetcher.list_markdown_files()
            if md_files:
                for md_file in md_files:
                    click.echo(f"   - {md_file['path']}")
            else:
                click.echo("   No markdown files found")
        else:
            click.echo("❌ Could not fetch repository information", err=True)
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
