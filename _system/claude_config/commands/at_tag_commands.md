---
title: @ Tag Search Commands
version: 1.0
date: 2025-08-04
type: command_interface
category: search_tools
tags: [at-tags, search, commands, navigation]
---

# @ Tag Search Commands

## Quick Reference

### Basic Search Commands
```bash
# Find specific @ patterns
at-search @mcp_tool                    # Find MCP tool definitions
at-search @validator @api              # Find validation + API patterns  
at-search @automation                  # Find automation workflows

# Category searches  
at-find --category=mcp_integration     # All MCP patterns
at-find --category=testing             # All testing patterns
at-find --category=documentation       # All doc tags

# Cross-reference searches
at-related notes/dev_tools/file.md     # Find related files
at-suggest @router                     # Suggest related patterns
```

### Advanced Search Commands
```bash
# Multi-pattern searches
at-search @mcp_tool @validation --intersection    # Files with BOTH tags
at-search @api @testing --union                   # Files with EITHER tag

# Context searches
at-context @server.agent 5             # Show 5 lines context around matches
at-examples @lru_cache                 # Show just the code examples

# File-based searches
at-in-file notes/workspace/agent.md    # Show all @ tags in specific file
at-missing --category=api              # Files missing API documentation tags
```

## Command Categories

### 1. Pattern Discovery
```bash
# Discover new patterns
at-scan --new-only                     # Scan for new @ patterns since last index
at-patterns --suggest                  # AI-suggested @ tag additions
at-validate --check-consistency        # Validate @ tag consistency

# Pattern analysis
at-analyze --frequency                 # Most/least common @ patterns
at-analyze --coverage                  # @ tag coverage by directory
at-analyze --relationships             # @ pattern co-occurrence analysis
```

### 2. Navigation & Cross-Reference
```bash
# Navigate using @ tags
at-nav @mcp_tool                      # Navigate to MCP tool examples
at-jump @architecture                 # Jump to architecture docs
at-tree @validation                   # Show validation pattern hierarchy

# Cross-reference mapping
at-map --visual                       # Generate visual @ tag relationship map  
at-connections notes/file.md          # Show connection network for file
at-pathway @api @testing              # Find pathway between different @ patterns
```

### 3. Integration & Automation
```bash
# Integration with existing tools
doc-manager --at-tags --target=api    # Generate docs based on @ tags
pattern-extract --at-filter=@mcp      # Extract patterns matching @ tags
workspace-nav --at-guide=@automation  # Navigate workspace using @ tags

# Automation commands
at-watch --auto-tag                   # Auto-tag new files
at-update --incremental               # Update @ tag index incrementally
at-report --daily                     # Generate daily @ tag report
```

### 4. Quality & Maintenance
```bash
# Quality assurance
at-lint --missing-tags                # Find files that should have @ tags
at-lint --orphaned-tags              # Find @ tags without examples
at-lint --broken-patterns            # Find malformed @ patterns

# Maintenance
at-clean --duplicates                # Remove duplicate @ tag entries
at-merge --similar                   # Merge similar @ tag patterns
at-archive --unused                  # Archive unused @ patterns
```

## Detailed Command Specifications

### at-search
**Purpose**: Primary @ tag search interface
**Syntax**: `at-search <@tag1> [<@tag2>] [options]`

**Options**:
- `--intersection`: Files containing ALL specified tags
- `--union`: Files containing ANY specified tag (default)
- `--category=<cat>`: Limit search to specific category
- `--confidence=<0.0-1.0>`: Minimum confidence threshold
- `--format=<json|markdown|table>`: Output format
- `--limit=<n>`: Maximum results to return

**Examples**:
```bash
# Basic usage
at-search @mcp_tool                           # Find all MCP tool patterns
at-search @api @validation --intersection     # Find files with both API and validation tags
at-search @automation --confidence=0.9        # High-confidence automation patterns only

# Advanced usage  
at-search @testing --category=performance --format=json --limit=10
```

### at-find
**Purpose**: Category-based and filtered search
**Syntax**: `at-find [options]`

**Options**:
- `--category=<category>`: Search within specific category
- `--recent=<days>`: Only files modified in last N days
- `--popular`: Sort by usage frequency
- `--new`: Only show newly discovered patterns
- `--missing`: Files that should have tags but don't

**Examples**:
```bash
at-find --category=mcp_integration            # All MCP patterns
at-find --recent=7 --popular                 # Popular patterns from last week
at-find --missing --category=documentation   # Docs missing @ tags
```

### at-related
**Purpose**: Find related files using @ tag similarity
**Syntax**: `at-related <file_path> [options]`

**Options**:
- `--similarity=<0.0-1.0>`: Minimum similarity threshold (default: 0.3)
- `--max-results=<n>`: Maximum related files to show (default: 10)
- `--exclude-category=<cat>`: Exclude specific categories
- `--format=<format>`: Output format

**Examples**:
```bash
at-related notes/workspace/agent-zero/README.md              # Find similar files
at-related notes/dev_tools/patterns/api.md --similarity=0.8  # High similarity only
```

### at-context
**Purpose**: Show @ tag matches with surrounding context
**Syntax**: `at-context <@tag> [context_lines]`

**Options**:
- `context_lines`: Number of lines before/after match (default: 3)
- `--highlight`: Highlight the @ tag in context
- `--line-numbers`: Show line numbers
- `--file-headers`: Show file path headers

**Examples**:
```bash
at-context @server.agent 5                   # Show 5 lines context
at-context @validation --highlight --line-numbers
```

## Integration with Existing Commands

