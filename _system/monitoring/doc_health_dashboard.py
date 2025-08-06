#!/usr/bin/env python3
"""
Documentation Health Dashboard
Comprehensive monitoring and reporting for documentation quality
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta
import subprocess
import re

class DocumentationHealthDashboard:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.metrics = {
            'timestamp': datetime.now().isoformat(),
            'overall_health': 0.0,
            'link_validity': 0.0,
            'api_coverage': 0.0,
            'example_completeness': 0.0,
            'freshness_score': 0.0,
            'file_statistics': {},
            'recommendations': []
        }
        
    def analyze_file_statistics(self):
        """Analyze basic file statistics"""
        markdown_files = list(self.root_dir.rglob("*.md"))
        
        stats = {
            'total_files': len(markdown_files),
            'total_size_bytes': 0,
            'categories': {},
            'recent_updates': 0,
            'outdated_files': 0
        }
        
        one_week_ago = datetime.now() - timedelta(days=7)
        three_months_ago = datetime.now() - timedelta(days=90)
        
        for file_path in markdown_files:
            try:
                file_stat = file_path.stat()
                stats['total_size_bytes'] += file_stat.st_size
                
                # Check file age
                mod_time = datetime.fromtimestamp(file_stat.st_mtime)
                if mod_time > one_week_ago:
                    stats['recent_updates'] += 1
                elif mod_time < three_months_ago:
                    stats['outdated_files'] += 1
                
                # Categorize by directory
                category = str(file_path.parent).split('/')[0] if '/' in str(file_path) else 'root'
                stats['categories'][category] = stats['categories'].get(category, 0) + 1
                
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")
        
        self.metrics['file_statistics'] = stats
        return stats
    
    def check_link_health(self):
        """Check link health from previous validation"""
        link_report_path = self.root_dir / "_system" / "monitoring" / "link_validation_report.json"
        
        if link_report_path.exists():
            try:
                with open(link_report_path, 'r') as f:
                    link_data = json.load(f)
                
                if link_data['total_links'] > 0:
                    validity = (link_data['valid_links'] / link_data['total_links']) * 100
                    self.metrics['link_validity'] = validity
                    
                    if validity < 90:
                        self.metrics['recommendations'].append({
                            'priority': 'high',
                            'category': 'links',
                            'message': f"Link validity is {validity:.1f}% - run link validation and fix broken links"
                        })
                
            except Exception as e:
                print(f"Error reading link validation report: {e}")
                self.metrics['link_validity'] = 0
                self.metrics['recommendations'].append({
                    'priority': 'medium',
                    'category': 'links',
                    'message': "Run link validation to check link health"
                })
        else:
            self.metrics['recommendations'].append({
                'priority': 'medium',
                'category': 'links',
                'message': "No link validation report found - run link validation"
            })
    
    def analyze_api_coverage(self):
        """Analyze API documentation coverage"""
        api_files = list(self.root_dir.rglob("*api*.md"))
        system_files = list((self.root_dir / "_system").rglob("*.py"))
        
        # Simple heuristic: ratio of API docs to system files
        if system_files:
            coverage = min(100, (len(api_files) / len(system_files)) * 100)
            self.metrics['api_coverage'] = coverage
            
            if coverage < 80:
                self.metrics['recommendations'].append({
                    'priority': 'medium',
                    'category': 'api',
                    'message': f"API coverage is {coverage:.1f}% - consider generating more API documentation"
                })
        else:
            self.metrics['api_coverage'] = 100  # No system files to document
    
    def check_example_completeness(self):
        """Check completeness of code examples"""
        pattern_files = list(self.root_dir.rglob("*pattern*.md"))
        guide_files = list(self.root_dir.rglob("*guide*.md"))
        
        files_with_examples = 0
        total_files = len(pattern_files) + len(guide_files)
        
        if total_files == 0:
            self.metrics['example_completeness'] = 100
            return
        
        for file_path in pattern_files + guide_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Look for code blocks
                if '```' in content or '    ' in content:  # Code blocks or indented code
                    files_with_examples += 1
                    
            except Exception as e:
                print(f"Error checking examples in {file_path}: {e}")
        
        completeness = (files_with_examples / total_files) * 100
        self.metrics['example_completeness'] = completeness
        
        if completeness < 80:
            self.metrics['recommendations'].append({
                'priority': 'medium',
                'category': 'examples',
                'message': f"Example completeness is {completeness:.1f}% - add code examples to guides and patterns"
            })
    
    def calculate_freshness_score(self):
        """Calculate documentation freshness score"""
        stats = self.metrics['file_statistics']
        
        if stats['total_files'] == 0:
            self.metrics['freshness_score'] = 100
            return
        
        # Score based on recent updates vs outdated files
        recent_ratio = stats['recent_updates'] / stats['total_files']
        outdated_ratio = stats['outdated_files'] / stats['total_files']
        
        # Freshness score: recent updates boost score, outdated files reduce it
        freshness = max(0, min(100, (recent_ratio * 100) - (outdated_ratio * 50) + 50))
        self.metrics['freshness_score'] = freshness
        
        if freshness < 70:
            self.metrics['recommendations'].append({
                'priority': 'low',
                'category': 'freshness',
                'message': f"Freshness score is {freshness:.1f}% - consider updating outdated documentation"
            })
    
    def calculate_overall_health(self):
        """Calculate overall documentation health score"""
        weights = {
            'link_validity': 0.3,
            'api_coverage': 0.2,
            'example_completeness': 0.25,
            'freshness_score': 0.25
        }
        
        overall = sum(self.metrics[metric] * weight for metric, weight in weights.items())
        self.metrics['overall_health'] = overall
        
        # Add overall health recommendation
        if overall >= 90:
            health_status = "Excellent"
            color = "🟢"
        elif overall >= 80:
            health_status = "Good"
            color = "🟡"
        elif overall >= 70:
            health_status = "Fair"
            color = "🟠"
        else:
            health_status = "Poor"
            color = "🔴"
        
        self.metrics['health_status'] = f"{color} {health_status}"
    
    def generate_dashboard(self):
        """Generate comprehensive health dashboard"""
        print("📊 DOCUMENTATION HEALTH DASHBOARD")
        print("=" * 50)
        print(f"📅 Generated: {self.metrics['timestamp']}")
        print()
        
        # File statistics
        stats = self.analyze_file_statistics()
        print("📁 FILE STATISTICS")
        print("-" * 30)
        print(f"Total files: {stats['total_files']}")
        print(f"Total size: {stats['total_size_bytes'] / 1024 / 1024:.1f} MB")
        print(f"Recent updates (7 days): {stats['recent_updates']}")
        print(f"Outdated files (90+ days): {stats['outdated_files']}")
        print()
        
        # Health metrics
        self.check_link_health()
        self.analyze_api_coverage()
        self.check_example_completeness()
        self.calculate_freshness_score()
        self.calculate_overall_health()
        
        print("🎯 HEALTH METRICS")
        print("-" * 30)
        print(f"Overall Health: {self.metrics['overall_health']:.1f}% {self.metrics['health_status']}")
        print(f"Link Validity: {self.metrics['link_validity']:.1f}%")
        print(f"API Coverage: {self.metrics['api_coverage']:.1f}%")
        print(f"Example Completeness: {self.metrics['example_completeness']:.1f}%")
        print(f"Freshness Score: {self.metrics['freshness_score']:.1f}%")
        print()
        
        # Recommendations
        if self.metrics['recommendations']:
            print("💡 RECOMMENDATIONS")
            print("-" * 30)
            for rec in self.metrics['recommendations']:
                priority_icon = {"high": "🚨", "medium": "⚠️", "low": "💡"}
                icon = priority_icon.get(rec['priority'], "📝")
                print(f"{icon} [{rec['priority'].upper()}] {rec['message']}")
            print()
        else:
            print("✅ No recommendations - documentation health is excellent!")
            print()
        
        # Save detailed report
        report_file = self.root_dir / "_system" / "monitoring" / "health_dashboard_report.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        
        print(f"💾 Detailed report saved to: {report_file}")
        
        # Generate summary for ledger
        self.update_ledger_metrics()
    
    def update_ledger_metrics(self):
        """Update ledger with current health metrics"""
        ledger_file = self.root_dir / "_ledger" / "token_budget.yaml"
        
        if ledger_file.exists():
            try:
                with open(ledger_file, 'r') as f:
                    ledger_data = yaml.safe_load(f) or {}
                
                # Add documentation health section
                ledger_data['documentation_health'] = {
                    'last_check': self.metrics['timestamp'],
                    'overall_health': self.metrics['overall_health'],
                    'link_validity': self.metrics['link_validity'],
                    'api_coverage': self.metrics['api_coverage'],
                    'example_completeness': self.metrics['example_completeness'],
                    'freshness_score': self.metrics['freshness_score'],
                    'recommendations_count': len(self.metrics['recommendations'])
                }
                
                with open(ledger_file, 'w') as f:
                    yaml.dump(ledger_data, f, default_flow_style=False)
                
                print(f"📊 Ledger updated with health metrics")
                
            except Exception as e:
                print(f"Warning: Could not update ledger: {e}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate documentation health dashboard")
    parser.add_argument("--dir", default=".", help="Directory to analyze (default: current)")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    
    args = parser.parse_args()
    
    dashboard = DocumentationHealthDashboard(args.dir)
    
    if args.json:
        dashboard.analyze_file_statistics()
        dashboard.check_link_health()
        dashboard.analyze_api_coverage()
        dashboard.check_example_completeness()
        dashboard.calculate_freshness_score()
        dashboard.calculate_overall_health()
        print(json.dumps(dashboard.metrics, indent=2))
    else:
        dashboard.generate_dashboard()

if __name__ == "__main__":
    main()