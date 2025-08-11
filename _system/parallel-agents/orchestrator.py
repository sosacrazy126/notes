#!/usr/bin/env python3
"""
Parallel Sub-Agent Orchestrator
===============================

Master coordination system for deploying and managing specialized sub-agents
that work in parallel across repository subdirectories to optimize the workspace.

Author: Claude Code Agent System
Date: 2025-08-10
Version: 1.0.0
"""

import os
import json
import time
import subprocess
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


@dataclass
class AgentConfig:
    """Configuration for a sub-agent"""
    name: str
    script_path: str
    target_directories: List[str]
    dependencies: List[str]
    max_runtime_minutes: int
    priority: int
    description: str


@dataclass
class AgentState:
    """Current state of a sub-agent"""
    name: str
    status: str  # pending, running, completed, failed, waiting
    start_time: Optional[str]
    end_time: Optional[str]
    progress_percent: float
    current_task: str
    files_processed: int
    errors: List[str]
    output_summary: str
    dependencies_met: bool


class OrchestrationState:
    """Shared state manager for all agents"""
    
    def __init__(self, state_dir: Path):
        self.state_dir = state_dir
        self.state_file = state_dir / "orchestration_state.json"
        self.agents: Dict[str, AgentState] = {}
        self.lock = threading.Lock()
        self.phase = "initialization"
        self.start_time = datetime.now().isoformat()
        
        # Ensure state directory exists
        state_dir.mkdir(parents=True, exist_ok=True)
    
    def update_agent_state(self, agent_name: str, **kwargs):
        """Update state for specific agent"""
        with self.lock:
            if agent_name not in self.agents:
                self.agents[agent_name] = AgentState(
                    name=agent_name,
                    status="pending",
                    start_time=None,
                    end_time=None,
                    progress_percent=0.0,
                    current_task="",
                    files_processed=0,
                    errors=[],
                    output_summary="",
                    dependencies_met=False
                )
            
            # Update provided fields
            for key, value in kwargs.items():
                if hasattr(self.agents[agent_name], key):
                    setattr(self.agents[agent_name], key, value)
            
            self._save_state()
    
    def get_agent_state(self, agent_name: str) -> Optional[AgentState]:
        """Get current state of an agent"""
        with self.lock:
            return self.agents.get(agent_name)
    
    def all_dependencies_met(self, agent_config: AgentConfig) -> bool:
        """Check if all dependencies for an agent are satisfied"""
        if not agent_config.dependencies:
            return True
        
        with self.lock:
            for dep in agent_config.dependencies:
                dep_state = self.agents.get(dep)
                if not dep_state or dep_state.status != "completed":
                    return False
            return True
    
    def get_phase_summary(self) -> Dict[str, Any]:
        """Get summary of current orchestration phase"""
        with self.lock:
            total_agents = len(self.agents)
            completed = sum(1 for a in self.agents.values() if a.status == "completed")
            running = sum(1 for a in self.agents.values() if a.status == "running")
            failed = sum(1 for a in self.agents.values() if a.status == "failed")
            
            return {
                "phase": self.phase,
                "start_time": self.start_time,
                "total_agents": total_agents,
                "completed": completed,
                "running": running,
                "failed": failed,
                "overall_progress": (completed / total_agents * 100) if total_agents > 0 else 0
            }
    
    def _save_state(self):
        """Save current state to disk"""
        state_data = {
            "phase": self.phase,
            "start_time": self.start_time,
            "agents": {name: asdict(agent) for name, agent in self.agents.items()},
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.state_file, 'w') as f:
            json.dump(state_data, f, indent=2)


