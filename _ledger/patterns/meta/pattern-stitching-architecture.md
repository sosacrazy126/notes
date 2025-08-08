---
pattern_name: pattern-stitching-architecture
pattern_type: meta
source_files:
  - _ledger/scripts/extract_patterns.md
  - dev_tools/fabric_patterns/specialized/experimental/review_design/system.md
  - _system/metadata/tagging_system/metadata_schema.yaml
confidence: 0.85

## Purpose
Define how extracted specs are stitched into a coherent knowledge system where rules become tags, tags drive discovery, and discovery feeds back into extraction.

## Architecture
Components:
1. Discovery Engine (`_system/metadata/tagging_system/discovery_engine.py`)
2. Extractor (per `extract_patterns.md` Phases 1–2)
3. Validator (schema `validation_rules`)
4. Injector (`metadata_injector.py` frontmatter writer)
5. Registry (`_ledger/patterns/index.yaml` + directories)
6. Review Loop (human-in-the-loop using `review_design` prompt)

Data Flow:
- Files → Discovery → Extraction → Transformation → Validation → Injection → Registry → Search/Review → New candidates

Interfaces:
- Input: file paths, raw markdown, optional code blocks
- Output: YAML frontmatter, pattern specs, index entries

## Constraints
- Keep human review checkpoints before injection in high-risk areas
- Schema remains single source of truth for taxonomy and validation

## Review Guidance
Use `dev_tools/fabric_patterns/specialized/experimental/review_design/system.md` to evaluate clarity, integration, security, performance, and maintainability of the pipeline.


