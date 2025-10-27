"""
Tests for wiki-notion converter functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wiki_notion.converter import NotionConverter
from wiki_notion.fetcher import GitHubRepoFetcher


def test_converter_initialization():
    """Test that converter initializes correctly"""
    converter = NotionConverter()
    assert converter is not None
    print("✅ Converter initialization test passed")


def test_clean_markdown():
    """Test markdown cleaning functionality"""
    converter = NotionConverter()
    
    test_md = """# Test Header

This is a test.

<!--This is a comment-->

Some content."""
    
    cleaned = converter.clean_markdown_for_notion(test_md)
    assert "<!--" not in cleaned  # Comments should be removed
    assert "# Test Header" in cleaned
    print("✅ Markdown cleaning test passed")


def test_markdown_to_html():
    """Test markdown to HTML conversion"""
    converter = NotionConverter()
    
    test_md = "# Header\n\nThis is **bold** text."
    html = converter.markdown_to_html(test_md, "Test")
    
    assert "<h1" in html
    assert "<strong>bold</strong>" in html
    assert "<!DOCTYPE html>" in html
    print("✅ Markdown to HTML conversion test passed")


def test_extract_links():
    """Test link extraction"""
    converter = NotionConverter()
    
    test_md = "[Link 1](http://example.com) and [Link 2](http://test.com)"
    links = converter.extract_links_from_markdown(test_md)
    
    assert len(links) == 2
    assert links[0]['text'] == 'Link 1'
    assert links[0]['url'] == 'http://example.com'
    print("✅ Link extraction test passed")


def test_table_of_contents():
    """Test TOC generation"""
    converter = NotionConverter()
    
    test_md = """# Main Header

## Section 1

### Subsection 1.1

## Section 2"""
    
    toc = converter.create_table_of_contents(test_md)
    assert "Table of Contents" in toc
    assert "Section 1" in toc
    assert "Section 2" in toc
    print("✅ Table of contents test passed")


def test_combine_files():
    """Test file combination"""
    converter = NotionConverter()
    
    files = [
        {'name': 'file1.md', 'content': '# File 1\n\nContent 1'},
        {'name': 'file2.md', 'content': '# File 2\n\nContent 2'},
    ]
    
    combined = converter.combine_multiple_files(files)
    assert 'file1.md' in combined
    assert 'file2.md' in combined
    assert 'Content 1' in combined
    assert 'Content 2' in combined
    print("✅ File combination test passed")


def test_fetcher_initialization():
    """Test fetcher initialization with URL parsing"""
    # Test various URL formats
    test_urls = [
        'https://github.com/owner/repo',
        'http://github.com/owner/repo',
        'https://github.com/owner/repo.git',
    ]
    
    for url in test_urls:
        fetcher = GitHubRepoFetcher(url)
        assert fetcher.owner == 'owner'
        assert fetcher.repo == 'repo'
    
    print("✅ Fetcher URL parsing test passed")


def test_html_output_structure():
    """Test that HTML output has proper structure"""
    converter = NotionConverter()
    
    test_md = "# Test\n\nContent"
    html = converter.markdown_to_html(test_md, "Test Doc")
    
    # Check for essential HTML elements
    assert "<!DOCTYPE html>" in html
    assert "<html" in html
    assert "<head>" in html
    assert "<body>" in html
    assert "<style>" in html  # Should have CSS
    assert "</html>" in html
    print("✅ HTML structure test passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("Running wiki-notion tests")
    print("="*60 + "\n")
    
    tests = [
        test_converter_initialization,
        test_clean_markdown,
        test_markdown_to_html,
        test_extract_links,
        test_table_of_contents,
        test_combine_files,
        test_fetcher_initialization,
        test_html_output_structure,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Tests completed: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
