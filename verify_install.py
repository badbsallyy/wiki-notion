#!/usr/bin/env python3
"""
Installation verification script for wiki-notion
Run this after installation to verify everything works correctly
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version {version.major}.{version.minor} is too old. Need 3.7+")
        return False

def check_dependencies():
    """Check if all dependencies are installed"""
    dependencies = [
        'requests',
        'markdown',
        'bs4',  # beautifulsoup4
        'html2text',
        'click',
    ]
    
    missing = []
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - NOT INSTALLED")
            missing.append(dep)
    
    return len(missing) == 0, missing

def check_module_import():
    """Check if wiki_notion modules can be imported"""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from wiki_notion.converter import NotionConverter
        print("✅ wiki_notion.converter")
    except ImportError as e:
        print(f"❌ wiki_notion.converter - {e}")
        return False
    
    try:
        from wiki_notion.fetcher import GitHubRepoFetcher
        print("✅ wiki_notion.fetcher")
    except ImportError as e:
        print(f"❌ wiki_notion.fetcher - {e}")
        return False
    
    try:
        from wiki_notion.cli import main
        print("✅ wiki_notion.cli")
    except ImportError as e:
        print(f"❌ wiki_notion.cli - {e}")
        return False
    
    return True

def run_basic_test():
    """Run a basic functionality test"""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from wiki_notion.converter import NotionConverter
        
        converter = NotionConverter()
        test_md = "# Test\n\nThis is a test."
        
        # Test HTML conversion
        html = converter.markdown_to_html(test_md, "Test")
        assert "<h1" in html
        print("✅ HTML conversion works")
        
        # Test markdown cleaning
        cleaned = converter.clean_markdown_for_notion(test_md)
        assert "Test" in cleaned
        print("✅ Markdown cleaning works")
        
        # Test link extraction
        links_md = "[Link](http://example.com)"
        links = converter.extract_links_from_markdown(links_md)
        assert len(links) == 1
        print("✅ Link extraction works")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("   wiki-notion Installation Verification")
    print("=" * 60)
    print()
    
    all_passed = True
    
    print("1. Checking Python version...")
    if not check_python_version():
        all_passed = False
    print()
    
    print("2. Checking dependencies...")
    deps_ok, missing = check_dependencies()
    if not deps_ok:
        all_passed = False
        print(f"\n   Missing dependencies: {', '.join(missing)}")
        print("   Install with: pip install -r requirements.txt")
    print()
    
    print("3. Checking module imports...")
    if not check_module_import():
        all_passed = False
    print()
    
    print("4. Running basic functionality test...")
    if not run_basic_test():
        all_passed = False
    print()
    
    print("=" * 60)
    if all_passed:
        print("   ✅ All checks passed!")
        print("=" * 60)
        print()
        print("🎉 wiki-notion is ready to use!")
        print()
        print("Try these commands:")
        print("  python -m wiki_notion.cli --help")
        print("  python examples/demo.py")
        print("  python examples/workflow.py")
        print()
    else:
        print("   ❌ Some checks failed")
        print("=" * 60)
        print()
        print("Please fix the issues above and run this script again.")
        print()
        sys.exit(1)

if __name__ == "__main__":
    main()
