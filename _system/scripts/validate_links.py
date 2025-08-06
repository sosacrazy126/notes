#!/usr/bin/env python3
"""
Documentation Link Validator
Validates all links in markdown files and generates a comprehensive report
"""

import os
import re
import requests
import json
from pathlib import Path
from urllib.parse import urljoin, urlparse
from datetime import datetime
import time

class LinkValidator:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'total_files': 0,
            'total_links': 0,
            'broken_links': 0,
            'valid_links': 0,
            'files_with_issues': [],
            'broken_link_details': []
        }
        
    def extract_links_from_file(self, file_path):
        """Extract all markdown links from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return []
        
        # Regex patterns for different link types
        patterns = [
            r'\[([^\]]*)\]\(([^)]+)\)',  # [text](url)
            r'<(https?://[^>]+)>',       # <url>
            r'(?<![\[\(])(https?://\S+)', # bare URLs
        ]
        
        links = []
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    if len(match) == 2:  # [text](url) format
                        links.append(match[1])
                    else:  # bare URL
                        links.append(match)
                else:  # <url> format
                    links.append(match)
        
        return links
    
    def is_valid_url(self, url):
        """Check if URL is valid and accessible"""
        # Skip relative links and anchors for now
        if url.startswith('#') or not url.startswith(('http://', 'https://')):
            return True, "Relative link (skipped)"
        
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            if response.status_code < 400:
                return True, f"Status: {response.status_code}"
            else:
                return False, f"HTTP {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, str(e)
    
    def validate_file(self, file_path):
        """Validate all links in a single file"""
        print(f"Validating: {file_path}")
        links = self.extract_links_from_file(file_path)
        
        if not links:
            return
        
        file_issues = []
        for link in links:
            self.results['total_links'] += 1
            is_valid, message = self.is_valid_url(link)
            
            if is_valid:
                self.results['valid_links'] += 1
            else:
                self.results['broken_links'] += 1
                issue = {
                    'file': str(file_path),
                    'link': link,
                    'error': message
                }
                file_issues.append(issue)
                self.results['broken_link_details'].append(issue)
                print(f"  ❌ BROKEN: {link} - {message}")
            
            # Rate limiting to be nice to servers
            time.sleep(0.1)
        
        if file_issues:
            self.results['files_with_issues'].append({
                'file': str(file_path),
                'issues': file_issues
            })
    
    def validate_all(self):
        """Validate links in all markdown files"""
        print("🔍 Starting documentation link validation...")
        print(f"📁 Scanning directory: {self.root_dir}")
        
        markdown_files = list(self.root_dir.rglob("*.md"))
        self.results['total_files'] = len(markdown_files)
        
        print(f"📄 Found {len(markdown_files)} markdown files")
        
        for file_path in markdown_files:
            # Skip certain directories that might have many external links
            if any(skip in str(file_path) for skip in ['.git', 'node_modules', '__pycache__']):
                continue
                
            self.validate_file(file_path)
        
        self.generate_report()
    
    def generate_report(self):
        """Generate a comprehensive validation report"""
        print("\n" + "="*60)
        print("📊 LINK VALIDATION REPORT")
        print("="*60)
        print(f"📅 Timestamp: {self.results['timestamp']}")
        print(f"📄 Files scanned: {self.results['total_files']}")
        print(f"🔗 Total links found: {self.results['total_links']}")
        print(f"✅ Valid links: {self.results['valid_links']}")
        print(f"❌ Broken links: {self.results['broken_links']}")
        
        if self.results['broken_links'] > 0:
            print(f"\n🚨 Files with issues: {len(self.results['files_with_issues'])}")
            print("\n📋 BROKEN LINKS DETAILS:")
            print("-" * 40)
            
            for issue in self.results['broken_link_details']:
                print(f"File: {issue['file']}")
                print(f"Link: {issue['link']}")
                print(f"Error: {issue['error']}")
                print("-" * 40)
        
        # Calculate success rate
        if self.results['total_links'] > 0:
            success_rate = (self.results['valid_links'] / self.results['total_links']) * 100
            print(f"\n📈 Success Rate: {success_rate:.1f}%")
            
            if success_rate >= 95:
                print("🎉 Excellent link health!")
            elif success_rate >= 90:
                print("👍 Good link health")
            elif success_rate >= 80:
                print("⚠️  Link health needs attention")
            else:
                print("🚨 Poor link health - immediate action needed")
        
        # Save detailed report
        report_file = self.root_dir / "_system" / "monitoring" / "link_validation_report.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Detailed report saved to: {report_file}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate links in documentation")
    parser.add_argument("--dir", default=".", help="Directory to scan (default: current)")
    parser.add_argument("--quick", action="store_true", help="Quick validation (skip external links)")
    
    args = parser.parse_args()
    
    validator = LinkValidator(args.dir)
    validator.validate_all()

if __name__ == "__main__":
    main()