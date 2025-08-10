---
pattern_name: rule-to-tag-pipeline
pattern_type: workflow
source_files:
  - _ledger/scripts/extract_patterns.md
  - _system/metadata/tagging_system/metadata_schema.yaml
  - _system/metadata/tagging_system/metadata_injector.py
  - _system/metadata/tagging_system/discovery_engine.py
confidence: 0.9

## Purpose
Convert natural-language "system rules" and repeated logic across the notes repo into reusable, taggable specifications and YAML frontmatter using an extraction → transformation → validation → injection pipeline.

## Inputs
- content_glob: string, file selector (e.g., "**/*.md")
- schema_path: path, metadata schema YAML (defaults to `_system/metadata/tagging_system/metadata_schema.yaml`)
- taxonomy: object, tag taxonomy loaded from schema
- validators: list, validation rules from schema.validation_rules

## Process
1. Discovery
   - Scan `content_glob` for candidate files
   - Parse markdown sections; detect rule-like lines and repeated structures per `extract_patterns.md`
2. Extraction
   - Produce `pattern_candidates` with confidence scores and suspected pattern_type (workflow|algorithm|architecture|meta)
3. Transformation
   - Normalize into spec format (inputs/process/outputs/constraints/examples)
   - Map terms to `tag_taxonomy` (consciousness/research/technical/functional/quality)
4. Validation
   - Apply `validation_rules.required_fields` and `consistency_checks`
   - Reject/flag candidates failing semantic checks
5. Injection
   - Write YAML frontmatter (uuid, title, tags) to original files
   - Save finalized specs to `_ledger/patterns/<type>/` and register in `_ledger/patterns/index.yaml`

## Outputs
- updated_files: list of files with injected/updated frontmatter
- specs_written: list of new/updated pattern specs
- index_updates: diff for `_ledger/patterns/index.yaml`

## Constraints
- Non-destructive: preserve original body text
- Deterministic YAML ordering
- UUID v4 required for every injected item

## Examples
```yaml
example:
  input:
    content_glob: "documentation/guides/**/*.md"
  output:
    updated_files: 17
    specs_written:
      - _ledger/patterns/workflows/rule-to-tag-pipeline.md
      - _ledger/patterns/meta/pattern-stitching-architecture.md
```

## Implementation Notes
- Discovery and extraction are provided by `discovery_engine.py`
- Frontmatter writes via `metadata_injector.py` with schema from `metadata_schema.yaml`
- Keep all generated artifacts tracked by git for auditability







