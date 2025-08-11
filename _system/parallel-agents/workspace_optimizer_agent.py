#!/usr/bin/env python3
"""
Workspace Optimizer Agent
========================

Specialized agent for cleaning heavy directories and optimizing workspace structure.
Targets venv/, node_modules/, __pycache__/, cache files, and other build artifacts.

Author: Claude Code Agent System
Date: 2025-08-10  
Version: 1.0.0
"""

import os
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Any, Tuple, Optional
import logging
import threading
import glob
import tarfile
import time


class WorkspaceOptimizerAgent:
    """Agent for workspace optimization and cleanup"""
    
    def __init__(self):
        self.repo_root = Path(os.environ.get("REPO_ROOT", "."))
        self.state_dir = Path(os.environ.get("STATE_DIR", "."))
        self.agent_name = os.environ.get("AGENT_NAME", "workspace-optimizer")
        
        # Target directory
        self.target_dirs = ["workspace"]
        
        # Setup logging
        self.setup_logging()
        
        # Cleanup configuration
        self.heavy_patterns = [
            "venv/",
            ".venv/",
            "env/",
            "node_modules/",
            "__pycache__/",
            "*.pyc",
            ".pytest_cache/",
            ".coverage", 
            ".nyc_output/",
            "coverage/",
            "dist/",
            "build/",
            ".egg-info/",
            "*.egg-info/",
            ".cache/",
            ".tox/",
            ".mypy_cache/",
            ".DS_Store",
            "*.log",
            "*.tmp",
            ".git/logs/",
            ".git/refs/remotes/",
        ]
        
        self.preserve_patterns = [
            "requirements.txt",
            "package.json",
            "pyproject.toml",
            "setup.py",
            "Pipfile",
            "environment.yml",
            ".gitignore",
            "README.md",
            "CLAUDE.md",
            "LICENSE"
        ]
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Tracking
        self.deleted_items = []
        self.archived_items = []
        self.space_freed = 0
        self.processed_projects = []
        
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
                    "space_freed_mb": 0
                }
            
            # Update with provided values
            state.update(kwargs)
            state["last_update"] = datetime.now().isoformat()
            
            # Save updated state
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)
    
    def calculate_directory_size(self, directory: Path) -> int:
        """Calculate total size of directory in bytes"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = Path(dirpath) / filename
                    try:
                        total_size += filepath.stat().st_size
                    except (OSError, FileNotFoundError):
                        continue
        except Exception as e:
            self.logger.warning(f"Could not calculate size of {directory}: {e}")
        
        return total_size
    
    def find_heavy_directories(self) -> List[Tuple[Path, str, int]]:
        """Find directories matching heavy patterns"""
        self.logger.info("🔍 Scanning for heavy directories...")
        self.update_state(current_task="Scanning for heavy directories", progress_percent=10)
        
        heavy_dirs = []
        
        for target_dir in self.target_dirs:
            workspace_path = self.repo_root / target_dir
            if not workspace_path.exists():
                continue
            
            # Find all potential heavy directories
            for pattern in self.heavy_patterns:
                if pattern.endswith('/'):
                    # Directory pattern
                    pattern_path = pattern.rstrip('/')
                    for match in workspace_path.rglob(pattern_path):
                        if match.is_dir():
                            size = self.calculate_directory_size(match)
                            heavy_dirs.append((match, pattern, size))
                else:
                    # File pattern  
                    for match in workspace_path.rglob(pattern):
                        if match.is_file():
                            try:
                                size = match.stat().st_size
                                heavy_dirs.append((match, pattern, size))
                            except (OSError, FileNotFoundError):
                                continue
        
        # Sort by size (largest first)
        heavy_dirs.sort(key=lambda x: x[2], reverse=True)
        
        total_size = sum(item[2] for item in heavy_dirs)
        self.logger.info(f"✅ Found {len(heavy_dirs)} heavy items ({total_size/1024/1024:.1f} MB)")
        
        return heavy_dirs
    
    def categorize_projects(self) -> Dict[str, Dict[str, Any]]:
        """Identify and categorize projects in workspace"""
        self.logger.info("📊 Categorizing workspace projects...")
        self.update_state(current_task="Categorizing projects", progress_percent=20)
        
        projects = {}
        
        for target_dir in self.target_dirs:
            workspace_path = self.repo_root / target_dir
            if not workspace_path.exists():
                continue
            
            # Look for project indicators
            project_indicators = [
                "package.json",
                "requirements.txt", 
                "pyproject.toml",
                "setup.py",
                "Cargo.toml",
                "go.mod",
                "pom.xml",
                "build.gradle",
                "Makefile"
            ]
            
            for indicator in project_indicators:
                for project_file in workspace_path.rglob(indicator):
                    project_root = project_file.parent
                    
                    # Skip if already found this project
                    if str(project_root) in projects:
                        continue
                    
                    # Determine project type
                    project_type = self.determine_project_type(project_file)
                    
                    # Calculate project size
                    project_size = self.calculate_directory_size(project_root)
                    
                    # Check for heavy directories within project
                    heavy_items = []
                    for pattern in self.heavy_patterns:
                        if pattern.endswith('/'):
                            pattern_dir = project_root / pattern.rstrip('/')
                            if pattern_dir.exists():
                                size = self.calculate_directory_size(pattern_dir)
                                heavy_items.append({
                                    "path": str(pattern_dir),
                                    "pattern": pattern,
                                    "size": size
                                })
                    
                    projects[str(project_root)] = {
                        "type": project_type,
                        "indicator_file": str(project_file),
                        "total_size": project_size,
                        "heavy_items": heavy_items,
                        "heavy_size": sum(item["size"] for item in heavy_items),
                        "status": "active" if self.is_active_project(project_root) else "inactive"
                    }
        
        self.logger.info(f"✅ Found {len(projects)} projects")
        return projects
    
    def determine_project_type(self, project_file: Path) -> str:
        """Determine project type from indicator file"""
        filename = project_file.name
        
        type_mapping = {
            "package.json": "nodejs",
            "requirements.txt": "python",
            "pyproject.toml": "python",
            "setup.py": "python",
            "Pipfile": "python", 
            "Cargo.toml": "rust",
            "go.mod": "golang",
            "pom.xml": "java",
            "build.gradle": "java",
            "Makefile": "c/cpp"
        }
        
        return type_mapping.get(filename, "unknown")
    
    def is_active_project(self, project_root: Path) -> bool:
        """Determine if project is actively being worked on"""
        # Check for recent modifications
        try:
            recent_threshold = datetime.now().timestamp() - (30 * 24 * 60 * 60)  # 30 days
            
            for file_path in project_root.rglob("*"):
                if file_path.is_file() and not any(pattern in str(file_path) for pattern in ["/.git/", "node_modules/", "venv/", "__pycache__/"]):
                    try:
                        if file_path.stat().st_mtime > recent_threshold:
                            return True
                    except (OSError, FileNotFoundError):
                        continue
        except Exception:
            pass
        
        return False
    
    def create_project_archive(self, project_path: Path, heavy_items: List[Dict]) -> Optional[Path]:
        """Create archive of heavy items before deletion"""
        if not heavy_items:
            return None
        
        try:
            archive_dir = self.state_dir / "archived_heavy_items"
            archive_dir.mkdir(exist_ok=True)
            
            project_name = project_path.name
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            archive_path = archive_dir / f"{project_name}_{timestamp}.tar.gz"
            
            with tarfile.open(archive_path, "w:gz") as tar:
                for item in heavy_items:
                    item_path = Path(item["path"])
                    if item_path.exists():
                        # Add with project-relative path
                        arcname = item_path.relative_to(project_path)
                        tar.add(item_path, arcname=arcname)
            
            self.logger.info(f"📦 Archived heavy items to: {archive_path}")
            return archive_path
            
        except Exception as e:
            self.logger.warning(f"Could not create archive for {project_path}: {e}")
            return None
    
    def clean_heavy_items(self, heavy_dirs: List[Tuple[Path, str, int]], projects: Dict[str, Dict]) -> Dict[str, Any]:
        """Clean identified heavy items"""
        self.logger.info("🧹 Cleaning heavy items...")
        self.update_state(current_task="Cleaning heavy directories", progress_percent=40)
        
        cleanup_results = {
            "deleted_items": [],
            "archived_items": [],
            "skipped_items": [],
            "space_freed": 0,
            "errors": []
        }
        
        processed = 0
        total_items = len(heavy_dirs)
        
        for item_path, pattern, size in heavy_dirs:
            try:
                # Check if item is in a critical project
                should_skip = False
                project_context = None
                
                for project_root, project_info in projects.items():
                    if str(item_path).startswith(project_root):
                        project_context = project_info
                        # Skip if project is active and item is critical
                        if project_info["status"] == "active" and pattern in ["requirements.txt", "package.json"]:
                            should_skip = True
                            break
                
                if should_skip:
                    cleanup_results["skipped_items"].append({
                        "path": str(item_path),
                        "pattern": pattern,
                        "size": size,
                        "reason": "active_project_critical_file"
                    })
                    continue
                
                # Archive if it's a large directory in an active project
                if (project_context and 
                    project_context["status"] == "active" and 
                    item_path.is_dir() and 
                    size > 10 * 1024 * 1024):  # > 10MB
                    
                    archive_path = self.create_project_archive(
                        Path(list(projects.keys())[0]), 
                        [{"path": str(item_path), "pattern": pattern, "size": size}]
                    )
                    
                    if archive_path:
                        cleanup_results["archived_items"].append({
                            "path": str(item_path),
                            "archive": str(archive_path),
                            "size": size
                        })
                
                # Delete the item
                if item_path.exists():
                    if item_path.is_dir():
                        shutil.rmtree(item_path, ignore_errors=True)
                    else:
                        item_path.unlink()
                    
                    cleanup_results["deleted_items"].append({
                        "path": str(item_path),
                        "pattern": pattern,
                        "size": size
                    })
                    cleanup_results["space_freed"] += size
                    self.space_freed += size
                
            except Exception as e:
                cleanup_results["errors"].append({
                    "path": str(item_path),
                    "error": str(e)
                })
                self.logger.warning(f"Could not delete {item_path}: {e}")
            
            processed += 1
            progress = 40 + (processed / total_items) * 40
            self.update_state(
                files_processed=processed,
                progress_percent=progress,
                space_freed_mb=cleanup_results["space_freed"] / 1024 / 1024
            )
        
        self.logger.info(f"✅ Cleaned {len(cleanup_results['deleted_items'])} items, freed {cleanup_results['space_freed']/1024/1024:.1f} MB")
        return cleanup_results
    
    def optimize_git_repositories(self) -> Dict[str, Any]:
        """Optimize git repositories in workspace"""
        self.logger.info("🔧 Optimizing git repositories...")
        self.update_state(current_task="Optimizing git repositories", progress_percent=80)
        
        optimization_results = {
            "repositories_optimized": [],
            "space_saved": 0,
            "errors": []
        }
        
        # Find git repositories
        for target_dir in self.target_dirs:
            workspace_path = self.repo_root / target_dir
            if not workspace_path.exists():
                continue
            
            for git_dir in workspace_path.rglob(".git"):
                if not git_dir.is_dir():
                    continue
                
                repo_root = git_dir.parent
                
                try:
                    # Get initial size
                    initial_size = self.calculate_directory_size(git_dir)
                    
                    # Run git gc
                    subprocess.run(["git", "gc", "--aggressive", "--prune=now"], 
                                 cwd=repo_root, capture_output=True)
                    
                    # Get final size
                    final_size = self.calculate_directory_size(git_dir)
                    space_saved = initial_size - final_size
                    
                    if space_saved > 0:
                        optimization_results["repositories_optimized"].append({
                            "path": str(repo_root),
                            "initial_size": initial_size,
                            "final_size": final_size,
                            "space_saved": space_saved
                        })
                        optimization_results["space_saved"] += space_saved
                    
                except Exception as e:
                    optimization_results["errors"].append({
                        "path": str(repo_root),
                        "error": str(e)
                    })
        
        self.logger.info(f"✅ Optimized {len(optimization_results['repositories_optimized'])} repositories")
        return optimization_results
    
    def generate_report(self, projects: Dict, cleanup_results: Dict, optimization_results: Dict):
        """Generate workspace optimization report"""
        self.logger.info("📝 Generating optimization report...")
        
        report_lines = [
            "# Workspace Optimization Report",
            f"**Generated**: {datetime.now().isoformat()}",
            f"**Agent**: {self.agent_name}",
            "",
            "## Summary",
            f"- **Projects Found**: {len(projects)}",
            f"- **Items Deleted**: {len(cleanup_results['deleted_items'])}",
            f"- **Items Archived**: {len(cleanup_results['archived_items'])}",
            f"- **Space Freed**: {cleanup_results['space_freed'] / 1024 / 1024:.1f} MB",
            f"- **Git Repositories Optimized**: {len(optimization_results['repositories_optimized'])}",
            f"- **Total Space Savings**: {(cleanup_results['space_freed'] + optimization_results['space_saved']) / 1024 / 1024:.1f} MB",
            ""
        ]
        
        # Project analysis
        if projects:
            report_lines.extend([
                "## Project Analysis",
                ""
            ])
            
            for project_path, project_info in projects.items():
                status_icon = "🟢" if project_info["status"] == "active" else "🔴"
                report_lines.extend([
                    f"### {status_icon} {Path(project_path).name}",
                    f"- **Type**: {project_info['type']}",
                    f"- **Status**: {project_info['status']}",
                    f"- **Total Size**: {project_info['total_size'] / 1024 / 1024:.1f} MB",
                    f"- **Heavy Items Size**: {project_info['heavy_size'] / 1024 / 1024:.1f} MB",
                    f"- **Heavy Items Count**: {len(project_info['heavy_items'])}",
                    ""
                ])
        
        # Cleanup details
        if cleanup_results['deleted_items']:
            report_lines.extend([
                "## Deleted Items",
                ""
            ])
            
            for item in cleanup_results['deleted_items']:
                size_mb = item['size'] / 1024 / 1024
                report_lines.append(f"- ❌ {item['path']} ({size_mb:.1f} MB)")
            
            report_lines.append("")
        
        # Archived items
        if cleanup_results['archived_items']:
            report_lines.extend([
                "## Archived Items", 
                ""
            ])
            
            for item in cleanup_results['archived_items']:
                size_mb = item['size'] / 1024 / 1024
                report_lines.append(f"- 📦 {item['path']} → {item['archive']} ({size_mb:.1f} MB)")
            
            report_lines.append("")
        
        # Git optimization
        if optimization_results['repositories_optimized']:
            report_lines.extend([
                "## Git Repository Optimization",
                ""
            ])
            
            for repo in optimization_results['repositories_optimized']:
                space_saved_mb = repo['space_saved'] / 1024 / 1024
                report_lines.append(f"- 🔧 {repo['path']} (saved {space_saved_mb:.1f} MB)")
            
            report_lines.append("")
        
        # Errors
        if cleanup_results['errors'] or optimization_results['errors']:
            report_lines.extend([
                "## Errors Encountered",
                ""
            ])
            
            for error in cleanup_results['errors'] + optimization_results['errors']:
                report_lines.append(f"- ⚠️ {error['path']}: {error['error']}")
        
        # Save report
        report_content = "\n".join(report_lines)
        report_path = self.state_dir.parent / "reports" / f"workspace_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write(report_content)
        
        self.logger.info(f"✅ Report saved: {report_path}")
        return report_path
    
    def execute(self) -> Dict[str, Any]:
        """Main agent execution"""
        self.logger.info(f"🚀 Starting {self.agent_name} execution")
        self.update_state(current_task="Initializing workspace optimization", progress_percent=0)
        
        results = {
            "agent_name": self.agent_name,
            "start_time": datetime.now().isoformat(),
            "success": False,
            "projects_found": 0,
            "items_deleted": 0,
            "items_archived": 0,
            "space_freed_mb": 0,
            "report_path": ""
        }
        
        try:
            # Step 1: Find heavy directories
            heavy_dirs = self.find_heavy_directories()
            
            # Step 2: Categorize projects
            projects = self.categorize_projects()
            results["projects_found"] = len(projects)
            
            # Step 3: Clean heavy items
            cleanup_results = self.clean_heavy_items(heavy_dirs, projects)
            results["items_deleted"] = len(cleanup_results["deleted_items"])
            results["items_archived"] = len(cleanup_results["archived_items"]) 
            results["space_freed_mb"] = cleanup_results["space_freed"] / 1024 / 1024
            
            # Step 4: Optimize git repositories
            optimization_results = self.optimize_git_repositories()
            
            # Step 5: Generate report
            report_path = self.generate_report(projects, cleanup_results, optimization_results)
            results["report_path"] = str(report_path)
            
            # Save detailed results
            detailed_results = {
                "projects": projects,
                "cleanup": cleanup_results,
                "optimization": optimization_results
            }
            
            results_path = self.state_dir / f"{self.agent_name}_results.json"
            with open(results_path, 'w') as f:
                json.dump(detailed_results, f, indent=2, default=str)
            
            # Final success update
            results["success"] = True
            self.update_state(
                current_task="Workspace optimization completed",
                progress_percent=100,
                status="completed",
                space_freed_mb=results["space_freed_mb"],
                files_processed=results["items_deleted"] + results["items_archived"]
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
    agent = WorkspaceOptimizerAgent()
    result = agent.execute()
    
    # Print result summary
    print("\n" + "="*60)
    print("🧹 WORKSPACE OPTIMIZER AGENT RESULTS")
    print("="*60)
    print(f"✅ Success: {result['success']}")
    print(f"📁 Projects Found: {result['projects_found']}")
    print(f"🗑️ Items Deleted: {result['items_deleted']}")
    print(f"📦 Items Archived: {result['items_archived']}")
    print(f"💾 Space Freed: {result['space_freed_mb']:.1f} MB")
    
    if result.get('report_path'):
        print(f"📋 Report: {result['report_path']}")
    
    if not result['success'] and 'error' in result:
        print(f"\n❌ Error: {result['error']}")
    
    print("="*60)
    
    return 0 if result['success'] else 1


if __name__ == "__main__":
    exit(main())