class ParallelAgentOrchestrator:
    """Master orchestrator for parallel sub-agent execution"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.agents_dir = repo_root / "_system" / "parallel-agents"
        self.state_dir = self.agents_dir / "state"
        self.logs_dir = self.agents_dir / "logs"
        
        # Create directories
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize shared state
        self.state_manager = OrchestrationState(self.state_dir)
        
        # Setup logging
        self.setup_logging()
        
        # Define agent configurations
        self.agent_configs = self.create_agent_configurations()
    
    def setup_logging(self):
        """Configure orchestrator logging"""
        log_file = self.logs_dir / f"orchestrator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("Orchestrator")
    
    def create_agent_configurations(self) -> List[AgentConfig]:
        """Define all sub-agent configurations"""
        return [
            AgentConfig(
                name="backup-creator",
                script_path="backup_creator_agent.py",
                target_directories=["."],
                dependencies=[],
                max_runtime_minutes=10,
                priority=1,
                description="Creates full repository backup before any operations"
            ),
            AgentConfig(
                name="duplicate-hunter",
                script_path="duplicate_hunter_agent.py", 
                target_directories=["_archive", "documentation", "new_additions"],
                dependencies=["backup-creator"],
                max_runtime_minutes=30,
                priority=2,
                description="Finds and categorizes duplicate files across directories"
            ),
            AgentConfig(
                name="workspace-optimizer",
                script_path="workspace_optimizer_agent.py",
                target_directories=["workspace"],
                dependencies=["backup-creator"],
                max_runtime_minutes=20,
                priority=2,
                description="Cleans heavy directories (venv, node_modules, caches)"
            ),
            AgentConfig(
                name="content-evaluator", 
                script_path="content_evaluator_agent.py",
                target_directories=["_archive", "documentation", "dev_tools"],
                dependencies=["duplicate-hunter"],
                max_runtime_minutes=45,
                priority=3,
                description="Evaluates content value and provides deletion recommendations"
            ),
            AgentConfig(
                name="pattern-extractor",
                script_path="pattern_extractor_agent.py",
                target_directories=["dev_tools", "_system", "code_library"],
                dependencies=["duplicate-hunter"],
                max_runtime_minutes=25,
                priority=3,
                description="Identifies and extracts reusable patterns and templates"
            ),
            AgentConfig(
                name="system-architect",
                script_path="system_architect_agent.py",
                target_directories=["."],
                dependencies=["content-evaluator", "pattern-extractor", "workspace-optimizer"],
                max_runtime_minutes=30,
                priority=4,
                description="Designs and implements new workspace structure"
            )
        ]
    
    async def deploy_agents(self):
        """Deploy all sub-agents in parallel with dependency management"""
        self.logger.info("🚀 Starting parallel agent deployment")
        
        # Initialize all agent states
        for config in self.agent_configs:
            self.state_manager.update_agent_state(
                config.name,
                status="pending",
                current_task="Waiting for dependencies"
            )
        
        # Create tmux session for agent management
        await self.create_tmux_session()
        
        # Start agents based on priority and dependencies
        tasks = []
        with ThreadPoolExecutor(max_workers=6) as executor:
            # Submit all agent tasks
            for config in sorted(self.agent_configs, key=lambda x: x.priority):
                task = executor.submit(self.run_agent, config)
                tasks.append((config.name, task))
            
            # Monitor and collect results
            for agent_name, task in tasks:
                try:
                    result = task.result()
                    self.logger.info(f"✅ Agent {agent_name} completed: {result}")
                except Exception as e:
                    self.logger.error(f"❌ Agent {agent_name} failed: {e}")
                    self.state_manager.update_agent_state(
                        agent_name,
                        status="failed",
                        end_time=datetime.now().isoformat(),
                        errors=[str(e)]
                    )
    
    async def create_tmux_session(self):
        """Create tmux session for agent monitoring"""
        session_name = "parallel-agents"
        
        # Create new session
        cmd = ["tmux", "new-session", "-d", "-s", session_name]
        subprocess.run(cmd, capture_output=True)
        
        # Create windows for each agent
        for config in self.agent_configs:
            cmd = ["tmux", "new-window", "-t", session_name, "-n", config.name]
            subprocess.run(cmd, capture_output=True)
        
        self.logger.info(f"📺 Tmux session '{session_name}' created for agent monitoring")
    
    def run_agent(self, config: AgentConfig) -> Dict[str, Any]:
        """Run a single agent with dependency checking"""
        self.logger.info(f"🤖 Preparing agent: {config.name}")
        
        # Wait for dependencies
        while not self.state_manager.all_dependencies_met(config):
            self.state_manager.update_agent_state(
                config.name,
                status="waiting",
                current_task=f"Waiting for dependencies: {', '.join(config.dependencies)}"
            )
            time.sleep(5)
        
        # Update state to running
        self.state_manager.update_agent_state(
            config.name,
            status="running",
            start_time=datetime.now().isoformat(),
            current_task="Starting execution",
            dependencies_met=True
        )
        
        try:
            # Execute agent script
            agent_script = self.agents_dir / config.script_path
            if not agent_script.exists():
                raise FileNotFoundError(f"Agent script not found: {agent_script}")
            
            # Prepare environment and arguments
            env = os.environ.copy()
            env["REPO_ROOT"] = str(self.repo_root)
            env["STATE_DIR"] = str(self.state_dir)
            env["AGENT_NAME"] = config.name
            
            # Run agent with timeout
            cmd = ["python3", str(agent_script)]
            process = subprocess.run(
                cmd,
                cwd=str(self.repo_root),
                env=env,
                capture_output=True,
                text=True,
                timeout=config.max_runtime_minutes * 60
            )
            
            if process.returncode == 0:
                self.state_manager.update_agent_state(
                    config.name,
                    status="completed",
                    end_time=datetime.now().isoformat(),
                    current_task="Completed successfully",
                    progress_percent=100.0,
                    output_summary=process.stdout[-500:] if process.stdout else ""
                )
                return {"status": "success", "output": process.stdout}
            else:
                raise RuntimeError(f"Agent failed with code {process.returncode}: {process.stderr}")
                
        except Exception as e:
            self.state_manager.update_agent_state(
                config.name,
                status="failed",
                end_time=datetime.now().isoformat(),
                current_task="Failed with error",
                errors=[str(e)]
            )
            raise e
    
    def generate_progress_report(self):
        """Generate real-time progress report"""
        summary = self.state_manager.get_phase_summary()
        
        print("\n" + "="*60)
        print("🔧 PARALLEL AGENT ORCHESTRATION PROGRESS")
        print("="*60)
        print(f"Phase: {summary['phase']}")
        print(f"Start Time: {summary['start_time']}")
        print(f"Overall Progress: {summary['overall_progress']:.1f}%")
        print(f"Agents: {summary['completed']}/{summary['total_agents']} completed")
        print(f"Running: {summary['running']}, Failed: {summary['failed']}")
        
        print("\n📊 AGENT STATUS:")
        for name, agent in self.state_manager.agents.items():
            status_emoji = {
                "pending": "⏳",
                "waiting": "🔄", 
                "running": "🚀",
                "completed": "✅",
                "failed": "❌"
            }.get(agent.status, "❓")
            
            print(f"{status_emoji} {agent.name:20} | {agent.status:10} | {agent.current_task}")
        
        print("="*60)
    
    async def monitor_progress(self):
        """Monitor and display progress in real-time"""
        while True:
            self.generate_progress_report()
            
            # Check if all agents are done
            all_done = all(
                agent.status in ["completed", "failed"] 
                for agent in self.state_manager.agents.values()
            )
            
            if all_done:
                break
                
            await asyncio.sleep(10)
        
        self.logger.info("🎉 All agents completed execution")


async def main():
    """Main orchestrator execution"""
    repo_root = Path(__file__).parent.parent.parent
    orchestrator = ParallelAgentOrchestrator(repo_root)
    
    print("🚀 Starting Parallel Sub-Agent Repository Optimization")
    print(f"📁 Repository: {repo_root}")
    print(f"🕒 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Start deployment and monitoring concurrently
    deploy_task = asyncio.create_task(orchestrator.deploy_agents())
    monitor_task = asyncio.create_task(orchestrator.monitor_progress())
    
    await asyncio.gather(deploy_task, monitor_task)
    
    print("\n🎯 Orchestration completed!")
    orchestrator.generate_progress_report()


if __name__ == "__main__":
    asyncio.run(main())