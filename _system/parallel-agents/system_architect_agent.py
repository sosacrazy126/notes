#!/usr/bin/env python3
"""
System Architect Agent
======================

Final agent that designs and implements the optimized workspace structure 
for the system thinking tool based on analysis from all other agents.

Author: Claude Code Agent System
Date: 2025-08-10
Version: 1.0.0
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Any, Tuple, Optional
import logging
import threading


class SystemArchitectAgent:
    """Agent for designing and implementing final workspace architecture"""
    
    def __init__(self):
        self.repo_root = Path(os.environ.get("REPO_ROOT", "."))
        self.state_dir = Path(os.environ.get("STATE_DIR", "."))
        self.agent_name = os.environ.get("AGENT_NAME", "system-architect")
        
        # Setup logging
        self.setup_logging()
        
        # New workspace architecture
        self.new_structure = {
            "core": {
                "description": "Essential system thinking tools and frameworks",
                "subdirs": {
                    "agents": "Curated active agents for development workflows",
                    "patterns": "Extracted patterns library from pattern-extractor",
                    "workflows": "Working development workflows and processes",
                    "templates": "Reusable templates for common tasks"
                }
            },
            "knowledge": {
                "description": "Consolidated documentation and reference materials",
                "subdirs": {
                    "quick-reference": "Fast lookup guides and cheat sheets",
                    "deep-dive": "Comprehensive documentation and tutorials",
                    "api-docs": "API documentation and specifications",
                    "guides": "Step-by-step implementation guides"
                }
            },
            "active-projects": {
                "description": "Current work areas and active development",
                "subdirs": {
                    "experiments": "Experimental features and prototypes",
                    "tools": "Utility tools and scripts in development"
                }
            },
            "tools": {
                "description": "Production-ready utilities and automation",
                "subdirs": {
                    "automation": "Automation scripts and workflows",
                    "cli": "Command-line tools and utilities",
                    "integrations": "Third-party integrations and connectors"
                }
            },
            "_archive": {
                "description": "Historical content and low-value materials",
                "subdirs": {
                    "legacy": "Deprecated systems and old implementations",
                    "backups": "System backups and safety copies",
                    "low-value": "Content marked for archival by content evaluator"
                }
            }
        }
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Migration tracking
        self.migration_log = []
        self.moved_files = []
        self.created_dirs = []
        
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
                    "directories_created": 0,
                    "files_moved": 0
                }
            
            # Update with provided values
            state.update(kwargs)
            state["last_update"] = datetime.now().isoformat()
            
            # Save updated state
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)
    
    def load_agent_results(self) -> Dict[str, Any]:
        """Load results from other agents"""
        self.logger.info("📊 Loading results from other agents...")
        self.update_state(current_task="Loading agent results", progress_percent=5)
        
        agent_results = {
            "duplicate_hunter": {},
            "content_evaluator": {},
            "pattern_extractor": {},
            "workspace_optimizer": {}
        }
        
        # Load results files
        for agent_name in agent_results.keys():
            results_file = self.state_dir / f"{agent_name}_results.json"
            if results_file.exists():
                try:
                    with open(results_file, 'r') as f:
                        agent_results[agent_name] = json.load(f)
                    self.logger.info(f"✅ Loaded {agent_name} results")
                except Exception as e:
                    self.logger.warning(f"Could not load {agent_name} results: {e}")
            
            # Also try detailed results
            detailed_file = self.state_dir / f"{agent_name}_detailed_results.json"
            if detailed_file.exists():
                try:
                    with open(detailed_file, 'r') as f:
                        detailed_data = json.load(f)
                        agent_results[agent_name]["detailed"] = detailed_data
                    self.logger.info(f"✅ Loaded {agent_name} detailed results")
                except Exception as e:
                    self.logger.warning(f"Could not load {agent_name} detailed results: {e}")
        
        return agent_results
    
    def create_new_directory_structure(self):
        """Create the new workspace directory structure"""
        self.logger.info("🏗️ Creating new directory structure...")
        self.update_state(current_task="Creating directory structure", progress_percent=15)
        
        created_dirs = []
        
        for main_dir, config in self.new_structure.items():
            main_path = self.repo_root / main_dir
            
            # Create main directory if it doesn't exist
            if not main_path.exists():
                main_path.mkdir(parents=True, exist_ok=True)
                created_dirs.append(str(main_path))
                self.logger.info(f"📁 Created: {main_path}")
            
            # Create subdirectories
            if "subdirs" in config:
                for subdir_name, subdir_desc in config["subdirs"].items():
                    subdir_path = main_path / subdir_name
                    if not subdir_path.exists():
                        subdir_path.mkdir(parents=True, exist_ok=True)
                        created_dirs.append(str(subdir_path))
                    
                    # Create README for each subdirectory
                    readme_path = subdir_path / "README.md"
                    if not readme_path.exists():
                        readme_content = f"# {subdir_name.replace('-', ' ').title()}\n\n{subdir_desc}\n\n*Directory created: {datetime.now().isoformat()}*\n"
                        with open(readme_path, 'w') as f:
                            f.write(readme_content)
        
        self.created_dirs = created_dirs
        self.logger.info(f"✅ Created {len(created_dirs)} directories")
        
        return created_dirs
    
    def migrate_high_value_content(self, agent_results: Dict[str, Any]):
        """Migrate high-value content to appropriate locations"""
        self.logger.info("📦 Migrating high-value content...")
        self.update_state(current_task="Migrating high-value content", progress_percent=30)
        
        migration_actions = []
        
        # Process content evaluator recommendations
        content_eval = agent_results.get("content_evaluator", {}).get("detailed", {})
        if content_eval:
            recommendations = content_eval.get("recommendations", {})
            
            # Keep high-value files in appropriate locations
            for item in recommendations.get("keep", []):
                file_path = Path(item["file_path"])
                if file_path.exists():
                    new_location = self.determine_new_location(file_path, item)
                    if new_location:
                        migration_actions.append({
                            "action": "move",
                            "source": str(file_path),
                            "destination": str(new_location),
                            "reason": f"High-value content (score: {item['score']:.3f})"
                        })
            
            # Move archive-recommended files
            for item in recommendations.get("archive", []):
                file_path = Path(item["file_path"])
                if file_path.exists():
                    archive_location = self.repo_root / "_archive" / "low-value" / file_path.name
                    migration_actions.append({
                        "action": "move", 
                        "source": str(file_path),
                        "destination": str(archive_location),
                        "reason": f"Low-value content (score: {item['score']:.3f})"
                    })
        
        # Process pattern extractor results
        pattern_data = agent_results.get("pattern_extractor", {})
        if pattern_data.get("library_path"):
            library_source = Path(pattern_data["library_path"])
            library_dest = self.repo_root / "core" / "patterns"
            
            if library_source.exists() and library_source != library_dest:
                migration_actions.append({
                    "action": "copy_tree",
                    "source": str(library_source),
                    "destination": str(library_dest),
                    "reason": "Pattern library from pattern extractor"
                })
        
        # Migrate system configuration files
        system_configs = [
            "_system/claude_config",
            "_system/agents", 
            "_system/scripts"
        ]
        
        for config_path in system_configs:
            source = self.repo_root / config_path
            if source.exists():
                dest = self.repo_root / "core" / source.name
                migration_actions.append({
                    "action": "copy_tree",
                    "source": str(source),
                    "destination": str(dest),
                    "reason": "Essential system configuration"
                })
        
        # Execute migration actions
        return self.execute_migration_actions(migration_actions)
    
    def determine_new_location(self, file_path: Path, content_info: Dict) -> Optional[Path]:
        """Determine appropriate new location for a file"""
        file_path_str = str(file_path).lower()
        file_name = file_path.name.lower()
        
        # Agent-related files
        if "agent" in file_name or "agent" in file_path_str:
            return self.repo_root / "core" / "agents" / file_path.name
        
        # Template files
        if "template" in file_name or "pattern" in file_name:
            return self.repo_root / "core" / "templates" / file_path.name
        
        # Workflow files
        if "workflow" in file_name or "process" in file_name:
            return self.repo_root / "core" / "workflows" / file_path.name
        
        # Documentation files
        if file_path.suffix == '.md':
            if "guide" in file_name or "tutorial" in file_name:
                return self.repo_root / "knowledge" / "deep-dive" / file_path.name
            elif "reference" in file_name or "api" in file_name:
                return self.repo_root / "knowledge" / "quick-reference" / file_path.name
            else:
                return self.repo_root / "knowledge" / "guides" / file_path.name
        
        # Configuration files
        if file_path.suffix in ['.json', '.yaml', '.yml', '.toml']:
            return self.repo_root / "tools" / "config" / file_path.name
        
        # Script files
        if file_path.suffix in ['.py', '.sh', '.js']:
            return self.repo_root / "tools" / "automation" / file_path.name
        
        return None
    
    def execute_migration_actions(self, migration_actions: List[Dict]) -> List[Dict]:
        """Execute file migration actions"""
        self.logger.info(f"🔄 Executing {len(migration_actions)} migration actions...")
        
        completed_actions = []
        total_actions = len(migration_actions)
        
        for i, action in enumerate(migration_actions):
            try:
                source = Path(action["source"])
                destination = Path(action["destination"])
                
                # Ensure destination directory exists
                destination.parent.mkdir(parents=True, exist_ok=True)
                
                if action["action"] == "move":
                    if source.exists():
                        shutil.move(str(source), str(destination))
                        completed_actions.append(action)
                        self.moved_files.append(str(destination))
                
                elif action["action"] == "copy":
                    if source.exists():
                        if source.is_file():
                            shutil.copy2(str(source), str(destination))
                        else:
                            shutil.copytree(str(source), str(destination), dirs_exist_ok=True)
                        completed_actions.append(action)
                
                elif action["action"] == "copy_tree":
                    if source.exists():
                        if destination.exists():
                            shutil.rmtree(str(destination))
                        shutil.copytree(str(source), str(destination))
                        completed_actions.append(action)
                
                # Update progress
                progress = 30 + (i / total_actions) * 40
                self.update_state(
                    files_processed=i + 1,
                    progress_percent=progress,
                    files_moved=len(completed_actions)
                )
                
            except Exception as e:
                self.logger.warning(f"Migration failed for {action['source']}: {e}")
                action["error"] = str(e)
        
        self.logger.info(f"✅ Completed {len(completed_actions)} migration actions")
        return completed_actions
    
    def create_integration_tools(self, agent_results: Dict[str, Any]):
        """Create tools for workspace integration and management"""
        self.logger.info("🔧 Creating integration tools...")
        self.update_state(current_task="Creating integration tools", progress_percent=75)
        
        tools_created = []
        
        # Create workspace navigator tool
        navigator_tool = self.create_workspace_navigator()
        tools_created.append(navigator_tool)
        
        # Create content search tool
        search_tool = self.create_content_search_tool(agent_results)
        tools_created.append(search_tool)
        
        # Create maintenance automation
        maintenance_tool = self.create_maintenance_automation()
        tools_created.append(maintenance_tool)
        
        # Create workspace health checker
        health_checker = self.create_workspace_health_checker()
        tools_created.append(health_checker)
        
        return tools_created
    
    def create_workspace_navigator(self) -> str:
        """Create workspace navigation tool"""
        navigator_content = '''#!/usr/bin/env python3
"""
Workspace Navigator
==================

