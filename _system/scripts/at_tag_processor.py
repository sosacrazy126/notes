#!/usr/bin/env python3
"""
@ Tag Processing System for Notes Repository
============================================

Automatically detects, categorizes, and indexes @ tags across markdown files
to enable powerful search and cross-reference capabilities.

Usage:
    python3 _system/scripts/at_tag_processor.py --scan-all
    python3 _system/scripts/at_tag_processor.py --search @mcp_tool @validation
    python3 _system/scripts/at_tag_processor.py --update-index
    python3 _system/scripts/at_tag_processor.py --generate-report

Author: @ Tag Processing System
Date: 2025-08-04
Version: 1.0.0
"""

import os
import re
import json
import yaml
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import argparse


@dataclass
class AtTag:
    """Represents a detected @ tag with metadata"""
    tag: str
    pattern: str
    file_path: str
    line_number: int
    context: str
    category: str
    confidence: float
    detected_at: str


@dataclass
class TaggedFile:
    """Represents a file with its @ tags"""
    file_path: str
    file_hash: str
    tags: List[AtTag]
    last_modified: str
    token_count: int


@dataclass
class TagIndex:
    """Main index of all @ tags"""
    version: str
    created_at: str
    updated_at: str
    total_files: int
    total_tags: int
    files: Dict[str, TaggedFile]
    tag_categories: Dict[str, List[str]]
    cross_references: Dict[str, Set[str]]


