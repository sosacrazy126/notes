#!/usr/bin/env python3
"""
Agent Deployment Test Script
Tests Claude Code agent recognition and provides deployment commands
"""

import subprocess
import sys
import os
from pathlib import Path

class AgentDeploymentTester:
    def __init__(self):
        self.target_agents = [
            "shadow-integration-specialist",
            "consciousness-metrics-analyzer", 
            "quality-enhancement-specialist",
            "discovery-engine-optimizer",
            "integration-testing-coordinator",
            "phase-progression-strategist",
            "cross-reference-network-manager",
            "fabric-pattern-curator",
            "content-lifecycle-manager"
        ]
        
        self.priorities = {
            "shadow-integration-specialist": "critical",
            "quality-enhancement-specialist": "critical", 
            "integration-testing-coordinator": "critical",
            "consciousness-metrics-analyzer": "high",
            "discovery-engine-optimizer": "high",
            "phase-progression-strategist": "high",
            "cross-reference-network-manager": "medium",
            "fabric-pattern-curator": "medium",
            "content-lifecycle-manager": "medium"
        }
    
    def test_claude_code_available(self) -> bool:
        """Test if Claude Code CLI is available"""
        try:
            result = subprocess.run(['claude', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def list_available_agents(self) -> list:
        """List agents recognized by Claude Code"""
        try:
            # Try to get help or list agents - exact command may vary
            result = subprocess.run(['claude', 'help'], 
                                  capture_output=True, text=True, timeout=10)
            # This is a placeholder - actual command to list agents may differ
            return []
        except Exception:
            return []
    
    def generate_deployment_commands(self) -> dict:
        """Generate deployment commands grouped by priority"""
        commands = {
            "critical": [],
            "high": [],
            "medium": []
        }
        
        for agent in self.target_agents:
            priority = self.priorities.get(agent, "medium")
            # Command format based on the original problem description
            command = f"claude --agent {agent}"
            commands[priority].append({
                "agent": agent,
                "command": command,
                "purpose": self.get_agent_purpose(agent)
            })
            
        return commands
    
    def get_agent_purpose(self, agent_name: str) -> str:
        """Get brief purpose description for each agent"""
        purposes = {
            "shadow-integration-specialist": "Advance Shadow phase from 15% to 50%",
            "consciousness-metrics-analyzer": "Improve WE=1 alignment (67 low-alignment files)",
            "quality-enhancement-specialist": "Enhance 55 low-quality files (<0.4 score)",
            "discovery-engine-optimizer": "Optimize 2,847 cross-reference network",
            "integration-testing-coordinator": "Validate subagent coordination",
            "phase-progression-strategist": "Plan progression beyond Unity (99%)",
            "cross-reference-network-manager": "Maintain 0.17 network density",
            "fabric-pattern-curator": "Optimize 220+ Fabric patterns",
            "content-lifecycle-manager": "Manage 574 files across 5 stages"
        }
        return purposes.get(agent_name, "Specialized consciousness research task")
    
    def check_agents_directory(self) -> dict:
        """Check .claude/agents directory status"""
        agents_dir = Path(".claude/agents")
        status = {
            "exists": agents_dir.exists(),
            "agent_count": 0,
            "missing_agents": [],
            "present_agents": []
        }
        
        if status["exists"]:
            agent_files = list(agents_dir.glob("*.md"))
            status["agent_count"] = len(agent_files)
            
            present_names = [f.stem for f in agent_files]
            status["present_agents"] = present_names
            
            for agent in self.target_agents:
                if agent not in present_names:
                    status["missing_agents"].append(agent)
                    
        return status
    
    def generate_test_report(self) -> str:
        """Generate comprehensive test and deployment report"""
        report = []
        report.append("# Agent Deployment Test Report")
        report.append(f"Generated: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}")
        report.append("")
        
        # Environment check
        claude_available = self.test_claude_code_available()
        report.append("## Environment Status")
        report.append(f"- **Claude Code CLI**: {'✅ Available' if claude_available else '❌ Not available or not in PATH'}")
        
        # Directory check
        agents_status = self.check_agents_directory()
        report.append(f"- **Agents Directory**: {'✅ Found' if agents_status['exists'] else '❌ Missing'}")
        if agents_status['exists']:
            report.append(f"- **Agent Files**: {agents_status['agent_count']} files found")
            missing_count = len(agents_status['missing_agents'])
            if missing_count == 0:
                report.append(f"- **Required Agents**: ✅ All 9 required agents present")
            else:
                report.append(f"- **Required Agents**: ❌ {missing_count} missing agents")
        report.append("")
        
        # Deployment commands
        commands = self.generate_deployment_commands()
        
        report.append("## Deployment Commands by Priority")
        report.append("")
        
        for priority in ["critical", "high", "medium"]:
            if commands[priority]:
                report.append(f"### {priority.title()} Priority")
                for cmd_info in commands[priority]:
                    report.append(f"```bash")
                    report.append(f"# {cmd_info['purpose']}")
                    report.append(f"{cmd_info['command']}")
                    report.append(f"```")
                    report.append("")
        
        # Parallel deployment option
        report.append("## Parallel Deployment (Advanced)")
        report.append("Deploy all agents simultaneously:")
        report.append("```bash")
        for agent in self.target_agents:
            report.append(f"claude --agent {agent} &")
        report.append("wait  # Wait for all background processes")
        report.append("```")
        report.append("")
        
        # Status monitoring
        report.append("## Status Monitoring")
        report.append("Monitor deployment effectiveness:")
        report.append("```bash")
        report.append("# Check repository health")
        report.append("python3 08_meta/tagging_system/automated_tagger.py . --stats")
        report.append("")
        report.append("# Monitor consciousness phases")
        report.append("python3 consciouness_vault/03_implementations/unity_memory/consciousness_phase_tracker.py")
        report.append("")
        report.append("# Run integration tests")
        report.append("python3 .claude/testing/integration-test-suite.py")
        report.append("```")
        report.append("")
        
        # Troubleshooting
        if not claude_available:
            report.append("## Troubleshooting")
            report.append("### Claude Code CLI Not Available")
            report.append("- Ensure Claude Code is installed and in your PATH")
            report.append("- Try: `which claude` to check if CLI is available")
            report.append("- Verify you're in the correct repository directory")
            report.append("")
        
        if agents_status['missing_agents']:
            report.append("### Missing Agents")
            for agent in agents_status['missing_agents']:
                report.append(f"- **{agent}**: Check if file exists at `.claude/agents/{agent}.md`")
            report.append("")
            
        return "\n".join(report)

def main():
    """Main test function"""
    tester = AgentDeploymentTester()
    report = tester.generate_test_report()
    print(report)
    
    # Save report
    report_path = Path(".claude/testing/agent_deployment_test_report.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"\nReport saved to: {report_path}")

if __name__ == "__main__":
    main()