Quick navigation and discovery tool for the optimized workspace.
"""

import os
from pathlib import Path

WORKSPACE_STRUCTURE = {
    "core": "Essential system thinking tools and frameworks",
    "knowledge": "Documentation and reference materials", 
    "active-projects": "Current work areas",
    "tools": "Production-ready utilities",
    "_archive": "Historical content"
}

def show_structure():
    """Display workspace structure"""
    print("🏗️  WORKSPACE STRUCTURE")
    print("="*50)
    
    for directory, description in WORKSPACE_STRUCTURE.items():
        path = Path(directory)
        if path.exists():
            file_count = len(list(path.rglob("*")))
            print(f"📁 {directory:15} | {description}")
            print(f"   {file_count} items")
        print()

def find_content(query: str):
    """Find content matching query"""
    print(f"🔍 Searching for: {query}")
    matches = []
    
    for root, dirs, files in os.walk("."):
        for file in files:
            if query.lower() in file.lower():
                matches.append(os.path.join(root, file))
    
    print(f"Found {len(matches)} matches:")
    for match in matches[:10]:  # Show first 10
        print(f"  - {match}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        find_content(sys.argv[1])
    else:
        show_structure()
'''
        
        navigator_path = self.repo_root / "tools" / "cli" / "navigate.py"
        navigator_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(navigator_path, 'w') as f:
            f.write(navigator_content)
        
        navigator_path.chmod(0o755)
        return str(navigator_path)
    
    def create_content_search_tool(self, agent_results: Dict[str, Any]) -> str:
        """Create content search and discovery tool"""
        search_content = '''#!/usr/bin/env python3
"""
Content Search Tool
==================

