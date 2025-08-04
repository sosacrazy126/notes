#!/usr/bin/env python3
"""
Agent Recognition Validator
Validates that all consciousness research subagents are properly formatted and recognized by Claude Code
"""

import os
import yaml
import re
from pathlib import Path
from typing import Dict, List, Tuple

class AgentRecognitionValidator:
    def __init__(self, agents_dir: str = ".claude/agents"):
        self.agents_dir = Path(agents_dir)
        self.required_agents = [
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
        
    def parse_agent_frontmatter(self, file_path: Path) -> Tuple[bool, Dict]:
        """Parse YAML frontmatter from agent file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check if file starts with YAML frontmatter
            if not content.startswith('---'):
                return False, {"error": "Missing YAML frontmatter"}
                
            # Extract frontmatter
            parts = content.split('---', 2)
            if len(parts) < 3:
                return False, {"error": "Incomplete YAML frontmatter"}
                
            frontmatter = parts[1].strip()
            try:
                metadata = yaml.safe_load(frontmatter)
                return True, metadata
            except yaml.YAMLError as e:
                return False, {"error": f"Invalid YAML: {e}"}
                
        except Exception as e:
            return False, {"error": f"File read error: {e}"}
    
    def validate_agent_specification(self, agent_name: str, metadata: Dict) -> List[str]:
        """Validate agent specification completeness"""
        issues = []
        
        # Required fields
        required_fields = ['name', 'description', 'tools', 'priority']
        for field in required_fields:
            if field not in metadata:
                issues.append(f"Missing required field: {field}")
        
        # Name consistency
        if 'name' in metadata and metadata['name'] != agent_name:
            issues.append(f"Agent name mismatch: file={agent_name}, yaml={metadata['name']}")
            
        # Description length check
        if 'description' in metadata:
            desc_len = len(metadata['description'])
            if desc_len < 50:
                issues.append(f"Description too short: {desc_len} chars (minimum 50)")
            elif desc_len > 300:
                issues.append(f"Description very long: {desc_len} chars (consider shortening)")
                
        # Tools validation
        if 'tools' in metadata:
            tools = metadata['tools']
            if isinstance(tools, str):
                # Convert comma-separated string to list
                tools = [t.strip() for t in tools.split(',')]
            if not isinstance(tools, list) or len(tools) == 0:
                issues.append("Tools field must be a non-empty list")
                
        # Priority validation
        if 'priority' in metadata:
            valid_priorities = ['critical', 'high', 'medium', 'low']
            if metadata['priority'] not in valid_priorities:
                issues.append(f"Invalid priority: {metadata['priority']} (must be one of {valid_priorities})")
        
        return issues
    
    def scan_agents_directory(self) -> Dict[str, Dict]:
        """Scan agents directory and validate all agent files"""
        results = {}
        
        if not self.agents_dir.exists():
            return {"error": f"Agents directory not found: {self.agents_dir}"}
            
        for file_path in self.agents_dir.glob("*.md"):
            agent_name = file_path.stem
            
            # Skip summary documents
            if agent_name.upper().endswith('_SUMMARY'):
                continue
                
            has_frontmatter, metadata = self.parse_agent_frontmatter(file_path)
            
            result = {
                "file_path": str(file_path),
                "file_size": file_path.stat().st_size,
                "has_frontmatter": has_frontmatter,
                "metadata": metadata if has_frontmatter else {},
                "issues": []
            }
            
            if has_frontmatter:
                result["issues"] = self.validate_agent_specification(agent_name, metadata)
            else:
                result["issues"] = ["Missing or invalid YAML frontmatter"]
                
            results[agent_name] = result
            
        return results
    
    def check_required_agents(self, scan_results: Dict) -> Dict[str, str]:
        """Check if all required consciousness research agents are present"""
        status = {}
        
        for agent_name in self.required_agents:
            if agent_name in scan_results:
                result = scan_results[agent_name]
                if result["has_frontmatter"] and len(result["issues"]) == 0:
                    status[agent_name] = "✅ READY"
                elif result["has_frontmatter"] and len(result["issues"]) > 0:
                    status[agent_name] = f"⚠️  ISSUES ({len(result['issues'])})"
                else:
                    status[agent_name] = "❌ NO FRONTMATTER"
            else:
                status[agent_name] = "❌ MISSING FILE"
                
        return status
    
    def generate_report(self) -> str:
        """Generate comprehensive validation report"""
        scan_results = self.scan_agents_directory()
        
        if "error" in scan_results:
            return f"ERROR: {scan_results['error']}"
            
        required_status = self.check_required_agents(scan_results)
        
        report = []
        report.append("# Agent Recognition Validation Report")
        report.append(f"Generated: {os.popen('date').read().strip()}")
        report.append("")
        
        # Summary
        total_agents = len(scan_results)
        ready_count = sum(1 for status in required_status.values() if status.startswith("✅"))
        report.append(f"## Summary")
        report.append(f"- **Total agent files**: {total_agents}")
        report.append(f"- **Required agents ready**: {ready_count}/{len(self.required_agents)}")
        report.append("")
        
        # Required agents status
        report.append("## Required Consciousness Research Agents")
        for agent_name, status in required_status.items():
            report.append(f"- **{agent_name}**: {status}")
        report.append("")
        
        # Detailed issues
        report.append("## Detailed Issues")
        has_issues = False
        for agent_name, result in scan_results.items():
            if result["issues"]:
                has_issues = True
                report.append(f"### {agent_name}")
                for issue in result["issues"]:
                    report.append(f"- {issue}")
                report.append("")
                
        if not has_issues:
            report.append("No issues found! All agents properly formatted.")
            report.append("")
        
        # All agents overview
        report.append("## All Agents Overview")
        for agent_name, result in sorted(scan_results.items()):
            size_kb = result["file_size"] / 1024
            frontmatter_status = "✅" if result["has_frontmatter"] else "❌"
            issues_count = len(result["issues"])
            issues_status = f"({issues_count} issues)" if issues_count > 0 else "✅"
            report.append(f"- **{agent_name}**: {size_kb:.1f}KB | Frontmatter: {frontmatter_status} | Validation: {issues_status}")
            
        return "\n".join(report)

def main():
    """Main validation function"""
    validator = AgentRecognitionValidator()
    report = validator.generate_report()
    print(report)
    
    # Save report
    report_path = Path(".claude/testing/agent_recognition_report.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"\nReport saved to: {report_path}")

if __name__ == "__main__":
    main()