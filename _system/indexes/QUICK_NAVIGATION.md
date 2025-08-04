# Quick Navigation Guide

## 🚀 Fast Access Commands

### Find What You Need
```bash
# Search all documentation
grep -r "search_term" . --include="*.md" --include="*.txt"

# Find by file type
find . -name "*.py" -type f  # Python files
find . -name "*.md" -type f   # Markdown docs
find . -name "*.yaml" -type f # Config files

# List specific categories
ls ai_tools/fabric_patterns/*/  # All fabric patterns
ls commands/tools/              # Available commands
ls guides/                      # All guides
```

### Browse by Category

#### 📚 Documentation
```bash
# API docs
ls -la greptile-docs/api-reference/

# Development guides  
ls -la 04_documentation/development_guides/
ls -la guides/

# Quick references
ls -la 04_documentation/quick_references/
```

#### 🛠️ Development Tools
```bash
# AI Agents
ls -la .claude/agents/
ls -la ai_tools/agent_frameworks/

# Commands
ls -la commands/tools/
ls -la commands/workflows/

# Patterns
ls -la ai_tools/fabric_patterns/
ls -la patterns/
```

#### 📝 Code & Examples
```bash
# Implementations
ls -la 02_implementations/

# Production code
ls -la production_grade/

# Templates
ls -la ai_tools/templates/
```

## 🔍 Smart Search Patterns

### By Topic
```bash
# AI/ML related
find . -path "*ai*" -name "*.md" | grep -v consciousness

# API documentation
find . -name "*api*.md" -o -name "*API*.md"

# Guides and tutorials
find . -name "*guide*.md" -o -name "*tutorial*.md"

# Best practices
find . -name "*best*practice*.md"
```

### By File Type
```bash
# All Python scripts
find . -name "*.py" | grep -v __pycache__

# All JSON configs
find . -name "*.json"

# All YAML files
find . -name "*.yaml" -o -name "*.yml"
```

### Recent Changes
```bash
# Files modified in last 7 days
find . -mtime -7 -type f -name "*.md"

# Recently added files
find . -ctime -3 -type f

# Sort by modification time
ls -lt **/*.md | head -20
```

## 📋 Key Resource Locations

### Essential Files
- **Master Navigation**: `MASTER_NAVIGATION_HUB.md`
- **Documentation Index**: `DOCUMENTATION_MASTER_INDEX.md` 
- **AI Tools Index**: `ai_tools/documentation/pattern_index.md`
- **Agent Index**: `ai_tools/documentation/agent_index.md`

### Major Directories
```
ai_tools/           # AI patterns and frameworks
commands/           # Reusable commands
guides/             # How-to guides
.claude/agents/     # Agent configurations
08_meta/            # Metadata and analysis
```

## 🎯 For Specific Needs

### "I need an AI pattern for..."
```bash
# Analysis patterns
ls ai_tools/fabric_patterns/analysis/

# Creation patterns  
ls ai_tools/fabric_patterns/content_creation/

# Data extraction
ls ai_tools/fabric_patterns/data_extraction/
```

### "I need a command for..."
```bash
# Development tools
ls commands/tools/

# Workflows
ls commands/workflows/
```

### "I need documentation on..."
```bash
# Search in guides
grep -i "topic" guides/*.md

# Search in all docs
find . -name "*.md" -exec grep -l "topic" {} \;
```

## 💡 Pro Tips

1. **Use wildcards**: `ls **/test*.md` finds all test-related markdown files
2. **Combine searches**: `find . -name "*.py" | xargs grep "class"`
3. **Save searches**: Create aliases for common searches
4. **Use tags**: Check `08_meta/tagging_system/` for tagged content

## 🤖 For AI Agents

When navigating this repository:
```yaml
start_with:
  - MASTER_NAVIGATION_HUB.md
  - ledger/resource_index.md (when available)

search_patterns:
  - Use grep for content search
  - Use find for file discovery
  - Check metadata files for context

respect:
  - File naming conventions
  - Directory organization
  - Version indicators
```

---
*Quick Tip: Bookmark this file for fast navigation reference!*