Advanced content discovery using metadata from agent analysis.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any

class ContentSearcher:
    def __init__(self):
        self.repo_root = Path.cwd()
        self.load_metadata()
    
    def load_metadata(self):
        """Load metadata from agent analysis"""
        self.metadata = {}
        
        # Load content evaluator metadata
        eval_file = Path("_system/parallel-agents/state/content-evaluator_detailed_results.json")
        if eval_file.exists():
            with open(eval_file) as f:
                self.metadata["evaluations"] = json.load(f)
    
    def search_by_score(self, min_score: float = 0.7) -> List[Dict]:
        """Find high-scoring content"""
        results = []
        
        if "evaluations" in self.metadata:
            for eval_data in self.metadata["evaluations"].get("evaluations", []):
                if eval_data.get("composite_score", 0) >= min_score:
                    results.append({
                        "file": eval_data["file_path"],
                        "score": eval_data["composite_score"],
                        "type": eval_data.get("file_extension", "")
                    })
        
        return sorted(results, key=lambda x: x["score"], reverse=True)
    
    def search_by_keyword(self, keyword: str) -> List[str]:
        """Search content by keyword"""
        matches = []
        
        for root, dirs, files in os.walk(self.repo_root):
            # Skip certain directories
            if any(skip in root for skip in [".git", "node_modules", "venv"]):
                continue
            
            for file in files:
                if file.endswith(('.md', '.txt', '.py', '.json')):
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if keyword.lower() in content.lower():
                                matches.append(str(file_path))
                    except:
                        pass
        
        return matches