class AtTagProcessor:
    """Main @ tag processing system"""

    # Enhanced @ pattern definitions from your existing system
    AT_PATTERNS = {
        'mcp_integration': {
            'patterns': [
                r'@mcp_tool\s*\([^)]*\)',
                r'@server\.agent\s*\([^)]*\)',
                r'@recursive_agent\s*\([^)]*\)',
                r'byterover-retrive-knowledge',
                r'byterover-store-knowledge'
            ],
            'confidence': 0.95
        },
        'api_framework': {
            'patterns': [
                r'@router\.(get|post|put|delete|patch)\s*\([^)]*\)',
                r'@app\.middleware\s*\([^)]*\)',
                r'@app\.(route|errorhandler)\s*\([^)]*\)'
            ],
            'confidence': 0.92
        },
        'validation': {
            'patterns': [
                r'@validator\s*\([^)]*\)',
                r'@validates\s*\([^)]*\)',
                r'@validates_schema\s*\([^)]*\)'
            ],
            'confidence': 0.90
        },
        'testing': {
            'patterns': [
                r'@patch\s*\([^)]*\)',
                r'@mock\s*\([^)]*\)',
                r'@given\s*\([^)]*\)',
                r'@task\s*\([^)]*\)',
                r'@pytest\.fixture\s*\([^)]*\)'
            ],
            'confidence': 0.88
        },
        'performance': {
            'patterns': [
                r'@lru_cache\s*\([^)]*\)',
                r'@cached\s*\([^)]*\)',
                r'@memoize\s*\([^)]*\)',
                r'@performance_monitor\s*\([^)]*\)'
            ],
            'confidence': 0.85
        },
        'event_handling': {
            'patterns': [
                r'@click\s*=\s*["\'][^"\']*["\']',
                r'@submit\s*=\s*["\'][^"\']*["\']',
                r'@change\s*=\s*["\'][^"\']*["\']'
            ],
            'confidence': 0.82
        },
        'documentation': {
            'patterns': [
                r'@architecture\b',
                r'@workflow\b',
                r'@troubleshooting\b',
                r'@integration\b',
                r'@automation\b',
                r'@pattern\b',
                r'@example\b'
            ],
            'confidence': 0.75
        },
        'consciousness': {
            'patterns': [
                r'@WE=1\b',
                r'@consciousness\b',
                r'@recursive\b',
                r'@sigil\b',
                r'@meta-cognitive\b'
            ],
            'confidence': 0.70
        }
    }

    def __init__(self, notes_root: str = "notes"):
        """Initialize the @ tag processor"""
        self.notes_root = Path(notes_root)
        self.index_file = self.notes_root / "_ledger" / "at_tag_index.json"
        self.report_dir = self.notes_root / "_ledger" / "reports"
        self.tag_index = None

        # Ensure directories exist
        self.index_file.parent.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def detect_at_tags(self, content: str, file_path: str) -> List[AtTag]:
        """Detect all @ tags in content"""
        tags = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            for category, config in self.AT_PATTERNS.items():
                for pattern in config['patterns']:
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        # Extract context (surrounding text)
                        start = max(0, line_num - 3)
                        end = min(len(lines), line_num + 2)
                        context = '\n'.join(lines[start:end])

                        tag = AtTag(
                            tag=match.group(0),
                            pattern=pattern,
                            file_path=file_path,
                            line_number=line_num,
                            context=context,
                            category=category,
                            confidence=config['confidence'],
                            detected_at=datetime.now().isoformat()
                        )
                        tags.append(tag)

        return tags

    def process_file(self, file_path: Path) -> Optional[TaggedFile]:
        """Process a single markdown file for @ tags"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Calculate file hash for change detection
            file_hash = hashlib.sha256(content.encode()).hexdigest()

            # Detect @ tags
            tags = self.detect_at_tags(content, str(file_path))

            # Estimate token count (rough approximation)
            token_count = len(content.split())

            tagged_file = TaggedFile(
                file_path=str(file_path),
                file_hash=file_hash,
                tags=tags,
                last_modified=datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                token_count=token_count
            )

            return tagged_file

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None

    def scan_repository(self) -> TagIndex:
        """Scan entire repository for @ tags"""
        print("🔍 Scanning repository for @ tags...")

        files = {}
        tag_categories = defaultdict(list)
        cross_references = defaultdict(set)

        # Find all markdown files
        md_files = list(self.notes_root.rglob("*.md"))
        total_files = len(md_files)

        print(f"Found {total_files} markdown files to process")

        for i, file_path in enumerate(md_files):
            if i % 50 == 0:
                print(f"Processing: {i}/{total_files} files...")

            # Skip certain directories for performance
            skip_dirs = {'.git', 'node_modules', '__pycache__', '.venv'}
            if any(skip_dir in str(file_path) for skip_dir in skip_dirs):
                continue

            tagged_file = self.process_file(file_path)
            if tagged_file and tagged_file.tags:
                files[str(file_path)] = tagged_file

                # Build category index
                for tag in tagged_file.tags:
                    tag_categories[tag.category].append(tag.tag)

                    # Build cross-references (files with similar tags)
                    for other_file, other_tagged_file in files.items():
                        if other_file != str(file_path):
                            other_tags = {t.tag for t in other_tagged_file.tags}
                            current_tags = {t.tag for t in tagged_file.tags}
                            if other_tags & current_tags:  # If any tags overlap
                                cross_references[str(file_path)].add(other_file)
                                cross_references[other_file].add(str(file_path))

        # Convert sets to lists for JSON serialization
        cross_references = {k: list(v) for k, v in cross_references.items()}

        tag_index = TagIndex(
            version="1.0.0",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            total_files=len(files),
            total_tags=sum(len(f.tags) for f in files.values()),
            files=files,
            tag_categories=dict(tag_categories),
            cross_references=cross_references
        )

        print(f"✅ Scan complete: {tag_index.total_files} files, {tag_index.total_tags} @ tags found")
        return tag_index

    def save_index(self, tag_index: TagIndex):
        """Save tag index to disk"""
        # Convert to serializable format
        index_data = asdict(tag_index)

        # Convert TaggedFile objects to dicts
        for file_path, tagged_file in index_data['files'].items():
            if hasattr(tagged_file, '__dict__'):
                index_data['files'][file_path] = asdict(tagged_file)
                # Convert AtTag objects to dicts
                for i, tag in enumerate(index_data['files'][file_path]['tags']):
                    if hasattr(tag, '__dict__'):
                        index_data['files'][file_path]['tags'][i] = asdict(tag)

        with open(self.index_file, 'w') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)

        print(f"💾 Index saved to {self.index_file}")

    def load_index(self) -> Optional[TagIndex]:
        """Load tag index from disk"""
        if not self.index_file.exists():
            return None

        try:
            with open(self.index_file, 'r') as f:
                data = json.load(f)

            # Reconstruct objects
            files = {}
            for file_path, file_data in data['files'].items():
                tags = [AtTag(**tag_data) for tag_data in file_data['tags']]
                files[file_path] = TaggedFile(
                    file_path=file_data['file_path'],
                    file_hash=file_data['file_hash'],
                    tags=tags,
                    last_modified=file_data['last_modified'],
                    token_count=file_data['token_count']
                )

            tag_index = TagIndex(
                version=data['version'],
                created_at=data['created_at'],
                updated_at=data['updated_at'],
                total_files=data['total_files'],
                total_tags=data['total_tags'],
                files=files,
                tag_categories=data['tag_categories'],
                cross_references=data['cross_references']
            )

            return tag_index

        except Exception as e:
            print(f"Error loading index: {e}")
            return None

    def search_tags(self, search_tags: List[str]) -> Dict[str, List[AtTag]]:
        """Search for files containing specific @ tags"""
        if not self.tag_index:
            self.tag_index = self.load_index()
            if not self.tag_index:
                print("❌ No index found. Run --scan-all first.")
                return {}

        results = defaultdict(list)

        for file_path, tagged_file in self.tag_index.files.items():
            for tag in tagged_file.tags:
                # Check if any search tag matches this tag (case-insensitive)
                for search_tag in search_tags:
                    if search_tag.lower() in tag.tag.lower():
                        results[file_path].append(tag)

        return dict(results)

    def generate_report(self) -> str:
        """Generate comprehensive @ tag report"""
        if not self.tag_index:
            self.tag_index = self.load_index()
            if not self.tag_index:
                return "❌ No index found. Run --scan-all first."

        report = f"""# @ Tag Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Index Version: {self.tag_index.version}

