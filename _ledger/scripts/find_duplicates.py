#!/usr/bin/env python3
"""
Find duplicate files across the repository using content hashing.
Helps prevent re-archiving already archived content.
"""

import os
import hashlib
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

def calculate_file_hash(filepath: Path) -> str:
    """Calculate SHA-256 hash of file content."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"Error hashing {filepath}: {e}")
        return ""

def scan_directory(root_path: str, extensions: List[str] = ['.md', '.txt']) -> Dict[str, List[str]]:
    """Scan directory and build hash -> [file_paths] mapping."""
    hash_map = defaultdict(list)
    
    for root, _, files in os.walk(root_path):
        # Skip .git directory
        if '.git' in root:
            continue
            
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                filepath = Path(root) / file
                file_hash = calculate_file_hash(filepath)
                if file_hash:
                    hash_map[file_hash].append(str(filepath))
    
    return hash_map

def find_duplicates(hash_map: Dict[str, List[str]]) -> List[Tuple[str, List[str]]]:
    """Find files with duplicate content."""
    duplicates = []
    
    for file_hash, file_paths in hash_map.items():
        if len(file_paths) > 1:
            duplicates.append((file_hash, file_paths))
    
    return duplicates

def categorize_location(filepath: str) -> str:
    """Categorize file location."""
    if '_archive/' in filepath:
        return 'archived'
    elif 'new additions/' in filepath:
        return 'new_additions'
    elif '_system/' in filepath:
        return 'system'
    else:
        return 'active'

def generate_report(duplicates: List[Tuple[str, List[str]]]) -> str:
    """Generate human-readable duplicate report."""
    report = ["# Duplicate Files Report\n"]
    report.append(f"Found {len(duplicates)} sets of duplicate files\n")
    
    for idx, (file_hash, file_paths) in enumerate(duplicates, 1):
        report.append(f"\n## Duplicate Set {idx}")
        report.append(f"**Hash**: {file_hash[:16]}...")
        report.append(f"**Files** ({len(file_paths)}):")
        
        # Group by location
        by_location = defaultdict(list)
        for path in file_paths:
            location = categorize_location(path)
            by_location[location].append(path)
        
        for location, paths in by_location.items():
            report.append(f"\n### {location.upper()}")
            for path in paths:
                report.append(f"- {path}")
        
        # Add recommendation
        if 'archived' in by_location and ('active' in by_location or 'new_additions' in by_location):
            report.append("\n**Recommendation**: Delete from active/new_additions (already archived)")
    
    return "\n".join(report)

def main():
    """Main execution."""
    print("Scanning for duplicate files...")
    
    # Scan repository
    repo_root = Path(__file__).parent.parent.parent
    hash_map = scan_directory(repo_root)
    
    print(f"Scanned {sum(len(paths) for paths in hash_map.values())} files")
    
    # Find duplicates
    duplicates = find_duplicates(hash_map)
    
    if duplicates:
        print(f"Found {len(duplicates)} sets of duplicates")
        
        # Generate report
        report = generate_report(duplicates)
        
        # Save report
        report_path = repo_root / "_ledger" / "reports" / "duplicate_report.md"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"Report saved to: {report_path}")
        
        # Also save JSON for programmatic use
        json_data = {
            "duplicates": [
                {
                    "hash": h,
                    "files": paths,
                    "locations": {loc: [p for p in paths if categorize_location(p) == loc] 
                                for loc in set(categorize_location(p) for p in paths)}
                }
                for h, paths in duplicates
            ]
        }
        
        json_path = repo_root / "_ledger" / "deduplication_map.json"
        with open(json_path, 'w') as f:
            json.dump(json_data, f, indent=2)
        
        print(f"JSON data saved to: {json_path}")
    else:
        print("No duplicates found!")

if __name__ == "__main__":
    main()