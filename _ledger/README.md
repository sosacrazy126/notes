# Ledger System

## Overview
This ledger system provides a scalable solution for managing a knowledge base that can grow to billions of tokens. It tracks all content across active directories, archives, and git history to prevent duplication and enable efficient navigation.

## Components

### 1. **manifest.yaml**
Master content index tracking all files with:
- File paths and locations (active/archived/git)
- Content hashes for deduplication
- Token counts for budget management
- Topic tags and categories
- Relationships between files

### 2. **topic_index.md**
Hierarchical topic browser organizing content by:
- Development tools and frameworks
- Programming languages
- AI/ML resources
- Best practices and patterns
- Architecture and design

### 3. **token_budget.yaml**
Token counting and management:
- Current usage statistics
- Per-category breakdowns
- Archival thresholds
- Compression policies

### 4. **deduplication_map.json**
Hash-based duplicate tracking:
- SHA-256 content hashes
- File location mappings
- Duplicate detection reports

## Usage

### Query Content
```bash
# Find all files about AI tools
ledger query --topic="ai-tools"

# Check token usage
ledger stats --category="active"

# Find duplicates
ledger dedup --check
```

### Add New Content
```bash
# Register new file in ledger
ledger add path/to/file.md --topics="ai,development"

# Bulk import directory
ledger import path/to/directory/
```

### Archive Management
```bash
# Archive old content
ledger archive --older-than="6 months"

# Compress rarely accessed files
ledger compress --access-count="<5"
```

## Architecture

```
_ledger/
├── manifest.yaml          # Master content index
├── topic_index.md         # Topic hierarchy
├── token_budget.yaml      # Token tracking
├── deduplication_map.json # Duplicate detection
├── scripts/              # Utility scripts
│   ├── generate_manifest.py
│   ├── count_tokens.py
│   └── find_duplicates.py
└── reports/              # Generated reports
    ├── weekly_summary.md
    └── duplicate_report.md
```

## Benefits

1. **Scalability**: Handles billions of tokens through efficient indexing
2. **No Duplicates**: Prevents content duplication across directories
3. **Fast Search**: Multiple access paths (topic, hash, relationship)
4. **Token Management**: Track and budget token usage
5. **Git Integration**: Preserves full history while keeping workspace clean

## Getting Started

1. Run initial scan: `python scripts/generate_manifest.py`
2. Review duplicate report: `cat reports/duplicate_report.md`
3. Set up token budget: `edit token_budget.yaml`
4. Start using ledger commands for content management

---

*Ledger System v1.0 - Managing knowledge at scale*