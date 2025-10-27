"""
GitHub repository fetcher and parser
"""

import os
import re
import requests
from typing import Dict, List, Optional
from urllib.parse import urlparse


class GitHubRepoFetcher:
    """Fetch and parse GitHub repository contents"""
    
    def __init__(self, repo_url: str, github_token: Optional[str] = None):
        """
        Initialize the fetcher with a repository URL
        
        Args:
            repo_url: GitHub repository URL (e.g., https://github.com/owner/repo)
            github_token: Optional GitHub personal access token for API access
        """
        self.repo_url = repo_url
        self.github_token = github_token
        self.owner, self.repo = self._parse_repo_url(repo_url)
        self.api_base = "https://api.github.com"
        
    def _parse_repo_url(self, url: str) -> tuple:
        """Parse GitHub URL to extract owner and repo name"""
        # Handle various GitHub URL formats
        patterns = [
            r'github\.com[:/]([^/]+)/([^/.]+)',
            r'github\.com/([^/]+)/([^/]+)\.git',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1), match.group(2)
        
        raise ValueError(f"Invalid GitHub URL: {url}")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for GitHub API requests"""
        headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        return headers
    
    def fetch_readme(self) -> Optional[str]:
        """Fetch README content from the repository"""
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}/readme"
        response = requests.get(url, headers=self._get_headers())
        
        if response.status_code == 200:
            data = response.json()
            # Decode base64 content
            import base64
            content = base64.b64decode(data['content']).decode('utf-8')
            return content
        return None
    
    def fetch_file_content(self, path: str) -> Optional[str]:
        """Fetch content of a specific file from the repository"""
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}/contents/{path}"
        response = requests.get(url, headers=self._get_headers())
        
        if response.status_code == 200:
            data = response.json()
            if data.get('type') == 'file':
                import base64
                content = base64.b64decode(data['content']).decode('utf-8')
                return content
        return None
    
    def list_markdown_files(self, path: str = "") -> List[Dict]:
        """List all markdown files in the repository"""
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}/contents/{path}"
        response = requests.get(url, headers=self._get_headers())
        
        markdown_files = []
        if response.status_code == 200:
            contents = response.json()
            if isinstance(contents, list):
                for item in contents:
                    if item['type'] == 'file' and item['name'].endswith(('.md', '.markdown')):
                        markdown_files.append({
                            'name': item['name'],
                            'path': item['path'],
                            'url': item['html_url']
                        })
                    elif item['type'] == 'dir':
                        # Recursively fetch from subdirectories
                        markdown_files.extend(self.list_markdown_files(item['path']))
        
        return markdown_files
    
    def fetch_repo_info(self) -> Optional[Dict]:
        """Fetch basic repository information"""
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}"
        response = requests.get(url, headers=self._get_headers())
        
        if response.status_code == 200:
            data = response.json()
            return {
                'name': data.get('name'),
                'full_name': data.get('full_name'),
                'description': data.get('description'),
                'stars': data.get('stargazers_count'),
                'forks': data.get('forks_count'),
                'url': data.get('html_url'),
                'topics': data.get('topics', []),
            }
        return None
