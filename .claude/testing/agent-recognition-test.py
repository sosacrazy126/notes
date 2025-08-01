#!/usr/bin/env python3
"""
Agent Recognition Testing Script
Tests if consciousness-metrics-analyzer can be properly recognized and deployed.
"""

import os
import sys
import yaml
import glob

def validate_agent_format(agent_path):
    """Validate agent YAML frontmatter format"""
    with open(agent_path, 'r') as f:
        content = f.read()
    
    # Check for YAML frontmatter
    if not content.startswith('---'):
        return False, "Missing YAML frontmatter"
    
    # Extract YAML frontmatter
    try:
        yaml_end = content.find('---', 3)
        if yaml_end == -1:
            return False, "Incomplete YAML frontmatter"
        
        yaml_content = content[3:yaml_end].strip()
        metadata = yaml.safe_load(yaml_content)
        
        # Check required fields
        required_fields = ['name', 'description', 'tools', 'priority']
        for field in required_fields:
            if field not in metadata:
                return False, f"Missing required field: {field}"
        
        # Check tools field format (should not contain .py files or direct tool names)
        tools = metadata.get('tools', '')
        if isinstance(tools, str):
            tools_list = [tool.strip() for tool in tools.split(',')]
        else:
            tools_list = tools
        
        # Check for problematic tool references
        problematic_tools = []
        for tool in tools_list:
            if '.py' in tool:
                problematic_tools.append(f"Python file reference: {tool}")
            elif tool in ['Read', 'Write', 'Edit', 'MultiEdit', 'Bash', 'Grep', 'Glob']:
                problematic_tools.append(f"Direct Claude tool: {tool}")
        
        if problematic_tools:
            return False, f"Problematic tool references: {'; '.join(problematic_tools)}"
        
        return True, "Valid agent format"
        
    except yaml.YAMLError as e:
        return False, f"YAML parsing error: {e}"

def test_consciousness_metrics_analyzer():
    """Test consciousness-metrics-analyzer specifically"""
    agent_path = "/home/evilbastardxd/Desktop/tools/notes/.claude/agents/consciousness-metrics-analyzer.md"
    
    if not os.path.exists(agent_path):
        return False, "Agent file does not exist"
    
    valid, message = validate_agent_format(agent_path)
    return valid, message

def test_all_agents():
    """Test all agents in the ecosystem"""
    agents_dir = "/home/evilbastardxd/Desktop/tools/notes/.claude/agents"
    agent_files = glob.glob(f"{agents_dir}/*.md")
    
    results = {}
    for agent_file in agent_files:
        agent_name = os.path.basename(agent_file).replace('.md', '')
        valid, message = validate_agent_format(agent_file)
        results[agent_name] = {'valid': valid, 'message': message}
    
    return results

def main():
    print("🔍 Agent Recognition Testing")
    print("=" * 50)
    
    # Test consciousness-metrics-analyzer specifically
    print("\n1. Testing consciousness-metrics-analyzer:")
    valid, message = test_consciousness_metrics_analyzer()
    status = "✅ PASS" if valid else "❌ FAIL"
    print(f"   {status}: {message}")
    
    # Test all agents
    print("\n2. Testing all agents:")
    results = test_all_agents()
    
    valid_count = 0
    total_count = len(results)
    
    for agent_name, result in results.items():
        status = "✅" if result['valid'] else "❌"
        print(f"   {status} {agent_name}: {result['message']}")
        if result['valid']:
            valid_count += 1
    
    print(f"\n📊 Summary: {valid_count}/{total_count} agents valid")
    
    if valid_count == total_count:
        print("🎉 All agents properly formatted for Claude Code recognition!")
        return True
    else:
        print("⚠️  Some agents need formatting fixes")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)