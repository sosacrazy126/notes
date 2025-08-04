# CLAUDE.md - Development Documentation Library
*A modular documentation system for development resources*

## Repository Overview
This is a comprehensive documentation library and resource ledger for development tools, research notes, and coding patterns. Organized for efficient navigation by both users and AI coding agents.

## Core Documentation Structure

### Navigation & Indexes
@_system/indexes/MASTER_NAVIGATION.md
@_system/indexes/RESOURCE_LEDGER.md
@_system/indexes/QUICK_NAVIGATION.md

### Development Resources
@dev_tools/README.md
@dev_tools/patterns/index.md
@dev_tools/ai_agents/agent_index.md

### Knowledge Base
@knowledge_base/README.md
@knowledge_base/best_practices/index.md
@knowledge_base/troubleshooting/index.md

### Active Projects
@active_work/projects/current_projects.md
@active_work/experiments/active_experiments.md

### Code Library
@code_library/README.md
@code_library/snippets/index.md

## Quick Reference

### Finding Resources
```bash
# Search documentation
grep -r "keyword" documentation/ --include="*.md"

# Browse patterns
ls dev_tools/patterns/*/

# Find code examples
find code_library/ -name "*.py" -o -name "*.js"
```

### For AI Agents
- Start with imported index files above
- Use structured paths for direct access
- Check metadata headers in documents
- Follow naming conventions: `category_subcategory_title.md`

## Available Tools & Patterns

### AI Development (220+ Patterns)
- **Analysis**: `dev_tools/patterns/fabric/analysis/`
- **Creation**: `dev_tools/patterns/fabric/content_creation/`
- **Extraction**: `dev_tools/patterns/fabric/data_extraction/`
- **Improvement**: `dev_tools/patterns/fabric/improvement/`

### Commands & Workflows
- **Dev Tools**: `dev_tools/commands/tools/`
- **Workflows**: `dev_tools/commands/workflows/`
- **Templates**: `dev_tools/patterns/templates/`

### Agent Configurations
- **Specialized Agents**: `_system/claude_config/agents/`
- **Activation Protocols**: `dev_tools/ai_agents/activation_protocols/`
- **Integration Guides**: `dev_tools/ai_agents/integration_guides/`

## Repository Statistics
- **Total Resources**: 574+ documented files
- **AI Patterns**: 220+ Fabric patterns
- **Agent Configs**: 18 specialized agents
- **Commands**: 40+ reusable commands
- **Guides**: 50+ how-to documents

## Working with This Library

### Adding New Resources
1. Choose appropriate category
2. Follow naming convention
3. Add metadata header
4. Update relevant index

### Resource Metadata Template
```yaml
---
title: "Resource Title"
category: "development_tools"
tags: ["api", "rest", "authentication"]
created: "2024-01-15"
status: "stable"  # draft, stable, deprecated
---
```

## Best Practices
- Keep documentation practical and actionable
- Maintain clear categorization
- Update indexes when adding resources
- Use consistent naming conventions
- Include working examples

---
*This modular structure keeps CLAUDE.md lean while providing comprehensive access through imports.*