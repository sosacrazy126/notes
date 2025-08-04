# Master Navigation Hub
*Central index for all documentation resources*

## 📁 Directory Structure

```
notes/
├── 📚 documentation/       # Technical docs and guides
├── 🛠️ dev_tools/          # Development resources
├── 📝 knowledge_base/      # Research and learning
├── 🔧 active_work/         # Current projects
├── 📦 code_library/        # Reusable code
├── 🗃️ _archive/           # Historical content
└── 📊 _system/            # System configuration
```

## 🚀 Quick Access by Purpose

### Documentation & Learning
- [API Documentation](../../documentation/api_docs/)
- [Development Guides](../../documentation/guides/)
- [Quick References](../../documentation/quick_refs/)
- [Best Practices](../../knowledge_base/best_practices/)

### Development Tools
- [AI Patterns](../../dev_tools/patterns/)
- [Commands](../../dev_tools/commands/)
- [Agent Configs](../../dev_tools/ai_agents/)
- [Workflows](../../dev_tools/workflows/)

### Code Resources
- [Code Snippets](../../code_library/snippets/)
- [Implementations](../../code_library/implementations/)
- [Examples](../../code_library/examples/)

### Project Management
- [Active Projects](../../active_work/projects/)
- [Experiments](../../active_work/experiments/)
- [Templates](../../dev_tools/patterns/templates/)

## 🔍 Search Strategies

### By Technology
```bash
# Python resources
find . -path "*python*" -name "*.md"

# JavaScript/Web
find . -path "*js*" -o -path "*web*" -name "*.md"

# AI/ML content
find . -path "*ai*" -o -path "*ml*" -name "*.md"
```

### By Document Type
```bash
# Guides
find documentation/guides -name "*.md"

# API docs
find documentation/api_docs -name "*.md"

# Patterns
find dev_tools/patterns -name "*.md"
```

### By Status
```bash
# Find stable resources
grep -r "status: stable" . --include="*.md"

# Find drafts
grep -r "status: draft" . --include="*.md"
```

## 📊 Resource Statistics

| Category | Count | Location |
|----------|-------|----------|
| Documentation | 150+ | `documentation/` |
| AI Patterns | 220+ | `dev_tools/patterns/` |
| Commands | 40+ | `dev_tools/commands/` |
| Guides | 50+ | `documentation/guides/` |
| Code Examples | 100+ | `code_library/` |

## 🎯 Navigation Tips

1. **Start Here**: This is your central hub
2. **Use Indexes**: Each major directory has its own index
3. **Follow Naming**: `category_subcategory_title.md`
4. **Check Metadata**: Headers contain tags and status
5. **Use Search**: Grep and find are your friends

---
*Last Updated: 2024-01-15*