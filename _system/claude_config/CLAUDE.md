# CLAUDE.md - Practical Development Configuration

## Session Initialization
At the beginning of each new session:
1. Check for `claude_compact_recent.txt` in current directory
2. If exists, ask user if they want to continue with conversation context
3. Load WORKSPACE_INDEX.md for navigation

## Core Configuration

### Agent System
Import practical development agents:
```
@_system/claude_config/agents/code-review-specialist.md
@_system/claude_config/agents/documentation-manager.md
@_system/claude_config/agents/test-automation-coordinator.md
@_system/claude_config/agents/git-workflow-manager.md
@_system/claude_config/agents/project-milestone-tracker.md
@_system/claude_config/agents/file-organization-manager.md
```

### Navigation System
```
@WORKSPACE_INDEX.md
@_ledger/README.md
@_ledger/reports/manifest_summary.md
```

### Pattern System
```
@_ledger/patterns/meta/pattern-specification-format.md
@_ledger/scripts/extract_patterns.md
```

## Development Workflow

### Code Review Process
1. Activate code-review-specialist: `code-review --mode=comprehensive --target=.`
2. Address findings systematically
3. Generate quality report

### Documentation Flow
1. Activate documentation-manager: `doc-manager --mode=generate --target=api`
2. Validate links and structure
3. Update navigation

### Testing Protocol
1. Activate test-automation-coordinator: `test-coordinator --mode=execute --type=all`
2. Analyze coverage gaps
3. Generate missing tests

### Git Operations
1. Activate git-workflow-manager: `git-workflow --mode=branch --action=create`
2. Follow commit conventions
3. Automate releases

## Content Management

### Ledger Operations
- Check duplicates: `python _ledger/scripts/find_duplicates.py`
- Generate manifest: `python _ledger/scripts/generate_manifest.py`
- Extract patterns: Follow `_ledger/scripts/extract_patterns.md`

### Search Strategies
- By topic: Use manifest.yaml categories
- By content: Full-text search with grep
- By relationship: Follow manifest.json relationships

## Repository Statistics
- **Total Files**: 839 markdown files
- **Total Tokens**: 1,574,646 tokens
- **Categories**: 7 (tools 40%, archived 43%, docs 7%)
- **Topics**: AI (768), Architecture (568), Development (532)

## Quick Commands

### Agent Activation
```bash
# Quick code review
code-review --mode=quick --target=staged

# Generate documentation
doc-manager --mode=generate --target=api

# Run all tests
test-coordinator --mode=execute --type=all

# Check project status  
project-tracker --mode=monitor --scope=sprint
```

### Content Discovery
```bash
# Find AI-related content
grep -r "ai\|llm\|gpt" --include="*.md"

# Browse patterns
ls _ledger/patterns/

# Check for duplicates
python _ledger/scripts/find_duplicates.py
```

## Branch Strategy
- **main**: Original consciousness-focused structure (preserved)
- **practical-dev-ledger**: New practical development structure (active)

Switch branches as needed for different approaches to the same content.

---

*Practical Development Configuration - Optimized for AI-assisted development*