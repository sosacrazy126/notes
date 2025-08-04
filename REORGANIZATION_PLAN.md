# Documentation Library Reorganization Plan

## Current → New Structure Mapping

### 1. Documentation Resources
**Current locations:**
- `04_documentation/`
- `guides/`
- `greptile-docs/`
- Various `README.md` files

**New location:** `documentation/`
```
documentation/
├── api_references/
│   └── (from greptile-docs/api-reference/)
├── development_guides/
│   └── (from guides/, 04_documentation/development_guides/)
├── quick_references/
│   └── (from 04_documentation/quick_references/)
└── technical_specs/
    └── (from 04_documentation/technical_references/)
```

### 2. Development Tools
**Current locations:**
- `ai_tools/`
- `commands/`
- `patterns/`
- `.claude/agents/`

**New location:** `development_tools/`
```
development_tools/
├── ai_agents/
│   ├── configurations/ (from .claude/agents/)
│   └── frameworks/ (from ai_tools/agent_frameworks/)
├── commands/
│   └── (from commands/tools/, commands/workflows/)
├── patterns/
│   ├── fabric/ (from ai_tools/fabric_patterns/)
│   └── custom/ (from patterns/, CustomClaude/patterns/)
└── workflows/
    └── (from ai_tools/agent_frameworks/development_workflows/)
```

### 3. Research & Learning
**Current locations:**
- `01_active_research/`
- `06_experimental/`
- Various experiment files

**New location:** `research_notes/`
```
research_notes/
├── case_studies/
│   └── (practical examples from experiments)
├── experiments/
│   └── (from 06_experimental/)
├── learning_notes/
│   └── (from guides/, ai_project_management/)
└── best_practices/
    └── (extracted from various docs)
```

### 4. Project Resources
**Current locations:**
- `07_project_management/`
- `_NoteCompanion/`
- `notecompanion_system/`

**New location:** `project_resources/`
```
project_resources/
├── _NoteCompanion/ (preserve as-is)
├── active_projects/
├── templates/
│   └── (from ai_tools/templates/)
└── configurations/
    └── (from various config files)
```

### 5. Code Library
**Current locations:**
- `02_implementations/`
- Code snippets scattered in docs
- `production_grade/`

**New location:** `code_library/`
```
code_library/
├── snippets/
│   └── (extracted from documentation)
├── utilities/
│   └── (from 02_implementations/)
├── integrations/
│   └── (from integration guides)
└── examples/
    └── (from various example files)
```

### 6. Knowledge Base
**Current locations:**
- Scattered across all directories
- `agentic seeds/`
- Various knowledge files

**New location:** `knowledge_base/`
```
knowledge_base/
├── by_technology/
│   ├── ai_ml/
│   ├── web_dev/
│   └── devops/
├── by_domain/
│   └── (organized by subject)
├── troubleshooting/
│   └── (extracted solutions)
└── faqs/
    └── (common questions)
```

### 7. Archive (for consciousness/philosophical content)
**New location:** `_archive/consciousness_research/`
```
_archive/
└── consciousness_research/
    ├── consciousness_vault/ (preserved)
    ├── philosophical_writings/
    └── consciousness_experiments/
```

## Migration Steps

### Phase 1: Prepare New Structure
```bash
# Create new directory structure
mkdir -p documentation/{api_references,development_guides,quick_references,technical_specs}
mkdir -p development_tools/{ai_agents,commands,patterns,workflows}
mkdir -p research_notes/{case_studies,experiments,learning_notes,best_practices}
mkdir -p project_resources/{active_projects,templates,configurations}
mkdir -p code_library/{snippets,utilities,integrations,examples}
mkdir -p knowledge_base/{by_technology,by_domain,troubleshooting,faqs}
mkdir -p ledger
mkdir -p .metadata/{tags,search_index,agent_config}
mkdir -p _archive/consciousness_research
```

### Phase 2: Content Migration
1. **Documentation**: Move guides and references
2. **Tools**: Consolidate AI tools and commands
3. **Code**: Extract and organize code examples
4. **Knowledge**: Categorize by technology/domain
5. **Archive**: Move consciousness-related content

### Phase 3: Create Indexes
```bash
# Generate master index
echo "# Resource Index" > ledger/resource_index.md
echo "Auto-generated: $(date)" >> ledger/resource_index.md

# Create category indexes
for dir in documentation development_tools research_notes; do
  echo "## $dir" >> ledger/resource_index.md
  find $dir -name "*.md" >> ledger/resource_index.md
done
```

### Phase 4: Set Up Search & Navigation
1. Create tag taxonomy
2. Build search index
3. Configure AI agent access patterns
4. Set up quick navigation scripts

## Practical Benefits

1. **Clear Organization**: Everything has a logical place
2. **Easy Discovery**: Multiple ways to find resources
3. **AI-Friendly**: Structured for agent navigation
4. **Version Controlled**: Track all changes
5. **Quality Focused**: Metrics and standards

## Implementation Timeline

- **Week 1**: Create structure, begin migration
- **Week 2**: Complete migration, create indexes
- **Week 3**: Set up search and navigation
- **Week 4**: Documentation and training

## Success Metrics

- All resources categorized and indexed
- Search functionality operational
- AI agents can navigate efficiently
- Usage tracking implemented
- Quality standards enforced