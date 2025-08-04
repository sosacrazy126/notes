#!/usr/bin/env python3
"""
Generate comprehensive content manifest for the development ledger system.
Creates searchable index of all content with metadata and relationships.
"""

import os
import yaml
import hashlib
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import re

def count_tokens(text):
    """Estimate token count (rough approximation)."""
    # Simple tokenization - in production would use tiktoken
    words = len(text.split())
    return int(words * 1.3)  # Rough GPT-4 token estimate

def extract_metadata(content):
    """Extract frontmatter and analyze content."""
    metadata = {
        'has_frontmatter': False,
        'tags': [],
        'title': '',
        'topics': []
    }
    
    # Check for YAML frontmatter
    if content.startswith('---\n'):
        try:
            end_idx = content.find('\n---\n', 4)
            if end_idx > 0:
                frontmatter = yaml.safe_load(content[4:end_idx])
                metadata['has_frontmatter'] = True
                metadata.update(frontmatter or {})
        except:
            pass
    
    # Extract title from first heading
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            metadata['title'] = line[2:].strip()
            break
    
    # Extract topics from content
    topics = set()
    content_lower = content.lower()
    
    # Common development topics
    dev_keywords = {
        'ai': ['ai', 'artificial intelligence', 'llm', 'gpt', 'claude'],
        'development': ['code', 'programming', 'development', 'software'],
        'testing': ['test', 'qa', 'testing', 'automation'],
        'documentation': ['docs', 'documentation', 'readme'],
        'architecture': ['architecture', 'design', 'pattern', 'framework'],
        'git': ['git', 'version control', 'commit', 'branch'],
        'devops': ['ci/cd', 'deployment', 'docker', 'kubernetes']
    }
    
    for topic, keywords in dev_keywords.items():
        if any(keyword in content_lower for keyword in keywords):
            topics.add(topic)
    
    metadata['topics'] = list(topics)
    return metadata

def categorize_file(filepath):
    """Determine file category based on path."""
    path_str = str(filepath)
    
    if '_archive/' in path_str:
        return 'archived'
    elif '_system/' in path_str or '_ledger/' in path_str:
        return 'system'
    elif 'dev_tools/' in path_str:
        return 'tools'
    elif 'documentation/' in path_str:
        return 'documentation'
    elif 'active_work/' in path_str:
        return 'active'
    elif 'code_library/' in path_str:
        return 'library'
    else:
        return 'misc'

def find_relationships(filepath, all_files):
    """Find related files based on content and naming."""
    relationships = []
    
    # Simple relationship detection
    file_stem = filepath.stem.lower()
    file_parent = str(filepath.parent)
    
    for other_file in all_files:
        if other_file == filepath:
            continue
            
        other_stem = other_file.stem.lower()
        other_parent = str(other_file.parent)
        
        # Same directory
        if file_parent == other_parent:
            relationships.append({
                'file': str(other_file),
                'type': 'sibling',
                'strength': 0.3
            })
        
        # Similar names
        if file_stem in other_stem or other_stem in file_stem:
            relationships.append({
                'file': str(other_file),
                'type': 'related',
                'strength': 0.5
            })
    
    # Sort by strength and limit
    relationships.sort(key=lambda x: x['strength'], reverse=True)
    return relationships[:5]

