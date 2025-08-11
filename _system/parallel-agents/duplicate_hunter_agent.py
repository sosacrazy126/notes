#!/usr/bin/env python3
"""
Duplicate Hunter Agent
=====================

Specialized agent for aggressive duplicate detection across repository subdirectories.
Uses multiple strategies: content hashing, semantic similarity, and filename patterns.

Author: Claude Code Agent System  
Date: 2025-08-10
Version: 1.0.0
"""

import os
import json
import hashlib
import difflib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict, Counter
import logging
import re
import threading


class DuplicateHunterAgent:
    """Agent for finding and categorizing duplicate files"""
    
    def __init__(self):
        self.repo_root = Path(os.environ.get("REPO_ROOT", "."))
        self.state_dir = Path(os.environ.get("STATE_DIR", "."))
        self.agent_name = os.environ.get("AGENT_NAME", "duplicate-hunter")
        
        # Target directories from orchestrator
        self.target_dirs = ["_archive", "documentation", "new_additions", "dev_tools"]
        
        # Setup logging
        self.setup_logging()
        
        # Duplicate detection configuration
        self.extensions = ['.md', '.txt', '.py', '.json', '.yaml', '.yml', '.sh']
        self.min_file_size = 100  # bytes
        self.similarity_threshold = 0.85
        self.content_chunk_size = 4096
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Results storage
        self.duplicate_sets = []
        self.file_hashes = {}
        self.semantic_groups = defaultdict(list)
        self.processed_count = 0
        
    def setup_logging(self):
        """Configure agent logging"""
        log_file = self.state_dir.parent / "logs" / f"{self.agent_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(self.agent_name)
    
    def update_state(self, **kwargs):
        """Update agent state for orchestrator"""
        state_file = self.state_dir / f"{self.agent_name}_state.json"
        
        with self.lock:
            # Load existing state or create new
            if state_file.exists():
                with open(state_file, 'r') as f:
                    state = json.load(f)
            else:
                state = {
                    "name": self.agent_name,
                    "start_time": datetime.now().isoformat(),
                    "files_processed": 0,
                    "current_task": "",
                    "progress_percent": 0.0,
                    "duplicates_found": 0
                }
            
            # Update with provided values
            state.update(kwargs)
            state["last_update"] = datetime.now().isoformat()
            
            # Save updated state
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)
    
    def calculate_content_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file content"""
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(self.content_chunk_size), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except Exception as e:
            self.logger.warning(f"Could not hash {file_path}: {e}")
            return ""
    
    def calculate_structure_hash(self, file_path: Path) -> str:
        """Calculate hash based on file structure (lines, words, etc.)"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Normalize whitespace and extract structure
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            words = content.lower().split()
            
            structure_data = {
                "line_count": len(lines),
                "word_count": len(words),
                "char_count": len(content.strip()),
                "first_line": lines[0] if lines else "",
                "last_line": lines[-1] if lines else "",
                "word_freq": dict(Counter(words).most_common(10))
            }
            
            structure_str = json.dumps(structure_data, sort_keys=True)
            return hashlib.md5(structure_str.encode()).hexdigest()
            
        except Exception as e:
            self.logger.warning(f"Could not calculate structure hash for {file_path}: {e}")
            return ""
    
    def calculate_semantic_similarity(self, file1: Path, file2: Path) -> float:
        """Calculate semantic similarity between two files"""
        try:
            with open(file1, 'r', encoding='utf-8', errors='ignore') as f:
                content1 = f.read()
            with open(file2, 'r', encoding='utf-8', errors='ignore') as f:
                content2 = f.read()
            
            # Use difflib for sequence matching
            similarity = difflib.SequenceMatcher(None, content1, content2).ratio()
            return similarity
            
        except Exception as e:
            self.logger.warning(f"Could not calculate similarity between {file1} and {file2}: {e}")
            return 0.0
    
    def categorize_file_location(self, file_path: Path) -> str:
        """Categorize file based on its location"""
        path_str = str(file_path)
        
        if "_archive/" in path_str:
            return "archived"
        elif "new_additions/" in path_str:
            return "new_additions"
        elif "documentation/" in path_str:
            return "documentation"
        elif "_system/" in path_str:
            return "system"
        elif "workspace/" in path_str:
            return "workspace"
        elif "dev_tools/" in path_str:
            return "dev_tools"
        else:
            return "active"
    
    def should_process_file(self, file_path: Path) -> bool:
        """Determine if file should be processed for duplicate detection"""
        # Check extension
        if file_path.suffix not in self.extensions:
            return False
        
        # Check file size
        try:
            if file_path.stat().st_size < self.min_file_size:
                return False
        except:
            return False
        
        # Skip certain patterns
        skip_patterns = [
            ".git/",
            "__pycache__/",
            "node_modules/",
            ".venv/",
            "venv/",
            ".log",
            ".cache"
        ]
        
        path_str = str(file_path)
        if any(pattern in path_str for pattern in skip_patterns):
            return False
        
        return True
    
    def scan_directory_for_files(self, directory: Path) -> List[Path]:
        """Scan directory and return list of files to process"""
        files_to_process = []
        
        if not directory.exists():
            self.logger.warning(f"Directory not found: {directory}")
            return files_to_process
        
        try:
            for file_path in directory.rglob("*"):
                if file_path.is_file() and self.should_process_file(file_path):
                    files_to_process.append(file_path)
        except Exception as e:
            self.logger.error(f"Error scanning {directory}: {e}")
        
        return files_to_process
    
    def find_exact_duplicates(self, files: List[Path]) -> Dict[str, List[Path]]:
        """Find files with identical content using hashing"""
        self.logger.info("🔍 Finding exact duplicates...")
        self.update_state(current_task="Finding exact duplicates", progress_percent=20)
        
        hash_map = defaultdict(list)
        processed = 0
        
        for file_path in files:
            content_hash = self.calculate_content_hash(file_path)
            if content_hash:
                hash_map[content_hash].append(file_path)
                self.file_hashes[str(file_path)] = content_hash
                
            processed += 1
            if processed % 100 == 0:
                progress = min(20 + (processed / len(files)) * 30, 50)
                self.update_state(
                    files_processed=processed,
                    progress_percent=progress
                )
        
        # Filter to only duplicates
        exact_duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}
        
        self.logger.info(f"✅ Found {len(exact_duplicates)} sets of exact duplicates")
        return exact_duplicates
    
    def find_similar_duplicates(self, files: List[Path]) -> List[Tuple[List[Path], float]]:
        """Find files with similar content using structure and semantic analysis"""
        self.logger.info("🔍 Finding similar duplicates...")
        self.update_state(current_task="Finding similar duplicates", progress_percent=50)
        
        similar_groups = []
        structure_map = defaultdict(list)
        
        # Group by structure hash first
        for file_path in files:
            structure_hash = self.calculate_structure_hash(file_path)
            if structure_hash:
                structure_map[structure_hash].append(file_path)
        
        processed_pairs = 0
        total_pairs = sum(len(group) * (len(group) - 1) // 2 for group in structure_map.values() if len(group) > 1)
        
        # Check semantic similarity within structure groups
        for group in structure_map.values():
            if len(group) < 2:
                continue
            
            # Check all pairs in group
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    similarity = self.calculate_semantic_similarity(group[i], group[j])
                    processed_pairs += 1
                    
                    if similarity >= self.similarity_threshold:
                        # Find if either file is already in a group
                        found_group = None
                        for existing_group, _ in similar_groups:
                            if group[i] in existing_group or group[j] in existing_group:
                                found_group = existing_group
                                break
                        
                        if found_group:
                            found_group.extend([f for f in [group[i], group[j]] if f not in found_group])
                        else:
                            similar_groups.append(([group[i], group[j]], similarity))
                    
                    # Update progress
                    if processed_pairs % 50 == 0:
                        progress = 50 + (processed_pairs / max(total_pairs, 1)) * 30
                        self.update_state(progress_percent=min(progress, 80))
        
        self.logger.info(f"✅ Found {len(similar_groups)} groups of similar files")
        return similar_groups
    
    def analyze_duplicates(self, exact_duplicates: Dict[str, List[Path]], similar_groups: List[Tuple[List[Path], float]]):
        """Analyze duplicates and provide recommendations"""
        self.logger.info("📊 Analyzing duplicates for recommendations...")
        self.update_state(current_task="Analyzing duplicates", progress_percent=80)
        
        analysis_results = {
            "exact_duplicate_sets": [],
            "similar_duplicate_sets": [],
            "recommendations": {
                "files_to_delete": [],
                "files_to_archive": [],
                "files_to_merge": []
            },
            "space_savings": 0
        }
        
        # Analyze exact duplicates
        for file_hash, file_list in exact_duplicates.items():
            locations = defaultdict(list)
            for file_path in file_list:
                location = self.categorize_file_location(file_path)
                locations[location].append(file_path)
            
            # Determine which files to keep/delete
            files_to_keep = []
            files_to_delete = []
            
            # Priority order: active > system > documentation > new_additions > archived
            location_priority = ["active", "system", "documentation", "new_additions", "archived"]
            
            kept_one = False
            for location in location_priority:
                if location in locations:
                    if not kept_one:
                        # Keep the first file from the highest priority location
                        files_to_keep.append(locations[location][0])
                        kept_one = True
                        # Mark the rest from this location for deletion
                        files_to_delete.extend(locations[location][1:])
                    else:
                        # Mark all files from lower priority locations for deletion
                        files_to_delete.extend(locations[location])
            
            # Calculate space savings
            if files_to_delete:
                space_saved = sum(f.stat().st_size for f in files_to_delete if f.exists())
                analysis_results["space_savings"] += space_saved
            
            duplicate_set = {
                "hash": file_hash,
                "files": [str(f) for f in file_list],
                "locations": {loc: [str(f) for f in files] for loc, files in locations.items()},
                "keep": [str(f) for f in files_to_keep],
                "delete": [str(f) for f in files_to_delete],
                "space_saved_bytes": space_saved if files_to_delete else 0
            }
            
            analysis_results["exact_duplicate_sets"].append(duplicate_set)
            analysis_results["recommendations"]["files_to_delete"].extend([str(f) for f in files_to_delete])
        
        # Analyze similar duplicates (require manual review)
        for similar_group, similarity in similar_groups:
            locations = defaultdict(list)
            for file_path in similar_group:
                location = self.categorize_file_location(file_path)
                locations[location].append(file_path)
            
            duplicate_set = {
                "files": [str(f) for f in similar_group],
                "similarity": similarity,
                "locations": {loc: [str(f) for f in files] for loc, files in locations.items()},
                "recommendation": "manual_review"
            }
            
            analysis_results["similar_duplicate_sets"].append(duplicate_set)
            analysis_results["recommendations"]["files_to_merge"].extend([str(f) for f in similar_group])
        
        self.duplicate_sets = analysis_results
        return analysis_results
    
    def generate_report(self, analysis_results: Dict[str, Any]):
        """Generate comprehensive duplicate detection report"""
        self.logger.info("📝 Generating duplicate detection report...")
        
        report_lines = [
            "# Duplicate Files Detection Report",
            f"**Generated**: {datetime.now().isoformat()}",
            f"**Agent**: {self.agent_name}",
            "",
            "## Summary",
            f"- **Exact Duplicate Sets**: {len(analysis_results['exact_duplicate_sets'])}",
            f"- **Similar File Groups**: {len(analysis_results['similar_duplicate_sets'])}",
            f"- **Files Recommended for Deletion**: {len(analysis_results['recommendations']['files_to_delete'])}",
            f"- **Potential Space Savings**: {analysis_results['space_savings'] / 1024 / 1024:.1f} MB",
            ""
        ]
        
        # Exact duplicates section
        if analysis_results['exact_duplicate_sets']:
            report_lines.extend([
                "## Exact Duplicates (Safe to Delete)",
                ""
            ])
            
            for i, dup_set in enumerate(analysis_results['exact_duplicate_sets'], 1):
                report_lines.extend([
                    f"### Duplicate Set {i}",
                    f"**Hash**: `{dup_set['hash'][:16]}...`",
                    f"**Space Savings**: {dup_set['space_saved_bytes'] / 1024:.1f} KB",
                    "",
                    "**Files to Keep**:",
                ])
                
                for file_path in dup_set['keep']:
                    report_lines.append(f"- ✅ {file_path}")
                
                report_lines.extend([
                    "",
                    "**Files to Delete**:",
                ])
                
                for file_path in dup_set['delete']:
                    report_lines.append(f"- ❌ {file_path}")
                
                report_lines.append("")
        
        # Similar duplicates section
        if analysis_results['similar_duplicate_sets']:
            report_lines.extend([
                "## Similar Files (Manual Review Required)",
                ""
            ])
            
            for i, dup_set in enumerate(analysis_results['similar_duplicate_sets'], 1):
                report_lines.extend([
                    f"### Similar Set {i}",
                    f"**Similarity**: {dup_set['similarity']:.2%}",
                    "",
                    "**Files**:",
                ])
                
                for file_path in dup_set['files']:
                    location = self.categorize_file_location(Path(file_path))
                    report_lines.append(f"- 📄 {file_path} ({location})")
                
                report_lines.append("")
        
        # Action items
        report_lines.extend([
            "## Recommended Actions",
            "",
            "### Immediate Actions (Safe)",
            "Execute the following commands to delete exact duplicates:",
            "```bash",
        ])
        
        for file_path in analysis_results['recommendations']['files_to_delete']:
            report_lines.append(f'rm "{file_path}"')
        
        report_lines.extend([
            "```",
            "",
            "### Manual Review Required",
            "The following similar files need manual inspection:",
        ])
        
        for file_path in analysis_results['recommendations']['files_to_merge']:
            report_lines.append(f"- {file_path}")
        
        # Save report
        report_content = "\n".join(report_lines)
        report_path = self.state_dir.parent / "reports" / f"duplicate_detection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write(report_content)
        
        self.logger.info(f"✅ Report saved: {report_path}")
        return report_path
    
    def execute(self) -> Dict[str, Any]:
        """Main agent execution"""
        self.logger.info(f"🚀 Starting {self.agent_name} execution")
        self.update_state(current_task="Initializing duplicate detection", progress_percent=0)
        
        results = {
            "agent_name": self.agent_name,
            "start_time": datetime.now().isoformat(),
            "success": False,
            "files_scanned": 0,
            "exact_duplicates": 0,
            "similar_groups": 0,
            "space_savings_mb": 0,
            "report_path": ""
        }
        
        try:
            # Step 1: Collect all files to scan
            self.update_state(current_task="Scanning directories for files", progress_percent=5)
            all_files = []
            
            for target_dir in self.target_dirs:
                dir_path = self.repo_root / target_dir
                files = self.scan_directory_for_files(dir_path)
                all_files.extend(files)
                self.logger.info(f"📂 {target_dir}: {len(files)} files found")
            
            results["files_scanned"] = len(all_files)
            self.logger.info(f"📊 Total files to scan: {len(all_files)}")
            
            if not all_files:
                self.logger.warning("⚠️  No files found to scan")
                return results
            
            # Step 2: Find exact duplicates
            exact_duplicates = self.find_exact_duplicates(all_files)
            results["exact_duplicates"] = len(exact_duplicates)
            
            # Step 3: Find similar duplicates
            similar_groups = self.find_similar_duplicates(all_files)
            results["similar_groups"] = len(similar_groups)
            
            # Step 4: Analyze and create recommendations
            analysis = self.analyze_duplicates(exact_duplicates, similar_groups)
            results["space_savings_mb"] = analysis["space_savings"] / 1024 / 1024
            
            # Step 5: Generate report
            report_path = self.generate_report(analysis)
            results["report_path"] = str(report_path)
            
            # Save analysis data
            analysis_path = self.state_dir / f"{self.agent_name}_analysis.json"
            with open(analysis_path, 'w') as f:
                json.dump(analysis, f, indent=2, default=str)
            
            # Final success update
            results["success"] = True
            self.update_state(
                current_task="Duplicate detection completed",
                progress_percent=100,
                status="completed",
                duplicates_found=results["exact_duplicates"] + results["similar_groups"],
                files_processed=results["files_scanned"]
            )
            
            self.logger.info(f"✅ {self.agent_name} completed successfully")
            
        except Exception as e:
            self.logger.error(f"❌ {self.agent_name} execution failed: {e}")
            results["success"] = False
            results["error"] = str(e)
            self.update_state(
                current_task=f"Execution failed: {e}",
                status="failed"
            )
        
        results["end_time"] = datetime.now().isoformat()
        return results


def main():
    """Main agent execution"""
    agent = DuplicateHunterAgent()
    result = agent.execute()
    
    # Print result summary
    print("\n" + "="*60)
    print("🔍 DUPLICATE HUNTER AGENT RESULTS")
    print("="*60)
    print(f"✅ Success: {result['success']}")
    print(f"📁 Files Scanned: {result['files_scanned']}")
    print(f"🔄 Exact Duplicates: {result['exact_duplicates']}")
    print(f"📊 Similar Groups: {result['similar_groups']}")
    print(f"💾 Space Savings: {result['space_savings_mb']:.1f} MB")
    
    if result.get('report_path'):
        print(f"📋 Report: {result['report_path']}")
    
    if not result['success'] and 'error' in result:
        print(f"\n❌ Error: {result['error']}")
    
    print("="*60)
    
    return 0 if result['success'] else 1


if __name__ == "__main__":
    exit(main())