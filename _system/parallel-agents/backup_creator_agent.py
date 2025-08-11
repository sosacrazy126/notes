#!/usr/bin/env python3
"""
Backup Creator Agent
===================

Creates comprehensive backup before any destructive operations.
First agent in the parallel optimization pipeline.

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
from typing import Dict, List, Any
import logging


class BackupCreatorAgent:
    """Agent responsible for creating safety backups"""
    
    def __init__(self):
        self.repo_root = Path(os.environ.get("REPO_ROOT", "."))
        self.state_dir = Path(os.environ.get("STATE_DIR", "."))
        self.agent_name = os.environ.get("AGENT_NAME", "backup-creator")
        
        # Setup logging
        self.setup_logging()
        
        # Backup configuration
        self.backup_dir = self.repo_root.parent / f"notes_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.exclude_patterns = [
            "*.git/*",
            "*venv/*", 
            "*node_modules/*",
            "*__pycache__/*",
            "*.pyc",
            "*cache/*",
            "*.log"
        ]
    
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
                "progress_percent": 0.0
            }
        
        # Update with provided values
        state.update(kwargs)
        state["last_update"] = datetime.now().isoformat()
        
        # Save updated state
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def create_git_backup(self) -> bool:
        """Create git bundle backup of repository"""
        self.logger.info("🔄 Creating git bundle backup...")
        self.update_state(current_task="Creating git bundle", progress_percent=10)
        
        try:
            bundle_path = self.backup_dir / "repository.bundle"
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Create git bundle
            cmd = ["git", "bundle", "create", str(bundle_path), "--all"]
            result = subprocess.run(cmd, cwd=self.repo_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"✅ Git bundle created: {bundle_path}")
                return True
            else:
                self.logger.error(f"❌ Git bundle failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Git bundle error: {e}")
            return False
    
    def create_file_backup(self) -> bool:
        """Create selective file system backup"""
        self.logger.info("🔄 Creating file system backup...")
        self.update_state(current_task="Backing up critical files", progress_percent=30)
        
        try:
            # Critical directories to backup fully
            critical_dirs = [
                "_ledger",
                "_system/claude_config", 
                "_system/agents",
                "code_library",
                "CLAUDE.md",
                "README.md"
            ]
            
            files_copied = 0
            total_size = 0
            
            for item in critical_dirs:
                source = self.repo_root / item
                if source.exists():
                    if source.is_file():
                        target = self.backup_dir / "critical" / item
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source, target)
                        files_copied += 1
                        total_size += source.stat().st_size
                    else:
                        target = self.backup_dir / "critical" / item
                        shutil.copytree(source, target, ignore=shutil.ignore_patterns(*self.exclude_patterns))
                        
                        # Count files in copied directory
                        for file_path in target.rglob("*"):
                            if file_path.is_file():
                                files_copied += 1
                                total_size += file_path.stat().st_size
            
            self.logger.info(f"✅ Backed up {files_copied} critical files ({total_size/1024/1024:.1f} MB)")
            self.update_state(files_processed=files_copied)
            return True
            
        except Exception as e:
            self.logger.error(f"❌ File backup error: {e}")
            return False
    
    def create_manifest(self) -> bool:
        """Create backup manifest with metadata"""
        self.logger.info("🔄 Creating backup manifest...")
        self.update_state(current_task="Creating backup manifest", progress_percent=80)
        
        try:
            manifest = {
                "backup_info": {
                    "created_at": datetime.now().isoformat(),
                    "source_repository": str(self.repo_root),
                    "backup_directory": str(self.backup_dir),
                    "agent_name": self.agent_name
                },
                "git_info": {},
                "file_info": {
                    "files_backed_up": 0,
                    "total_size_bytes": 0,
                    "critical_directories": []
                },
                "exclude_patterns": self.exclude_patterns
            }
            
            # Get git information
            try:
                # Current branch
                result = subprocess.run(["git", "branch", "--show-current"], 
                                      cwd=self.repo_root, capture_output=True, text=True)
                manifest["git_info"]["current_branch"] = result.stdout.strip()
                
                # Latest commit
                result = subprocess.run(["git", "log", "-1", "--format=%H %s"], 
                                      cwd=self.repo_root, capture_output=True, text=True)
                manifest["git_info"]["latest_commit"] = result.stdout.strip()
                
                # Repository status
                result = subprocess.run(["git", "status", "--porcelain"], 
                                      cwd=self.repo_root, capture_output=True, text=True)
                manifest["git_info"]["uncommitted_changes"] = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
                
            except Exception as e:
                self.logger.warning(f"Could not get git info: {e}")
            
            # Count backup files
            if self.backup_dir.exists():
                total_files = 0
                total_size = 0
                for file_path in self.backup_dir.rglob("*"):
                    if file_path.is_file() and file_path.name != "manifest.json":
                        total_files += 1
                        total_size += file_path.stat().st_size
                
                manifest["file_info"]["files_backed_up"] = total_files
                manifest["file_info"]["total_size_bytes"] = total_size
            
            # Save manifest
            manifest_path = self.backup_dir / "manifest.json"
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            self.logger.info(f"✅ Backup manifest created: {manifest_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Manifest creation error: {e}")
            return False
    
    def verify_backup(self) -> bool:
        """Verify backup integrity"""
        self.logger.info("🔄 Verifying backup integrity...")
        self.update_state(current_task="Verifying backup", progress_percent=90)
        
        try:
            # Check if backup directory exists
            if not self.backup_dir.exists():
                self.logger.error("❌ Backup directory not found")
                return False
            
            # Check if git bundle exists and is valid
            bundle_path = self.backup_dir / "repository.bundle"
            if bundle_path.exists():
                # Verify bundle
                result = subprocess.run(["git", "bundle", "verify", str(bundle_path)], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    self.logger.error(f"❌ Git bundle verification failed: {result.stderr}")
                    return False
            
            # Check if manifest exists
            manifest_path = self.backup_dir / "manifest.json"
            if not manifest_path.exists():
                self.logger.error("❌ Backup manifest not found")
                return False
            
            # Verify manifest content
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
                
            required_keys = ["backup_info", "git_info", "file_info"]
            if not all(key in manifest for key in required_keys):
                self.logger.error("❌ Backup manifest is incomplete")
                return False
            
            self.logger.info("✅ Backup verification successful")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Backup verification error: {e}")
            return False
    
    def create_recovery_script(self):
        """Create script for easy backup recovery"""
        recovery_script = f'''#!/bin/bash
# Repository Recovery Script
# Generated: {datetime.now().isoformat()}

set -e

BACKUP_DIR="{self.backup_dir}"
RESTORE_DIR="$1"

if [ -z "$RESTORE_DIR" ]; then
    echo "Usage: $0 <restore_directory>"
    exit 1
fi

echo "🔄 Restoring repository from backup..."
echo "📁 Backup: $BACKUP_DIR" 
echo "📁 Restore to: $RESTORE_DIR"

# Create restore directory
mkdir -p "$RESTORE_DIR"
cd "$RESTORE_DIR"

# Restore from git bundle
if [ -f "$BACKUP_DIR/repository.bundle" ]; then
    echo "🔄 Restoring from git bundle..."
    git clone "$BACKUP_DIR/repository.bundle" .
else
    echo "❌ Git bundle not found"
    exit 1
fi

# Copy critical files
if [ -d "$BACKUP_DIR/critical" ]; then
    echo "🔄 Restoring critical files..."
    cp -r "$BACKUP_DIR/critical/"* .
fi

echo "✅ Repository restored successfully!"
echo "📋 Check manifest.json for backup details"
'''
        
        script_path = self.backup_dir / "restore.sh"
        with open(script_path, 'w') as f:
            f.write(recovery_script)
        
        # Make script executable
        script_path.chmod(0o755)
        
        self.logger.info(f"✅ Recovery script created: {script_path}")
    
    def execute(self) -> Dict[str, Any]:
        """Main agent execution"""
        self.logger.info(f"🚀 Starting {self.agent_name} execution")
        self.update_state(current_task="Initializing backup process", progress_percent=0)
        
        results = {
            "agent_name": self.agent_name,
            "start_time": datetime.now().isoformat(),
            "success": False,
            "backup_path": str(self.backup_dir),
            "operations": {}
        }
        
        try:
            # Step 1: Create git backup
            results["operations"]["git_backup"] = self.create_git_backup()
            
            # Step 2: Create file backup
            results["operations"]["file_backup"] = self.create_file_backup()
            
            # Step 3: Create manifest
            results["operations"]["manifest"] = self.create_manifest()
            
            # Step 4: Verify backup
            results["operations"]["verification"] = self.verify_backup()
            
            # Step 5: Create recovery script
            self.create_recovery_script()
            results["operations"]["recovery_script"] = True
            
            # Final state update
            all_successful = all(results["operations"].values())
            results["success"] = all_successful
            
            if all_successful:
                self.update_state(
                    current_task="Backup completed successfully",
                    progress_percent=100,
                    status="completed"
                )
                self.logger.info(f"✅ {self.agent_name} completed successfully")
                self.logger.info(f"📁 Backup location: {self.backup_dir}")
            else:
                failed_ops = [k for k, v in results["operations"].items() if not v]
                self.logger.error(f"❌ {self.agent_name} failed operations: {failed_ops}")
                self.update_state(
                    current_task=f"Failed operations: {failed_ops}",
                    status="failed"
                )
            
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
    agent = BackupCreatorAgent()
    result = agent.execute()
    
    # Print result summary
    print("\n" + "="*50)
    print("📦 BACKUP CREATOR AGENT RESULTS")
    print("="*50)
    print(f"✅ Success: {result['success']}")
    print(f"📁 Backup Path: {result['backup_path']}")
    
    print("\n📊 Operations:")
    for operation, success in result["operations"].items():
        status = "✅" if success else "❌"
        print(f"{status} {operation}")
    
    if not result['success'] and 'error' in result:
        print(f"\n❌ Error: {result['error']}")
    
    print("="*50)
    
    return 0 if result['success'] else 1


if __name__ == "__main__":
    exit(main())