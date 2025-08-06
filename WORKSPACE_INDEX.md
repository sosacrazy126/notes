# Workspace Index

**Last Updated**: 2025-08-04  
**Type**: Development Resource Library  
**Purpose**: Centralized navigation for all development resources, tools, and documentation

## 📁 Directory Structure

### 🛠️ Development Tools (`dev_tools/`)
- **AI Prompts Library**: Curated collection of production AI prompts
- **Fabric Patterns**: Reusable code patterns and templates
- **External Research**: Third-party tools and frameworks
- **Commands**: Development automation scripts

### 📝 Documentation (`documentation/`)
- **Guides**: How-to guides and tutorials
- **API References**: API documentation
- **Architecture**: System design documents

### 💻 Active Work (`active_work/`)
- **Projects**: Current development projects
- **Experiments**: Proof of concepts and experiments
- **Snippets**: Quick code references

### 📦 Code Library (`code_library/`)
- **Components**: Reusable code components
- **Templates**: Project templates
- **Production**: Production-ready code

### 🗃️ Archive (`_archive/`)
- **Historical Projects**: Completed/deprecated projects
- **Legacy Documentation**: Outdated references
- **Research Archive**: Past research and experiments

### 📊 System (`_system/`)
- **Configuration**: Claude and system configs
- **Agents**: Development automation agents
- **Indexes**: Navigation and search indexes

### 📈 Ledger (`_ledger/`)
- **Content Manifest**: Master file index with deduplication
- **Token Budget**: Usage tracking and limits
- **Reports**: Duplicate detection and analytics

## 🚀 Quick Access

### Common Tasks
- [Agent Activation Guide](_system/claude_config/agents/AGENT_ACTIVATION_GUIDE.md)
- [Development Library Structure](documentation/guides/DEVELOPMENT_LIBRARY_STRUCTURE.md)
- [Ledger System Documentation](_ledger/README.md)

### Development Agents
1. **Code Review**: `code-review --mode=quick --target=.`
2. **Documentation**: `doc-manager --mode=generate --target=api`
3. **Testing**: `test-coordinator --mode=execute --type=all`
4. **Git Workflow**: `git-workflow --mode=branch --action=create`
5. **Project Tracking**: `project-tracker --mode=monitor --scope=sprint`
6. **File Organization**: `file-organizer --mode=analyze --scope=full`

### AI Prompt Collections
- Production Prompts: `dev_tools/external_research/system-prompts-collection/`
- Fabric Patterns: `dev_tools/fabric_patterns/`

## 🚀 Enhanced @ Functionality

### Architecture & Specifications
- **Architecture Document**: [Enhanced @ Functionality Architecture](dev_tools/documentation/enhanced_at_functionality_architecture.md)
- **Technical Specifications**: [Enhanced @ Functionality Specs](dev_tools/patterns/enhanced_at_functionality_specs.md)
- **Pattern Registry**: [Enhanced @ Pattern Registry](_ledger/patterns/enhanced_at_pattern_registry.md)
- **Configuration Management**: [Enhanced @ Configuration](_system/claude_config/enhanced_at_configuration.md)

### System Status
- **Activation Date**: 2025-08-04
- **Pattern Detection**: 127 patterns detected across 7 categories
- **Enhancement Coverage**: 70% automatic, 24% suggested, 6% manual
- **MCP Integration**: Active via `[byterover-mcp]` in `AGENT.md`

### Key Features
- **Automatic Pattern Detection**: 40% decorator density threshold activation
- **MCP Tool Integration**: `@mcp_tool()`, `@server.agent()`, `@recursive_agent()`
- **API Enhancement**: FastAPI, validation, middleware patterns
- **Testing Framework**: pytest, hypothesis, locust integration
- **Performance Optimization**: Caching, monitoring, error handling

### Usage
```bash
# Check system status
grep -r "@mcp_tool\|@server\.agent" dev_tools/

# View pattern registry
cat _ledger/patterns/enhanced_at_pattern_registry.md

# Validate configuration
python _system/scripts/validate_enhanced_at_config.py
```

## 📈 Repository Statistics
- **Total Size**: 359MB
- **Markdown Files**: 904
- **Duplicate Sets Found**: 75
- **Active Development Files**: ~500
- **Archived Content**: 62MB

## 🔍 Search Strategies

### By Topic
```bash
# Find AI-related content
grep -r "ai\|artificial intelligence" --include="*.md"

# Find testing resources
find . -name "*test*" -type f
```

### By Date
```bash
# Recently modified files
find . -mtime -7 -name "*.md"

# Files older than 6 months
find . -mtime +180 -name "*.md"
```

### Using Ledger
```bash
# Check for duplicates
python _ledger/scripts/find_duplicates.py

# Generate manifest (coming soon)
python _ledger/scripts/generate_manifest.py
```

## 🏷️ Content Categories

### By Purpose
- **Development Tools**: Practical coding resources
- **AI/ML Resources**: Prompts, models, workflows
- **Testing & QA**: Test frameworks and strategies
- **Documentation**: Guides and references
- **Architecture**: Design patterns and principles

### By Technology
- **Languages**: Python, JavaScript, TypeScript, Go
- **Frameworks**: React, FastAPI, Next.js
- **Tools**: Git, Docker, CI/CD
- **AI Platforms**: Claude, GPT, Local LLMs

## 📝 Contributing

1. **Adding Content**: Place in appropriate directory
2. **Avoid Duplicates**: Check ledger before adding
3. **Use Clear Names**: Follow naming conventions
4. **Update Index**: Keep this file current

## 🔗 External Links

- [Project Repository](.)
- [Issue Tracker](_system/claude_config/agents/issues/)
- [Change Log](CHANGELOG.md)

---

*This index replaces: MASTER_NAVIGATION_HUB.md, QUICK_NAVIGATION.md, DOCUMENTATION_MASTER_INDEX.md, and WE1_WORKSPACE_CONFIGURATION.md*