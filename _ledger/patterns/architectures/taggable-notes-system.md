---
pattern_name: taggable-notes-system
pattern_type: architecture
source_files:
  - WORKSPACE_INDEX.md
  - _system/metadata/tagging_system/metadata_schema.yaml
  - _ledger/scripts/extract_patterns.md
confidence: 0.8

## Purpose
Describe the architecture that turns a messy notes folder into a modular, taggable, AI-ready knowledge base.

## Components
- Content Store: repository tree (`documentation/`, `dev_tools/`, `_archive/`, etc.)
- Pattern Library: `_ledger/patterns/*`
- Metadata System: schema + injector + discovery
- Reports & Ledger: `_ledger/reports/*`, `_ledger/manifest.*`
- Workspace Index: `WORKSPACE_INDEX.md`

## Interactions
1. New notes are written anywhere in the tree
2. Discovery finds candidates and proposes specs
3. Validator ensures frontmatter consistency with schema
4. Injector writes YAML and registers spec files
5. Index provides navigation; reports provide audit trail

## Constraints
- Non-destructive frontmatter edits
- Tag taxonomy centralized in schema
- Everything verifiable via git history