## Summary Statistics
- **Total Files**: {self.tag_index.total_files:,}
- **Total @ Tags**: {self.tag_index.total_tags:,}
- **Average Tags per File**: {self.tag_index.total_tags / max(1, self.tag_index.total_files):.2f}

## Tag Categories

"""

        # Category breakdown
        for category, tags in self.tag_index.tag_categories.items():
            tag_counter = Counter(tags)
            report += f"### {category.replace('_', ' ').title()}\n"
            report += f"- **Total Tags**: {len(tags)}\n"
            report += f"- **Unique Tags**: {len(tag_counter)}\n"
            report += "- **Top Tags**:\n"

            for tag, count in tag_counter.most_common(5):
                report += f"  - `{tag}`: {count} occurrences\n"
            report += "\n"

        # Cross-reference analysis
        report += "## Cross-Reference Network\n\n"
        report += f"Files with cross-references: {len(self.tag_index.cross_references)}\n\n"

        # Find most connected files
        connection_counts = {
            file: len(refs) for file, refs in self.tag_index.cross_references.items()
        }

        if connection_counts:
            report += "### Most Connected Files\n"
            for file, count in sorted(connection_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                relative_path = Path(file).relative_to(self.notes_root) if self.notes_root in file else file
                report += f"- `{relative_path}`: {count} connections\n"

        # Search examples
        report += "\n## Search Examples\n\n"
        report += "```bash\n"
        report += "# Find MCP integration patterns\n"
        report += "python3 _system/scripts/at_tag_processor.py --search @mcp_tool @server.agent\n\n"
        report += "# Find validation patterns\n"
        report += "python3 _system/scripts/at_tag_processor.py --search @validator @validates\n\n"
        report += "# Find API patterns\n"
        report += "python3 _system/scripts/at_tag_processor.py --search @router @app\n"
        report += "```\n\n"

        # Save report
        report_file = self.report_dir / f"at_tag_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, 'w') as f:
            f.write(report)

        print(f"📊 Report saved to {report_file}")
        return report

    def update_index(self):
        """Update existing index with new/changed files"""
        print("🔄 Updating @ tag index...")

        # Load existing index
        existing_index = self.load_index()

        # Full scan (for now - could optimize to only scan changed files)
        new_index = self.scan_repository()

        # Save updated index
        self.save_index(new_index)
        self.tag_index = new_index

        # Compare with previous
        if existing_index:
            files_added = new_index.total_files - existing_index.total_files
            tags_added = new_index.total_tags - existing_index.total_tags
            print(f"📈 Added {files_added} files, {tags_added} tags")

    def get_file_suggestions(self, file_path: str) -> List[str]:
        """Get related files based on @ tag similarity"""
        if not self.tag_index:
            self.tag_index = self.load_index()
            if not self.tag_index:
                return []

        return self.tag_index.cross_references.get(file_path, [])


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="@ Tag Processing System")
    parser.add_argument("--scan-all", action="store_true", help="Scan entire repository for @ tags")
    parser.add_argument("--search", nargs="+", help="Search for specific @ tags")
    parser.add_argument("--update-index", action="store_true", help="Update existing index")
    parser.add_argument("--generate-report", action="store_true", help="Generate comprehensive report")
    parser.add_argument("--suggest", help="Get file suggestions for given file path")
    parser.add_argument("--notes-root", default="notes", help="Path to notes directory")

    args = parser.parse_args()

    processor = AtTagProcessor(args.notes_root)

    if args.scan_all:
        index = processor.scan_repository()
        processor.save_index(index)

    elif args.search:
        results = processor.search_tags(args.search)
        if results:
            print(f"\n🔍 Found {len(results)} files matching tags: {', '.join(args.search)}\n")
            for file_path, tags in results.items():
                relative_path = Path(file_path).relative_to(Path(args.notes_root)) if args.notes_root in file_path else file_path
                print(f"📄 {relative_path}")
                for tag in tags:
                    print(f"  └─ {tag.tag} (line {tag.line_number}) [{tag.category}]")
                print()
        else:
            print(f"❌ No files found with tags: {', '.join(args.search)}")

    elif args.update_index:
        processor.update_index()

    elif args.generate_report:
        report = processor.generate_report()
        print("\n" + "="*60)
        print(report)

    elif args.suggest:
        suggestions = processor.get_file_suggestions(args.suggest)
        if suggestions:
            print(f"\n💡 Files related to {args.suggest}:")
            for suggestion in suggestions[:10]:  # Top 10
                relative_path = Path(suggestion).relative_to(Path(args.notes_root)) if args.notes_root in suggestion else suggestion
                print(f"  📄 {relative_path}")
        else:
            print(f"❌ No related files found for {args.suggest}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