def generate_manifest(root_path):
    """Generate complete content manifest."""
    root = Path(root_path)
    manifest = {
        'metadata': {
            'version': '1.0',
            'generated': datetime.now().isoformat(),
            'total_files': 0,
            'total_tokens': 0,
            'total_size_bytes': 0
        },
        'categories': defaultdict(lambda: {
            'file_count': 0,
            'token_count': 0,
            'size_bytes': 0
        }),
        'topics': defaultdict(int),
        'entries': []
    }
    
    # Find all markdown files
    md_files = list(root.rglob('*.md'))
    md_files = [f for f in md_files if '.git' not in str(f)]
    
    print(f"Processing {len(md_files)} markdown files...")
    
    for filepath in md_files:
        try:
            # Read file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Calculate stats
            file_size = filepath.stat().st_size
            token_count = count_tokens(content)
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            
            # Extract metadata
            metadata = extract_metadata(content)
            category = categorize_file(filepath)
            
            # Find relationships
            relationships = find_relationships(filepath, md_files)
            
            # Create entry
            entry = {
                'file_path': str(filepath.relative_to(root)),
                'absolute_path': str(filepath),
                'content_hash': content_hash,
                'size_bytes': file_size,
                'token_count': token_count,
                'category': category,
                'topics': metadata['topics'],
                'title': metadata['title'],
                'has_frontmatter': metadata['has_frontmatter'],
                'last_modified': datetime.fromtimestamp(filepath.stat().st_mtime).isoformat(),
                'relationships': relationships
            }
            
            manifest['entries'].append(entry)
            
            # Update statistics
            manifest['categories'][category]['file_count'] += 1
            manifest['categories'][category]['token_count'] += token_count
            manifest['categories'][category]['size_bytes'] += file_size
            
            for topic in metadata['topics']:
                manifest['topics'][topic] += 1
            
            manifest['metadata']['total_files'] += 1
            manifest['metadata']['total_tokens'] += token_count
            manifest['metadata']['total_size_bytes'] += file_size
            
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            continue
    
    # Convert defaultdicts to regular dicts
    manifest['categories'] = dict(manifest['categories'])
    manifest['topics'] = dict(manifest['topics'])
    
    return manifest

def save_manifest(manifest, output_path):
    """Save manifest in multiple formats."""
    output_path = Path(output_path)
    
    # YAML format (human readable)
    yaml_path = output_path / 'manifest.yaml'
    with open(yaml_path, 'w') as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
    
    # JSON format (programmatic use)
    json_path = output_path / 'manifest.json'
    with open(json_path, 'w') as f:
        json.dump(manifest, f, indent=2, sort_keys=False)
    
    # Summary report
    summary_path = output_path / 'reports' / 'manifest_summary.md'
    summary_path.parent.mkdir(exist_ok=True)
    
    with open(summary_path, 'w') as f:
        f.write(generate_summary_report(manifest))
    
    return {
        'yaml': yaml_path,
        'json': json_path,
        'summary': summary_path
    }

def generate_summary_report(manifest):
    """Generate human-readable summary report."""
    report = ["# Content Manifest Summary\n"]
    
    # Overview
    meta = manifest['metadata']
    report.extend([
        f"**Generated**: {meta['generated']}",
        f"**Total Files**: {meta['total_files']:,}",
        f"**Total Tokens**: {meta['total_tokens']:,}",
        f"**Total Size**: {meta['total_size_bytes']:,} bytes\n",
    ])
    
    # Categories
    report.append("## By Category\n")
    for category, stats in manifest['categories'].items():
        pct = (stats['token_count'] / meta['total_tokens']) * 100
        report.append(f"- **{category.title()}**: {stats['file_count']} files, "
                     f"{stats['token_count']:,} tokens ({pct:.1f}%)")
    
    # Topics
    report.append("\n## By Topic\n")
    sorted_topics = sorted(manifest['topics'].items(), key=lambda x: x[1], reverse=True)
    for topic, count in sorted_topics[:10]:
        report.append(f"- **{topic}**: {count} files")
    
    # Top files by size
    report.append("\n## Largest Files\n")
    sorted_files = sorted(manifest['entries'], key=lambda x: x['token_count'], reverse=True)
    for entry in sorted_files[:10]:
        report.append(f"- {entry['file_path']}: {entry['token_count']:,} tokens")
    
    report.append("\n---\n*Generated by content manifest system*")
    return "\n".join(report)

def main():
    """Main execution."""
    repo_root = Path(__file__).parent.parent.parent
    print(f"Generating manifest for: {repo_root}")
    
    # Generate manifest
    manifest = generate_manifest(repo_root)
    
    # Save in multiple formats
    ledger_path = repo_root / '_ledger'
    paths = save_manifest(manifest, ledger_path)
    
    print(f"\nManifest generated:")
    print(f"- YAML: {paths['yaml']}")
    print(f"- JSON: {paths['json']}")
    print(f"- Summary: {paths['summary']}")
    
    # Print quick stats
    meta = manifest['metadata']
    print(f"\nQuick Stats:")
    print(f"- {meta['total_files']} files processed")
    print(f"- {meta['total_tokens']:,} total tokens")
    print(f"- {len(manifest['categories'])} categories")
    print(f"- {len(manifest['topics'])} topics identified")

if __name__ == "__main__":
    main()