from setuptools import setup, find_packages

setup(
    name="wiki-notion",
    version="0.1.0",
    description="Convert GitHub repositories (lists/wikis) to Notion-friendly HTML/Markdown",
    author="",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "markdown>=3.5.0",
        "beautifulsoup4>=4.12.0",
        "html2text>=2020.1.16",
        "click>=8.1.0",
    ],
    entry_points={
        "console_scripts": [
            "wiki-notion=wiki_notion.cli:main",
        ],
    },
    python_requires=">=3.7",
)