### Enhanced doc-manager Commands
```bash
# @ tag-aware documentation management
doc-manager --mode=analyze --at-tags          # Analyze @ tag coverage
doc-manager --mode=generate --at-filter=@api # Generate docs for API patterns only
doc-manager --mode=validate --at-consistency # Validate @ tag consistency
```

### Enhanced pattern-extract Commands
```bash
# @ tag-guided pattern extraction
pattern-extract --at-source=@mcp_tool        # Extract from MCP tool patterns
pattern-extract --at-target=@automation      # Generate automation patterns
pattern-extract --at-cross-ref              # Generate cross-reference patterns
```

### Enhanced workspace-nav Commands
```bash
# @ tag-guided workspace navigation
workspace-nav --at-guide=@architecture       # Navigate using architecture tags
workspace-nav --at-suggest                  # AI-suggested navigation based on @ tags
workspace-nav --at-map                      # Visual map of @ tag relationships
```

## Configuration

### Default Settings
```yaml
# ~/.at-search-config.yaml
at_search:
  default_confidence: 0.75
  max_results: 50
  default_format: "markdown"
  auto_update_index: true
  case_sensitive: false
  
categories:
  mcp_integration: 
    priority: "high"
    auto_suggest: true
  api_framework:
    priority: "high" 
    auto_suggest: true
  documentation:
    priority: "medium"
    auto_suggest: false
```

### Index Configuration
```yaml
# _ledger/at_tag_config.yaml
indexing:
  scan_directories:
    - "dev_tools/"
    - "workspace/"
    - "_ledger/patterns/"
    - "documentation/"
  exclude_patterns:
    - "*.tmp"
    - "*_backup_*"
    - ".git/*"
  update_frequency: "daily"
  
pattern_detection:
  confidence_threshold: 0.7
  context_lines: 3
  cross_reference_similarity: 0.3
```

## CLI Aliases

### Bash Aliases
```bash
# Add to ~/.bashrc or ~/.zshrc
alias @find='python3 _system/scripts/at_tag_processor.py --search'
alias @scan='python3 _system/scripts/at_tag_processor.py --scan-all'  
alias @update='python3 _system/scripts/at_tag_processor.py --update-index'
alias @report='python3 _system/scripts/at_tag_processor.py --generate-report'
alias @related='python3 _system/scripts/at_tag_processor.py --suggest'

# Quick searches
alias @api='@find @router @app @api'
alias @mcp='@find @mcp_tool @server.agent @recursive_agent'  
alias @test='@find @patch @given @task @pytest'
alias @perf='@find @lru_cache @cached @performance'
```

### Power User Shortcuts
```bash
# Complex search shortcuts
alias @full-stack='@find @api @database @frontend @backend'
alias @ai-patterns='@find @mcp @agent @consciousness @recursive'
alias @quality='@find @testing @validation @security @performance'
alias @docs='@find @documentation @architecture @workflow @example'
```

## Usage Examples by Scenario

### Scenario 1: Finding API Patterns
```bash
# Step 1: Find all API-related patterns
@api

# Step 2: Focus on validation patterns
at-search @validator @api --intersection

# Step 3: Get related files for deeper exploration
at-related notes/dev_tools/patterns/api_patterns.md

# Step 4: Show context for specific patterns
at-context @router.post 5
```

### Scenario 2: Exploring MCP Integration
```bash
# Step 1: Find all MCP patterns
@mcp

# Step 2: Analyze MCP pattern relationships
at-analyze --relationships --category=mcp_integration

# Step 3: Find files that need MCP documentation
at-find --missing --category=mcp_integration

# Step 4: Generate MCP integration report
at-report --category=mcp_integration
```

### Scenario 3: Code Quality Review
```bash
# Step 1: Find all testing patterns
@test

# Step 2: Find files missing test tags
at-lint --missing-tags --category=testing

# Step 3: Cross-reference testing with API patterns
at-search @testing @api --intersection

# Step 4: Generate quality assessment report
at-report --quality --category=testing
```

## Error Handling & Troubleshooting

### Common Issues
```bash
# Index not found
at-search @anything
# Output: ❌ No index found. Run --scan-all first.
# Solution: python3 _system/scripts/at_tag_processor.py --scan-all

# No results found
at-search @nonexistent
# Output: ❌ No files found with tags: @nonexistent
# Solution: Use at-patterns --suggest to see available patterns

# Performance issues
at-search @common_pattern
# Output: 🐌 Large result set, consider adding filters
# Solution: Use --confidence, --category, or --limit options
```

### Debug Commands
```bash
# Debug index
at-debug --index-stats                # Show index statistics
at-debug --verify-integrity          # Verify index integrity
at-debug --performance-profile       # Profile search performance

# Debug patterns
at-debug --pattern-validation        # Validate all @ patterns
at-debug --detection-accuracy        # Test pattern detection accuracy
at-debug --missing-classifications   # Find unclassified @ patterns
```

## Performance Optimization

### Search Performance
- Index is cached in memory after first load
- Search uses optimized data structures for O(log n) lookups  
- Cross-references pre-computed during indexing
- Confidence filtering applied early to reduce result set

### Index Performance
- Incremental updates only scan changed files
- File hashing prevents unnecessary reprocessing
- Parallel processing for large repositories
- Configurable scan frequency and scope

---

**Commands Status**: ✅ Ready for Implementation
**Integration**: Compatible with existing doc-manager, pattern-extract, workspace-nav
**Performance**: Optimized for repositories up to 10,000 files
**Maintenance**: Auto-updating index with configurable frequency