def main():
    import sys
    
    searcher = ContentSearcher()
    
    if len(sys.argv) < 2:
        print("Usage: python search.py <keyword|--high-score>")
        return
    
    if sys.argv[1] == "--high-score":
        results = searcher.search_by_score()
        print(f"🌟 High-scoring content ({len(results)} files):")
        for result in results[:10]:
            print(f"  {result['score']:.3f} - {result['file']}")
    else:
        keyword = sys.argv[1]
        matches = searcher.search_by_keyword(keyword)
        print(f"🔍 Found {len(matches)} matches for '{keyword}':")
        for match in matches[:10]:
            print(f"  - {match}")

if __name__ == "__main__":
    main()
'''
        
        search_path = self.repo_root / "tools" / "cli" / "search.py"
        search_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(search_path, 'w') as f:
            f.write(search_content)
        
        search_path.chmod(0o755)
        return str(search_path)
    
    def create_maintenance_automation(self) -> str:
        """Create workspace maintenance automation"""
        maintenance_content = '''#!/bin/bash
# Workspace Maintenance Automation
# Runs periodic cleanup and optimization tasks

set -e

echo "🧹 Starting workspace maintenance..."

# Clean temporary files
echo "🗑️  Removing temporary files..."
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name "*.log" -mtime +30 -delete 2>/dev/null || true
find . -name ".DS_Store" -delete 2>/dev/null || true

