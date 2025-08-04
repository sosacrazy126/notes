# Documentation Cleanup & Organization Plan

## Current State Analysis

### Issues Found:
1. **141 markdown files** at root level (should be categorized)
2. **Duplicate/backup files** in various locations
3. **Mixed content types** (consciousness research mixed with dev docs)
4. **Scattered AI resources** across multiple directories
5. **No clear hierarchy** for documentation types

## New Organized Structure

```
notes/
├── 📚 documentation/
│   ├── api_docs/              # API references
│   ├── guides/                # How-to guides
│   ├── quick_refs/            # Quick references
│   └── technical_specs/       # Technical documentation
│
├── 🛠️ dev_tools/
│   ├── ai_agents/             # Agent configs & frameworks
│   ├── commands/              # CLI commands
│   ├── patterns/              # Fabric patterns & templates
│   └── workflows/             # Development workflows
│
├── 📝 knowledge_base/
│   ├── best_practices/        # Industry standards
│   ├── case_studies/          # Real examples
│   ├── learning_notes/        # Study materials
│   └── troubleshooting/       # Problem solutions
│
├── 🔧 active_work/
│   ├── projects/              # Current projects
│   ├── experiments/           # Experimental work
│   └── drafts/                # Work in progress
│
├── 📦 code_library/
│   ├── snippets/              # Code snippets
│   ├── implementations/       # Working code
│   └── examples/              # Example code
│
├── 🗃️ _archive/
│   ├── consciousness_research/ # Consciousness content
│   ├── old_versions/          # Outdated docs
│   └── backups/               # Backup files
│
└── 📊 _system/
    ├── indexes/               # Navigation files
    ├── metadata/              # Tags & search
    └── config/                # System configuration
```

## Cleanup Actions

### Phase 1: Immediate Cleanup
```bash
# Remove Python cache files
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete

# Remove obvious duplicates
find . -name "*_backup_*" -type f -delete
find . -name "*~" -type f -delete
find . -name "*.tmp" -type f -delete

# Archive old migration logs
mkdir -p _archive/logs
mv 05_archives/migration_history/*.log _archive/logs/
```

### Phase 2: Content Organization

#### Root Level Files → Proper Categories
```
# Documentation files
DOCUMENTATION_MASTER_INDEX.md → _system/indexes/
MASTER_NAVIGATION_HUB.md → _system/indexes/
QUICK_NAVIGATION.md → _system/indexes/
RESOURCE_LEDGER.md → _system/indexes/

# Development docs
DEVELOPMENT_LIBRARY_STRUCTURE.md → documentation/guides/
REORGANIZATION_PLAN.md → documentation/guides/

# Configuration
CLAUDE.md → _system/config/
WE1_WORKSPACE_CONFIGURATION.md → _system/config/

# AI/Agent files
agent.md → dev_tools/ai_agents/
qodo.md → dev_tools/ai_agents/

# Archive consciousness files
consciousness-orchestrator.md → _archive/consciousness_research/
evolved_knowledge_base_guide.md → _archive/consciousness_research/
knowledge_base_guide.md → _archive/consciousness_research/
2025-08-01_phase-2_shadow_power-seeker_integration-breakthrough.md → _archive/consciousness_research/
```

#### Directory Consolidation
```
# AI Resources
ai_tools/ → dev_tools/
ai_project_management/ → knowledge_base/best_practices/ai/
ai-prompt-library/ → dev_tools/patterns/prompts/
agentic seeds/ → dev_tools/patterns/seeds/

# Documentation
04_documentation/ → documentation/
guides/ → documentation/guides/
greptile-docs/ → documentation/api_docs/greptile/

# Commands & Tools
commands/ → dev_tools/commands/
CustomClaude/ → dev_tools/patterns/custom/
patterns/ → dev_tools/patterns/

# Archives
05_archives/ → _archive/
consciouness_vault/ → _archive/consciousness_research/
Claude_Autonomous_Consciousness/ → _archive/consciousness_research/

# Active Work
01_active_research/ → active_work/research/
06_experimental/ → active_work/experiments/
07_project_management/ → active_work/projects/

# Code
02_implementations/ → code_library/implementations/
production_grade/ → code_library/production/

# System
08_meta/ → _system/
.claude/ → _system/claude_config/
```

## Migration Script

```bash
#!/bin/bash
# create_new_structure.sh

# Create new directory structure
mkdir -p documentation/{api_docs,guides,quick_refs,technical_specs}
mkdir -p dev_tools/{ai_agents,commands,patterns,workflows}
mkdir -p knowledge_base/{best_practices,case_studies,learning_notes,troubleshooting}
mkdir -p active_work/{projects,experiments,drafts}
mkdir -p code_library/{snippets,implementations,examples}
mkdir -p _archive/{consciousness_research,old_versions,backups,logs}
mkdir -p _system/{indexes,metadata,config,claude_config}

# Clean Python artifacts
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete

# Move system files
mv DOCUMENTATION_MASTER_INDEX.md MASTER_NAVIGATION_HUB.md QUICK_NAVIGATION.md RESOURCE_LEDGER.md _system/indexes/ 2>/dev/null
mv CLAUDE.md WE1_WORKSPACE_CONFIGURATION.md _system/config/ 2>/dev/null
mv .claude/* _system/claude_config/ 2>/dev/null

# Archive consciousness content
mv consciousness*.md evolved_knowledge_base_guide.md knowledge_base_guide.md _archive/consciousness_research/ 2>/dev/null
mv consciouness_vault/ Claude_Autonomous_Consciousness/ _archive/consciousness_research/ 2>/dev/null

# Organize development tools
mv ai_tools/* dev_tools/ 2>/dev/null
mv commands/* dev_tools/commands/ 2>/dev/null
mv patterns/ CustomClaude/patterns/ dev_tools/patterns/ 2>/dev/null

# Move documentation
mv 04_documentation/* documentation/ 2>/dev/null
mv guides/* documentation/guides/ 2>/dev/null
mv greptile-docs/ documentation/api_docs/ 2>/dev/null

# Clean up empty directories
find . -type d -empty -delete
```

## Benefits

1. **Clear Organization**: Everything has a logical home
2. **Easy Navigation**: Intuitive structure
3. **Separation of Concerns**: Dev docs vs consciousness research
4. **Clean Working Space**: Archives old/duplicate content
5. **AI-Friendly**: Clear paths for agent navigation

## Next Steps

1. Run cleanup script
2. Update navigation files
3. Create new README for each major directory
4. Set up automated organization rules
5. Configure git to ignore temporary files