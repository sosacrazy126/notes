# Agent Activation Guide

## Overview
This guide provides instructions for activating and using the practical development agents in your workflow. These agents are designed to automate common development tasks and improve code quality.

## Available Agents

### 1. Code Review Specialist
**Purpose**: Automated code quality, security, and performance analysis  
**Activation**: `code-review --mode=[quick|comprehensive|security|performance] --target=[file|directory|PR]`

```bash
# Quick review of a single file
code-review --mode=quick --target=src/api/auth.js

# Comprehensive PR review
code-review --mode=comprehensive --target=PR-123

# Security-focused review
code-review --mode=security --target=src/
```

### 2. Documentation Manager
**Purpose**: Automated documentation generation and maintenance  
**Activation**: `doc-manager --mode=[generate|validate|update] --target=[api|guides|all]`

```bash
# Generate API documentation
doc-manager --mode=generate --target=api

# Validate all documentation links
doc-manager --mode=validate --target=all

# Update installation guide
doc-manager --mode=update --target=guides/installation.md
```

### 3. Test Automation Coordinator
**Purpose**: Comprehensive test suite management  
**Activation**: `test-coordinator --mode=[execute|analyze|generate] --type=[unit|integration|e2e|all]`

```bash
# Run all tests
test-coordinator --mode=execute --type=all

# Analyze test coverage
test-coordinator --mode=analyze --type=unit

# Generate missing tests
test-coordinator --mode=generate --type=integration
```

### 4. Git Workflow Manager
**Purpose**: Git operations and workflow automation  
**Activation**: `git-workflow --mode=[branch|commit|merge|release] --action=[create|validate|automate]`

```bash
# Create feature branch
git-workflow --mode=branch --action=create --name=feature/user-auth

# Validate commit messages
git-workflow --mode=commit --action=validate

# Automate release
git-workflow --mode=release --action=automate --version=1.2.0
```

### 5. Project Milestone Tracker
**Purpose**: Project progress tracking and milestone management  
**Activation**: `project-tracker --mode=[monitor|analyze|report] --scope=[sprint|milestone|project]`

```bash
# Monitor current sprint
project-tracker --mode=monitor --scope=sprint

# Analyze milestone progress
project-tracker --mode=analyze --scope=milestone --id=Q1-release

# Generate project report
project-tracker --mode=report --scope=project
```

### 6. File Organization Manager
**Purpose**: Project structure and organization management  
**Activation**: `file-organizer --mode=[analyze|organize|cleanup] --scope=[full|directory|pattern]`

```bash
# Analyze project structure
file-organizer --mode=analyze --scope=full

# Organize specific directory
file-organizer --mode=organize --scope=directory --path=src/components

# Cleanup temporary files
file-organizer --mode=cleanup --scope=pattern --pattern="*.tmp"
```

## Integration Workflows

### PR Review Workflow
```bash
# 1. Create feature branch
git-workflow --mode=branch --action=create --name=feature/new-api

# 2. After implementation, run tests
test-coordinator --mode=execute --type=all

# 3. Review code quality
code-review --mode=comprehensive --target=.

# 4. Generate/update docs
doc-manager --mode=update --target=api

# 5. Create PR
git-workflow --mode=merge --action=create-pr
```

### Release Workflow
```bash
# 1. Check milestone completion
project-tracker --mode=analyze --scope=milestone --id=v2.0

# 2. Run full test suite
test-coordinator --mode=execute --type=all

# 3. Security review
code-review --mode=security --target=.

# 4. Generate changelog and release
git-workflow --mode=release --action=automate --version=2.0.0
```

### Daily Development Workflow
```bash
# Morning: Check project status
project-tracker --mode=monitor --scope=sprint

# Before coding: Ensure clean structure
file-organizer --mode=analyze --scope=directory --path=src/

# After coding: Run relevant tests
test-coordinator --mode=execute --type=unit --path=src/newFeature/

# Before commit: Review changes
code-review --mode=quick --target=staged

# Commit with validation
git-workflow --mode=commit --action=validate
```

## Configuration

### Agent Settings
Agents can be configured via `_system/claude_config/settings.json`:

```json
{
  "agents": {
    "code-review": {
      "default_mode": "quick",
      "auto_fix": true,
      "severity_threshold": "warning"
    },
    "test-automation": {
      "parallel_execution": true,
      "coverage_threshold": 85,
      "fail_on_decrease": true
    },
    "git-workflow": {
      "branch_prefix": "feature/",
      "commit_convention": "conventional",
      "auto_changelog": true
    }
  }
}
```

### CI/CD Integration
Add to your CI/CD pipeline:

```yaml
# .github/workflows/agents.yml
name: Development Agents
on: [push, pull_request]

jobs:
  code-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Code Review
        run: code-review --mode=comprehensive --target=.
      
      - name: Run Tests
        run: test-coordinator --mode=execute --type=all
      
      - name: Check Documentation
        run: doc-manager --mode=validate --target=all
```

### IDE Integration
Most agents support IDE integration through extensions:

- **VS Code**: Install "Development Agents" extension
- **IntelliJ**: Use "Agent Tools" plugin
- **Vim**: Add agent commands to `.vimrc`

## Best Practices

### 1. Regular Usage
- Run `code-review` before every commit
- Execute `test-coordinator` after significant changes
- Use `project-tracker` daily to monitor progress
- Run `file-organizer` weekly to maintain structure

### 2. Automation
- Configure git hooks for automatic agent execution
- Set up CI/CD pipelines with agent integration
- Use scheduled tasks for regular maintenance agents

### 3. Team Collaboration
- Share agent configurations in version control
- Document team-specific agent workflows
- Create custom agent commands for common tasks

## Troubleshooting

### Common Issues

**Agent not found**
```bash
# Ensure agents are in PATH
export PATH=$PATH:/home/evilbastardxd/Desktop/tools/notes/_system/claude_config/agents/bin
```

**Permission denied**
```bash
# Make agents executable
chmod +x /path/to/agent
```

**Configuration not loading**
```bash
# Check settings.json syntax
cat _system/claude_config/settings.json | jq .
```

## Advanced Usage

### Custom Agent Chains
Create custom workflows by chaining agents:

```bash
#!/bin/bash
# custom-pre-commit.sh
code-review --mode=quick --target=staged && \
test-coordinator --mode=execute --type=affected && \
doc-manager --mode=update --target=affected && \
git-workflow --mode=commit --action=create
```

### Agent Aliases
Add to your shell configuration:

```bash
# ~/.bashrc or ~/.zshrc
alias cr='code-review --mode=quick --target=.'
alias test='test-coordinator --mode=execute --type=unit'
alias docs='doc-manager --mode=generate --target=api'
alias track='project-tracker --mode=monitor --scope=sprint'
```

## Support

For issues or feature requests:
- Check agent logs: `~/.agent-logs/`
- Run in debug mode: `AGENT_DEBUG=true <agent-command>`
- Report issues to: `_system/claude_config/agents/issues/`

---

*Last Updated: 2025-08-04*  
*Version: 1.0.0*