# Update file counts in README files
echo "📊 Updating directory statistics..."
for readme in */README.md; do
    if [ -f "$readme" ]; then
        dir=$(dirname "$readme")
        count=$(find "$dir" -type f ! -name "README.md" | wc -l)
        # Update file count if line exists
        sed -i "s/\\*Directory created:.*/\\*Directory updated: $(date -I) ($count files)\\*/" "$readme" 2>/dev/null || true
    fi
done

# Validate workspace structure
echo "🔍 Validating workspace structure..."
required_dirs=("core" "knowledge" "active-projects" "tools" "_archive")

for dir in "${required_dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "⚠️  Missing required directory: $dir"
        mkdir -p "$dir"
        echo "📁 Created: $dir"
    fi
done

# Generate workspace health report
echo "📋 Generating health report..."
{
    echo "# Workspace Health Report"
    echo "**Generated:** $(date)"
    echo ""
    echo "## Directory Statistics"
    
    for dir in "${required_dirs[@]}"; do
        if [ -d "$dir" ]; then
            file_count=$(find "$dir" -type f | wc -l)
            dir_size=$(du -sh "$dir" 2>/dev/null | cut -f1)
            echo "- **$dir**: $file_count files, $dir_size"
        fi
    done
    
    echo ""
    echo "## Recent Activity"
    echo "Files modified in last 7 days:"
    find . -type f -mtime -7 | head -10 | while read file; do
        echo "- $file"
    done
    
} > workspace_health_report.md

echo "✅ Maintenance completed!"
echo "📊 Health report: workspace_health_report.md"
'''
        
        maintenance_path = self.repo_root / "tools" / "automation" / "maintain_workspace.sh"
        maintenance_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(maintenance_path, 'w') as f:
            f.write(maintenance_content)
        
        maintenance_path.chmod(0o755)
        return str(maintenance_path)
    
    def create_workspace_health_checker(self) -> str:
        """Create workspace health monitoring tool"""
        health_checker_content = '''#!/usr/bin/env python3
"""
Workspace Health Checker
========================

Monitors workspace health and provides recommendations.
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any

class WorkspaceHealthChecker:
    def __init__(self):
        self.repo_root = Path.cwd()
        self.health_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_health": "unknown",
            "checks": {},
            "recommendations": []
        }
    
    def check_directory_structure(self) -> Dict[str, Any]:
        """Check if required directories exist"""
        required_dirs = ["core", "knowledge", "active-projects", "tools", "_archive"]
        missing_dirs = []
        
        for dir_name in required_dirs:
            dir_path = self.repo_root / dir_name
            if not dir_path.exists():
                missing_dirs.append(dir_name)
        
        status = "healthy" if not missing_dirs else "warning"
        
        return {
            "name": "Directory Structure",
            "status": status,
            "details": {
                "required_directories": len(required_dirs),
                "existing_directories": len(required_dirs) - len(missing_dirs),
                "missing_directories": missing_dirs
            }
        }
    
    def check_file_distribution(self) -> Dict[str, Any]:
        """Check file distribution across directories"""
        distribution = {}
        total_files = 0
        
        for item in self.repo_root.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                file_count = len(list(item.rglob("*")))
                distribution[item.name] = file_count
                total_files += file_count
        
        # Check if any directory has too many files (> 50% of total)
        max_ratio = max(distribution.values()) / total_files if total_files > 0 else 0
        status = "healthy" if max_ratio < 0.5 else "warning"
        
        return {
            "name": "File Distribution",
            "status": status,
            "details": {
                "total_files": total_files,
                "distribution": distribution,
                "max_concentration": f"{max_ratio:.1%}"
            }
        }
    
    def check_recent_activity(self) -> Dict[str, Any]:
        """Check for recent file modifications"""
        recent_threshold = datetime.now() - timedelta(days=7)
        recent_files = []
        
        for file_path in self.repo_root.rglob("*"):
            if file_path.is_file():
                try:
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mtime > recent_threshold:
                        recent_files.append(str(file_path))
                except:
                    pass
        
        status = "healthy" if recent_files else "warning"
        
        return {
            "name": "Recent Activity",
            "status": status,
            "details": {
                "recent_files": len(recent_files),
                "sample_files": recent_files[:5]
            }
        }
    
    def check_workspace_size(self) -> Dict[str, Any]:
        """Check overall workspace size"""
        total_size = 0
        large_dirs = []
        
        for item in self.repo_root.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                dir_size = sum(f.stat().st_size for f in item.rglob("*") if f.is_file())
                total_size += dir_size
                
                if dir_size > 100 * 1024 * 1024:  # > 100MB
                    large_dirs.append({
                        "name": item.name,
                        "size_mb": dir_size / 1024 / 1024
                    })
        
        status = "healthy" if total_size < 1024 * 1024 * 1024 else "warning"  # < 1GB
        
        return {
            "name": "Workspace Size",
            "status": status,
            "details": {
                "total_size_mb": total_size / 1024 / 1024,
                "large_directories": large_dirs
            }
        }
    
    def run_all_checks(self):
        """Run all health checks"""
        checks = [
            self.check_directory_structure(),
            self.check_file_distribution(),
            self.check_recent_activity(),
            self.check_workspace_size()
        ]
        
        self.health_report["checks"] = {check["name"]: check for check in checks}
        
        # Determine overall health
        statuses = [check["status"] for check in checks]
        if all(status == "healthy" for status in statuses):
            self.health_report["overall_health"] = "healthy"
        elif any(status == "error" for status in statuses):
            self.health_report["overall_health"] = "error" 
        else:
            self.health_report["overall_health"] = "warning"
        
        # Generate recommendations
        self.generate_recommendations()
    
    def generate_recommendations(self):
        """Generate health recommendations"""
        recommendations = []
        
        for check_name, check in self.health_report["checks"].items():
            if check["status"] != "healthy":
                if check_name == "Directory Structure":
                    if check["details"]["missing_directories"]:
                        recommendations.append(
                            f"Create missing directories: {', '.join(check['details']['missing_directories'])}"
                        )
                
                elif check_name == "File Distribution":
                    if check["details"]["max_concentration"] > "50.0%":
                        recommendations.append("Consider redistributing files to balance directory sizes")
                
                elif check_name == "Recent Activity":
                    if check["details"]["recent_files"] == 0:
                        recommendations.append("Workspace appears inactive - consider archiving if no longer used")
                
                elif check_name == "Workspace Size":
                    if check["details"]["total_size_mb"] > 1000:
                        recommendations.append("Workspace is large - consider running cleanup tools")
        
        self.health_report["recommendations"] = recommendations
    
    def save_report(self):
        """Save health report to file"""
        report_path = self.repo_root / "workspace_health_report.json"
        with open(report_path, 'w') as f:
            json.dump(self.health_report, f, indent=2)
        return report_path
    
    def print_summary(self):
        """Print health summary"""
        health_icons = {
            "healthy": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        
        print(f"🏥 WORKSPACE HEALTH CHECK")
        print(f"Overall: {health_icons[self.health_report['overall_health']]} {self.health_report['overall_health'].upper()}")
        print()
        
        for check_name, check in self.health_report["checks"].items():
            icon = health_icons[check["status"]]
            print(f"{icon} {check_name}: {check['status']}")
        
        if self.health_report["recommendations"]:
            print()
            print("💡 RECOMMENDATIONS:")
            for rec in self.health_report["recommendations"]:
                print(f"  - {rec}")

def main():
    checker = WorkspaceHealthChecker()
    checker.run_all_checks()
    
    report_path = checker.save_report()
    checker.print_summary()
    
    print(f"\\n📋 Full report saved: {report_path}")

if __name__ == "__main__":
    main()
'''
        
        health_path = self.repo_root / "tools" / "cli" / "health_check.py"
        health_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(health_path, 'w') as f:
            f.write(health_checker_content)
        
        health_path.chmod(0o755)
        return str(health_path)
    
    def generate_architecture_documentation(self, agent_results: Dict[str, Any], migration_log: List[Dict]) -> str:
        """Generate comprehensive architecture documentation"""
        self.logger.info("📝 Generating architecture documentation...")
        
        doc_lines = [
            "# Optimized Workspace Architecture",
            f"**Created**: {datetime.now().isoformat()}",
            f"**Agent**: {self.agent_name}",
            "",
            "## Overview",
            "",
            "This document describes the optimized workspace architecture created by the",
            "System Architect Agent based on analysis from parallel sub-agents.",
            "",
            "## Architecture Principles",
            "",
            "1. **Clarity**: Clear separation of concerns with logical directory structure",
            "2. **Accessibility**: Easy discovery and navigation of content",
            "3. **Maintainability**: Sustainable organization that supports growth",
            "4. **Integration**: Seamless tool integration and workflow automation",
            "",
            "## Directory Structure",
            ""
        ]
        
        for main_dir, config in self.new_structure.items():
            doc_lines.extend([
                f"### `{main_dir}/`",
                f"{config['description']}",
                ""
            ])
            
            if "subdirs" in config:
                for subdir, desc in config["subdirs"].items():
                    doc_lines.append(f"- **`{subdir}/`**: {desc}")
                doc_lines.append("")
        
        # Migration summary
        if migration_log:
            doc_lines.extend([
                "## Migration Summary",
                "",
                f"**Total Actions**: {len(migration_log)}",
                f"**Files Moved**: {len([a for a in migration_log if a.get('action') == 'move'])}",
                f"**Files Copied**: {len([a for a in migration_log if a.get('action') in ['copy', 'copy_tree']])}",
                ""
            ])
        
        # Agent analysis summary
        doc_lines.extend([
            "## Agent Analysis Summary",
            ""
        ])
        
        for agent_name, results in agent_results.items():
            if results:
                doc_lines.extend([
                    f"### {agent_name.replace('_', ' ').title()}",
                ])
                
                if agent_name == "duplicate_hunter":
                    doc_lines.append(f"- Duplicate sets found: {results.get('exact_duplicates', 0)}")
                    doc_lines.append(f"- Space savings: {results.get('space_savings_mb', 0):.1f} MB")
                
                elif agent_name == "content_evaluator":
                    doc_lines.append(f"- Files evaluated: {results.get('files_evaluated', 0)}")
                    doc_lines.append(f"- Average score: {results.get('avg_score', 0):.3f}")
                    doc_lines.append(f"- Keep recommendations: {results.get('recommendations_keep', 0)}")
                    doc_lines.append(f"- Archive recommendations: {results.get('recommendations_archive', 0)}")
                
                elif agent_name == "pattern_extractor":
                    doc_lines.append(f"- Patterns extracted: {results.get('patterns_extracted', 0)}")
                    doc_lines.append(f"- Categories created: {results.get('categories_created', 0)}")
                
                elif agent_name == "workspace_optimizer":
                    doc_lines.append(f"- Projects found: {results.get('projects_found', 0)}")
                    doc_lines.append(f"- Items deleted: {results.get('items_deleted', 0)}")
                    doc_lines.append(f"- Space freed: {results.get('space_freed_mb', 0):.1f} MB")
                
                doc_lines.append("")
        
        # Integration tools
        doc_lines.extend([
            "## Integration Tools",
            "",
            "The following tools have been created for workspace management:",
            "",
            "- **`tools/cli/navigate.py`**: Workspace navigation and discovery",
            "- **`tools/cli/search.py`**: Content search with metadata integration", 
            "- **`tools/cli/health_check.py`**: Workspace health monitoring",
            "- **`tools/automation/maintain_workspace.sh`**: Automated maintenance",
            "",
            "## Usage Guidelines",
            "",
            "### For Development Work",
            "1. Store active agents in `core/agents/`",
            "2. Use `core/workflows/` for process documentation",
            "3. Place utilities in `tools/automation/` or `tools/cli/`",
            "",
            "### For Documentation",
            "1. Quick references go in `knowledge/quick-reference/`",
            "2. Comprehensive guides in `knowledge/deep-dive/`",
            "3. API docs in `knowledge/api-docs/`",
            "",
            "### For Maintenance",
            "1. Run `tools/automation/maintain_workspace.sh` weekly",
            "2. Check health with `tools/cli/health_check.py`",
            "3. Archive old content periodically",
            "",
            "## Future Enhancements",
            "",
            "- Automated content categorization based on machine learning",
            "- Integration with external knowledge management systems",  
            "- Advanced search with semantic similarity",
            "- Workflow automation and task orchestration",
            "",
            f"---",
            f"*Architecture created by {self.agent_name} on {datetime.now().strftime('%Y-%m-%d')}*"
        ]
        
        doc_content = "\n".join(doc_lines)
        doc_path = self.repo_root / "ARCHITECTURE.md"
        
        with open(doc_path, 'w') as f:
            f.write(doc_content)
        
        self.logger.info(f"✅ Architecture documentation saved: {doc_path}")
        return str(doc_path)
    
    def execute(self) -> Dict[str, Any]:
        """Main agent execution"""
        self.logger.info(f"🚀 Starting {self.agent_name} execution")
        self.update_state(current_task="Initializing system architecture", progress_percent=0)
        
        results = {
            "agent_name": self.agent_name,
            "start_time": datetime.now().isoformat(),
            "success": False,
            "directories_created": 0,
            "files_migrated": 0,
            "tools_created": 0,
            "architecture_doc": ""
        }
        
        try:
            # Step 1: Load agent results
            agent_results = self.load_agent_results()
            
            # Step 2: Create new directory structure
            created_dirs = self.create_new_directory_structure()
            results["directories_created"] = len(created_dirs)
            
            # Step 3: Migrate high-value content
            migration_log = self.migrate_high_value_content(agent_results)
            results["files_migrated"] = len(migration_log)
            
            # Step 4: Create integration tools
            tools_created = self.create_integration_tools(agent_results)
            results["tools_created"] = len(tools_created)
            
            # Step 5: Generate architecture documentation
            self.update_state(current_task="Generating architecture documentation", progress_percent=90)
            arch_doc = self.generate_architecture_documentation(agent_results, migration_log)
            results["architecture_doc"] = arch_doc
            
            # Save detailed results
            detailed_results = {
                "created_directories": created_dirs,
                "migration_log": migration_log,
                "tools_created": tools_created,
                "agent_results_summary": agent_results
            }
            
            results_path = self.state_dir / f"{self.agent_name}_results.json"
            with open(results_path, 'w') as f:
                json.dump(detailed_results, f, indent=2, default=str)
            
            # Final success update
            results["success"] = True
            self.update_state(
                current_task="System architecture completed",
                progress_percent=100,
                status="completed",
                directories_created=results["directories_created"],
                files_moved=results["files_migrated"],
                files_processed=results["files_migrated"]
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
    agent = SystemArchitectAgent()
    result = agent.execute()
    
    # Print result summary
    print("\n" + "="*60)
    print("🏗️  SYSTEM ARCHITECT AGENT RESULTS")
    print("="*60)
    print(f"✅ Success: {result['success']}")
    print(f"📁 Directories Created: {result['directories_created']}")
    print(f"📦 Files Migrated: {result['files_migrated']}")
    print(f"🔧 Tools Created: {result['tools_created']}")
    
    if result.get('architecture_doc'):
        print(f"📋 Architecture Doc: {result['architecture_doc']}")
    
    if not result['success'] and 'error' in result:
        print(f"\n❌ Error: {result['error']}")
    
    print("="*60)
    
    return 0 if result['success'] else 1


if __name__ == "__main__":
    exit(main())